from django.views.generic import TemplateView

class AboutPageView(TemplateView):
    template_name = 'index/top.html'

class WelcomePageView(TemplateView):
    template_name = 'index/welcome.html'

class CharasetView(TemplateView):
    template_name = 'index/charaset.html'
