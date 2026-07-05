"""Edit-mode auth.

Replaces the original hardcoded-password + Flask session with a signed,
stateless bearer token. The password now comes from EDIT_PASSWORD; if unset it
falls back to the legacy value (with a one-time warning) so behaviour is
preserved out-of-the-box. Compared with hmac.compare_digest (constant-time).
"""
import hmac

from fastapi import Header, HTTPException
from itsdangerous import URLSafeTimedSerializer, BadData

from .config import get_settings

_LEGACY_PASSWORD = "2Galletas!"
_MAX_AGE = 60 * 60 * 24 * 7  # tokens valid for 7 days
_warned = False


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(get_settings().SECRET_KEY, salt="lotalf-edit-mode")


def _expected_password() -> str:
    global _warned
    pw = get_settings().EDIT_PASSWORD
    if not pw:
        if not _warned:
            print("[lotalf] WARNING: EDIT_PASSWORD not set — using the legacy password. "
                  "Set EDIT_PASSWORD in .env to change it.")
            _warned = True
        return _LEGACY_PASSWORD
    return pw


def verify_password(password: str) -> bool:
    return hmac.compare_digest(password or "", _expected_password())


def make_token() -> str:
    return _serializer().dumps({"role": "editor"})


def is_valid_token(token: str) -> bool:
    try:
        _serializer().loads(token, max_age=_MAX_AGE)
        return True
    except BadData:
        return False


def require_editor(authorization: str = Header(default="")) -> bool:
    """FastAPI dependency for write endpoints."""
    token = ""
    if authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    if not is_valid_token(token):
        raise HTTPException(status_code=401, detail="No autorizado. Identifíquese para editar.")
    return True
