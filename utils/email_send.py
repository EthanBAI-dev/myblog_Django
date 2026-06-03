import random
import string
from users.models import EmailVerifyRecord
from django.core.mail import send_mail


def random_str(randomlength=8):
    """生成指定长度的随机字符串"""
    chars = string.ascii_letters + string.digits
    strcode = ''.join(random.sample(chars, randomlength))
    return strcode


def send_register_email(email, send_type='register'):
    """发送邮件：注册激活 or 忘记密码"""
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '博客注册激活链接'
        email_body = '请点击以下链接激活账号：http://127.0.0.1:8000/users/active/{0}'.format(code)
        send_mail(email_title, email_body, 'admin@blog.com', [email])

    elif send_type == 'forget':
        email_title = '博客密码找回链接'
        email_body = '请点击以下链接修改密码：http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)
        send_mail(email_title, email_body, 'admin@blog.com', [email])
