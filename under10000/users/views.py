from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import RegisterForm, LoginForm

# Create your views here.
def register(request):
    register_form = RegisterForm()
    # register_form을 'forms'라는 이름으로 전달함.
    context = {"forms": register_form}

    if request.method == "GET":
        return render(request, "users/register.html")

    elif request.method == "POST":
        register_form = RegisterForm(request.POST)
        # is_valid() 메서드는 forms.py에서 작성한 clean() 메서드를 호출함.
        if register_form.is_valid():
            user = User(
                user_id=register_form.user_id,
                user_pw=register_form.user_pw,
                user_name=register_form.user_name,
                user_email=register_form.user_email,
            )
            user.save()
            return redirect("/")
        else:
            context["forms"] = register_form
        return render(request, "users/register.html", context)


def login(request):
    loginform = LoginForm()
    context = {"forms": loginform}

    if request.method == "GET":
        return render(request, "users/login.html")

    elif request.method == "POST":
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            request.session["login_session"] = loginform.login_session
            request.session.set_expiry(0)
            return redirect("/")
        else:
            context["forms"] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context["error"] = value
        return render(request, "users/login.html", context)


def logout(request):
    request.session.flush()
    return redirect("/")
