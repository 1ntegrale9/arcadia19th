from django.views.generic import TemplateView

class WelcomePageView(TemplateView):
    template_name = 'index/welcome.html'
