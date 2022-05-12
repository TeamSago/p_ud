from django import forms
from .models import User
from argon2 import PasswordHasher, exceptions
from argon2.exceptions import VerifyMismatchError

# user_id, user_pw, user_pw_confirm, user_name, user_email
class RegisterForm(forms.ModelForm):
    user_id = forms.CharField(
        label="User ID",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "user_id",
                "placeholder": "User ID",
            }
        ),
        error_messages={
            "required": "User ID is required.",
            "unique": "User ID already exists.",
        },
    )

    user_pw = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "user_pw",
                "placeholder": "Password",
            }
        ),
        error_messages={"required": "Password is required."},
    )
    user_pw_confirm = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "user_pw_confirm",
                "placeholder": "Confirm Password",
            }
        ),
        error_messages={"required": "Password does not match."},
    )
    user_name = forms.CharField(
        label="User Name",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "user_name",
                "placeholder": "User Name",
            }
        ),
        error_messages={
            "required": "User Name is required.",
            "unique": "User Name already exists.",
        },
    )
    user_email = forms.CharField(
        label="User Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "user_email",
                "placeholder": "User Email",
            }
        ),
        error_messages={
            "required": "Email is required.",
            "unique": "User Email already exists.",
        },
    )
    field_order = [
        "user_id",
        "user_pw",
        "user_pw_confirm",
        "user_name",
        "user_email",
    ]

    class Meta:
        model = User
        fields = [
            "user_id",
            "user_pw",
            "user_name",
            "user_email",
        ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get("user_id", "")
        user_pw = cleaned_data.get("user_pw", "")
        user_pw_confirm = cleaned_data.get("user_pw_confirm", "")
        user_name = cleaned_data.get("user_name", "")
        user_email = cleaned_data.get("user_email", "")

        if user_pw != user_pw_confirm:
            return self.add_error("user_pw_confirm", "Password does not match.")
        elif not (4 <= len(user_id) <= 16):
            return self.add_error(
                "user_id", "User ID must be in between 4 and 16 characters."
            )
        elif 8 > len(user_pw):
            return self.add_error("user_pw", "Password must be more than 8 characters.")
        else:
            self.user_id = user_id
            self.user_pw = PasswordHasher().hash(user_pw)
            self.user_pw_confirm = user_pw_confirm
            self.user_name = user_name
            self.user_email = user_email


# loginform 제작
class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label="User ID",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "user_id",
                "placeholder": "User ID",
            }
        ),
        error_messages={"required": "User ID is required."},
    )
    user_pw = forms.CharField(
        max_length=128,
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "user_pw",
                "placeholder": "Password",
            }
        ),
        error_messages={"required": "Password is required."},
    )

    field_order = [
        "user_id",
        "user_pw",
    ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get("user_id", "")
        user_pw = cleaned_data.get("user_pw", "")

        if user_id == "":
            return self.add_error("user_id", "Incorrect User ID.")
        elif user_pw == "":
            return self.add_error("user_pq", "Incorrect Password.")
        else:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return self.add_error("user_id", "User ID dose not exist.")

            try:
                PasswordHasher().verify(user.user_pw, user_pw)
            except exceptions.VerifyMismatchError:
                return self.add_error("user_pw", "Wrong Password.")

            self.login_session = user.user_id


# RegisterForm은 ModelForm, LoginForm은 Form.
# 둘의 차이점은, 전자는 모델의 속성값들을 그대로 이어받지만, 후자는 그렇지 않으므로 max_length처럼 필드속성을 추가해야함.
