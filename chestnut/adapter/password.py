
from ..application.user.service.register import PasswordService
from ..infra.deps.password import hashpassword, checkpassword


pswd_bcrypt_adapter = PasswordService(en=hashpassword, de=checkpassword)
