from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
hash_passsword = PasswordHash.recommended()
def password_hash(password:str)->str:
    return hash_passsword.hash(password)

def varify_password(password:str,hashPassword:str)->bool:
    return hash_passsword.verify(password,hashPassword)


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl='auth/login'
)