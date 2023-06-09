from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/vocab/")
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, self.template_name, {"form": form})
        login(request, user)
        return HttpResponseRedirect("/vocab/")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")
