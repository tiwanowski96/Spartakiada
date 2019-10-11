from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .forms import UserCreateForm, UserLoginForm


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'loging/user_form.html'
    success_url = reverse_lazy('login')


class UserLoginView(View):

    def get(self, request):
        form = UserLoginForm()
        ctx = {'form': form}
        return render(request, 'loging/user_login_form.html', ctx)

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'loging/user_login_form.html', ctx)


class UserLogoutView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/')
        else:
            return redirect('login')

