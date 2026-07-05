from hashlib import md5

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .. import db

router = APIRouter(prefix="/api/comments", tags=["comments"])


def _identicon(name: str) -> str:
    digest = md5((name or "").encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?d=identicon"


@router.get("")
def list_comments(session=Depends(db.get_session)):
    C = db.table("comments")
    rows = session.query(C).all()
    out = []
    for r in rows:
        d = db.row_to_dict(r)
        d["identicon"] = _identicon(d.get("name", ""))
        out.append(d)
    out.reverse()  # newest first (parity with the Flask view)
    return out


class CommentIn(BaseModel):
    name: str
    email: str
    comment: str


@router.post("")
def add_comment(body: CommentIn, session=Depends(db.get_session)):
    C = db.table("comments")
    session.add(C(name=body.name, email=body.email, comment=body.comment))
    session.commit()
    return {"ok": True}
