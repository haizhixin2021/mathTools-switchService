from pydantic import BaseModel

# ================= 数据模型 =================
class LoginRequest(BaseModel):
    code: str

class ProxyRequest(BaseModel):
    inputs: dict  # 传给 HF 的实际业务数据
