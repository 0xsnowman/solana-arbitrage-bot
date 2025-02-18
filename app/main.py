from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import trades, balances, email_verification

app = FastAPI(title="Solana Arbitrage Bot - Solace")

# Allow requests from your frontend (adjust the origin if necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],
)

# Include routers
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(balances.router, prefix="/balances", tags=["Balances"])
app.include_router(email_verification.router, prefix="/email", tags=["Email Verification"])

@app.get("/")
def root():
    return {"message": "Welcome to Solana Arbitrage Bot"}
