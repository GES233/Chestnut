
from ..application.user.service.user_auth import PasswordService
from ..infra.deps.password import hashpassword, checkpassword


pswd_bcrypt_adapter = PasswordService(en=hashpassword, de=checkpassword)
