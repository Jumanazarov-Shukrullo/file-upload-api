from fastapi import APIRouter
from core.security import create_access_token

router = APIRouter()

@router.get("/token", summary="Generate a demo JWT (no creds required)")
def generate_token():
    # you could embed any payload you like here
    token = create_access_token({"sub": "demo-user"}, expires_delta=60*24)
    return {"access_token": token, "token_type": "bearer"}
