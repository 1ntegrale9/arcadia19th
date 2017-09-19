from django.views.generic import TemplateView

class TopPageView(TemplateView):
    template_name = 'index/top.html'

class CharasetView(TemplateView):
    template_name = 'index/charaset.html'
