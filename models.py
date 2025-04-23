from pydantic import BaseModel

class CallMessage(BaseModel):
    type: str = "call"
    from_user: str
    group: str
    remark: str = ""

class JoinMessage(BaseModel):
    action: str = "join"
    group: str
    remark: str = ""

class LeaveMessage(BaseModel):
    action: str = "leave"
    group: str

class CallAction(BaseModel):
    action: str = "call"
    group: str
