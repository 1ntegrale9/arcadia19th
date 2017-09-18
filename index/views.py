from django.views import generic

class TopPageView(generic.TemplateView):
    template_name = 'index/top.html'
