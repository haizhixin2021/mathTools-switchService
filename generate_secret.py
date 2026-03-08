import secrets
import string

# 生成 32 字节的随机密钥（推荐用于生产环境）
secret_key = secrets.token_urlsafe(32)
print(f"JWT_SECRET (推荐): {secret_key}")

# 生成 64 字节的随机密钥（更安全）
secret_key_64 = secrets.token_urlsafe(64)
print(f"JWT_SECRET (更安全): {secret_key_64}")

# 使用字母和数字生成 32 位密钥
alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(32))
print(f"JWT_SECRET (字母数字): {password}")
