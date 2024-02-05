from django import forms
from .models import Users
from django.contrib.auth.hashers import check_password


class Changed_outline(forms.Form):
    paper_DOI = forms.CharField()
    original_outline = forms.CharField()
    changed_outline = forms.CharField()

"""doi 입력 받기"""
class Doi(forms.Form):
    doi = forms.URLField()

class Test4(forms.Form):
    doi = forms.URLField()
#
# class relation(forms.Form):


"""바뀐 Outline 입력받기"""
# class Changed_Outline(forms.ModelForm):
#     origin_outline = forms.


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        label="사용자이름",
        required=True,
        widget=forms.TextInput(
            attrs={
                'calss' : 'user-id',
                'placeholder' : '아이디'
            }
        ),
        error_messages={
            'required': '아이디를 입력해주세요'
        },
    )


    password = forms.CharField(
        max_length=128,
        label="비밀번호",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'user-pw',
                'placeholder' : '비밀번호'
            }
        ),
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
    )

    field_order = [
        'user_id',
        'user_pw',
    ]

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.post('id')
        password = cleaned_data.post('pwd')

        if username and password:
            try:
                user = Users.objects.post(username=username)
                if not check_password(password, user.password):
                    self.add_error('password', '비밀번호를 틀렸습니다.')
                else:
                    self.user_id = user.id(8)
            except Exception:
                self.add_error('username', '존재하지 않는 아이디 입니다.')
