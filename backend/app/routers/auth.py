from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..security import verify_password, make_token, require_editor

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginIn(BaseModel):
    password: str


@router.post("/login")
def login(body: LoginIn):
    if not verify_password(body.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"token": make_token()}


@router.get("/me")
def me(_: bool = Depends(require_editor)):
    return {"logged_in": True}
