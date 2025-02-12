from fastapi import APIRouter, HTTPException
from app.services.email_service import send_email, verify_code
from app.schemas.email import EmailRequest, CodeVerification

router = APIRouter()

@router.post("/send-verification-code")
async def send_verification_code(request: EmailRequest):
    await send_email(request.email)
    return {"message": "Verification code sent!"}

@router.post("/verify-code")
async def check_code(request: CodeVerification):
    if await verify_code(request.email, request.code):
        return {"message": "Email verified successfully!"}
    raise HTTPException(status_code=400, detail="Invalid verification code")
