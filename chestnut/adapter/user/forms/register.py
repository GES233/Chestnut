from typing import Any
from wtforms.form import Form
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from pydantic import BaseModel, EmailStr, validator, ValidationError

from ....application.user.dto.register import RegisterForm


class SignUpForm(Form):
    nickname = StringField(
        "nickname",
        validators=[DataRequired()],
        render_kw={"placeholder": "昵称", "aria-label": "昵称", "autocomplete": "nickname"},
    )
    email = StringField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={
            "placeholder": "邮件地址",
            "aria-label": "邮件地址",
            "autocomplete": "email",
        },
    )
    password = PasswordField(
        "password",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "密码",
            "aria-label": "密码",
        },
    )
    confirm = PasswordField(
        "confirm",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={
            "placeholder": "确认密码",
            "aria-label": "确认密码",
        },
    )
    remember = BooleanField(render_kw={"role": "switch", "checked": "checked"})


def check_signup_form(form: SignUpForm) -> RegisterForm | SignUpForm:
    if form.validate():
        return SignUpModel(
            nickname=form.nickname.data,  # type: ignore
            email=form.email.data,  # type: ignore
            password=form.password.data,  # type: ignore
            confirm=form.confirm.data,  # type: ignore
            remember=form.remember.data
        ).todto()
    else:
        if form.confirm.errors:
            form.confirm.render_kw["aria-invalid"] = "true"
            form.confirm.render_kw["placeholder"] = "密码不一致"
            form.confirm.render_kw["value"] = ""
            form.password.render_kw["value"] = ""
        elif form.email.errors:
            form.email.render_kw["aria-invalid"] = "true"
            form.email.render_kw["placeholder"] = "邮件格式错误"
            form.email.render_kw["value"] = ""
        return form


def common_nickname(form: SignUpForm) -> SignUpForm:
    form.nickname.render_kw["aria-invalid"] = "true"
    form.nickname.render_kw["placeholder"] = "与其他用户重名"
    form.nickname.render_kw["value"] = ""  # Delete
    form.email.render_kw["value"] = form.email.data
    return form


def common_email(form: SignUpForm) -> SignUpForm:
    form.email.render_kw["aria-invalid"] = "true"
    form.email.render_kw["placeholder"] = "邮件与其他用户冲突"
    form.email.render_kw["value"] = ""  # Delete
    form.nickname.render_kw["value"] = form.nickname.data
    return form


class SignUpModel(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    confirm: str
    remember: bool

    @validator("confirm")
    def passwd_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValidationError("Password not same!", SignUpModel)
    
    def todto(self):
        return RegisterForm(nickname=self.nickname, email=self.email, password=self.password)
