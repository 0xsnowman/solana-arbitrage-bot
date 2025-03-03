from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.types import TokenAccountOpts, TxOpts
from solders.transaction import VersionedTransaction
from solders.transaction_status import TransactionConfirmationStatus
from solders.signature import Signature
from solders import message
from solana.rpc.commitment import Confirmed
from constants import JUPITER_ENDPOINT, SOL_ADDRESS
import base58, base64, requests, time


def get_keypair(private_key: str):
    private_key_bytes = base58.b58decode(private_key)
    keypair = Keypair.from_bytes(private_key_bytes)
    return keypair


def get_sol_balance(client: Client, wallet_address: str):
    pubkey = Pubkey(base58.b58decode(wallet_address))
    try:
        sol_balance = client.get_balance(pubkey)
        sol_decimals = 9
        ui_amount = float(sol_balance.value / 10 ** sol_decimals)
        payload = {
            "amount": int(sol_balance.value),
            "decimals": int(sol_decimals),
            "uiAmount": ui_amount
        }
        return payload
    except Exception as e:
        print(str(e))
        return {
            "amount": int(0),
            "decimals": int(0),
            "uiAmount": float(0)
        }
        
        
def get_spl_balance(client: Client, wallet_address: str, mint_address: str):
    try:
        pubkey = Pubkey(base58.b58decode(wallet_address))
        mint_pubkey = Pubkey(base58.b58decode(mint_address))
        response = client.get_token_accounts_by_owner(
            pubkey,
            TokenAccountOpts(mint=mint_pubkey),
        )
        payload = {}
            
        if len(response.value) > 0:
            token_account = response.value[0].pubkey
            spl_balance = client.get_token_account_balance(token_account)
            payload = {
                "amount": int(spl_balance.value.amount),
                "decimals": int(spl_balance.value.decimals),
                "uiAmount": float(spl_balance.value.ui_amount_string)
            }
        else:
            payload = {
                "amount": int(0),
                "decimals": int(9),
                "uiAmount": float(0)
            }
        return payload
    except Exception as e:
        print(str(e))
        return {
            "amount": int(0),
            "decimals": int(9),
            "uiAmount": float(0)
        }
        
        
def confirm_transaction(client: Client, txid: Signature):
    start_time = time.time()
    timeout = 30
    while True:
        # Check if timeout has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            break
        
        # Get transaction status
        response = client.get_signature_statuses([txid])
        status = response.value[0]  # Status of the transaction
        
        if status is not None:
            confirmation_status = status.confirmation_status
            if confirmation_status == TransactionConfirmationStatus.Confirmed:
                print("Transaction confirmed!")
                return True
        else:
            print("Transaction not found. Retrying...")
        # Wait for a short period before retrying
        time.sleep(2)
    return False

        
def send_transaction(client: Client, tx: VersionedTransaction):
    try:
        send_options = TxOpts(
            skip_preflight=False,
            max_retries=0,
            preflight_commitment=Confirmed,
            skip_confirmation=True
        )
        txid = client.send_raw_transaction(bytes(tx), send_options)
        status = confirm_transaction(client, txid.value)
        if status:
            return txid.__str__()
        return ""
    except Exception as e:
        print(str(e))
        return ""
        
        
def fetch_quote(mint: str, amount: int, slippage: int):
    try:
        response = requests.get(
            f"{JUPITER_ENDPOINT}/quote?"
            f"inputMint={mint}&"
            f"outputMint={SOL_ADDRESS}&"
            f"amount={amount}&"
            f"slippageBps={slippage}&"
            f"onlyDirectRoutes=false&"
            f"asLegacyTransaction=false&"
        )
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(response.text)
            return {}
    except Exception as e:
        print(str(e))
        return {}
    
    
def fetch_swap(endpoint: str, quote: dict, keypair: Keypair, settings: dict):
    prioritization_fee = 0
    payload = {
        "method": "qn_estimatePriorityFees",
        "id": 1,
        "jsonrpc": '2.0',
        "params": {
            "last_n_blocks": 100,
            "account": "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"
        }
    }

    try:
        response = requests.post(endpoint, json=payload)
        data = response.json()
        speed = settings["priority_fee"]
        prioritization_fee = int(data["result"]["per_compute_unit"][speed])
    except Exception as e:
        print(str(e))
        return None

    # Construct the payload
    payload = {
        "quoteResponse": quote,
        "userPublicKey": keypair.pubkey().__str__(),
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": prioritization_fee
    }

    try:
        response = requests.post(f"{JUPITER_ENDPOINT}/swap", json=payload)
        data = response.json()
        swap_transaction_base64 = data['swapTransaction']

        # Decode the base64 transaction
        swap_transaction_buf = base64.b64decode(swap_transaction_base64)

        # Deserialize the transaction
        transaction = VersionedTransaction.from_bytes(swap_transaction_buf)

        # Sign the transaction with the keypair
        signature = keypair.sign_message(message.to_bytes_versioned(transaction.message))
        signed_txn = VersionedTransaction.populate(transaction.message, [signature])

        return signed_txn
    except Exception as e:
        print(str(e))
        return None
