from wtforms.form import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired

from ....application.user.dto.login import LoginForm as LoginDTO


class LoginForm(Form):
    email = StringField(
        "email",
        validators=[DataRequired()],
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
            "autocomplete": "current-password",
        },
    )
    remember = BooleanField(render_kw={"role": "switch", "checked": "checked"})


def validate_login_form(form: LoginForm) -> LoginDTO | LoginForm:
    if form.validate():
        return LoginDTO.fromdict(**form.data)
    else:
        if form.email.errors:
            form.email.render_kw["aria-invalid"] = "true"
            form.email.render_kw["placeholder"] = "请填入邮箱"
        elif form.password.errors:
            form.password.render_kw["aria-invalid"] = "true"
            form.password.render_kw["placeholder"] = "请填入密码"
        return form


def user_not_exist(form: LoginForm) -> LoginForm:
    form.email.render_kw["aria-invalid"] = "true"
    form.email.render_kw["placeholder"] = "用户不存在！"
    return form


def password_not_match(form: LoginForm) -> LoginForm:
    form.password.render_kw["aria-invalid"] = "true"
    form.password.render_kw["placeholder"] = "密码错误"
    return form

def no_user_matched(form: LoginForm) -> LoginForm:
    form.email.render_kw["aria-invalid"] = "true"
    form.password.render_kw["aria-invalid"] = "true"
    return form
