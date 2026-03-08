import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# ================= 配置区域 =================
# 所有敏感信息都应该配置在 .env 文件中
HF_TOKEN = os.getenv("HF_TOKEN") 
SPACE_URL = os.getenv("SPACE_URL")

WX_APP_ID = os.getenv("WX_APP_ID")
WX_APP_SECRET = os.getenv("WX_APP_SECRET")

# JWT 配置
JWT_SECRET = os.getenv("JWT_SECRET", "SUPER_SECRET_CHANGE_THIS_IN_PROD_123456")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "120"))  # Token 有效期 2 小时
