from fastapi import FastAPI
from app.api.routes import trades, balances, email_verification

app = FastAPI(title="Solana Arbitrage Bot")

# Include routers
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(balances.router, prefix="/balances", tags=["Balances"])
app.include_router(email_verification.router, prefix="/email", tags=["Email Verification"])

@app.get("/")
def root():
    return {"message": "Welcome to Solana Arbitrage Bot"}
