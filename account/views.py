from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .forms import RegisterForm, LoginForm

class MyPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "account/info.html"

class CreateUserView(generic.CreateView):
    template_name = 'account/create.html'
    form_class = RegisterForm
    success_url = reverse_lazy('werewolf:index')

def login(request):
    context = {
        'template_name': 'account/login.html',
        'authentication_form': LoginForm
    }
    return auth_views.login(request, **context)

def logout(request):
    context = {
        'template_name': 'werewolf/index.html',
    }
    return auth_views.logout(request, **context)
