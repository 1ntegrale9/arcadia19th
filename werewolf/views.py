from django.views.generic import ListView, CreateView

class OpenVillageIndexView(CreateView):
    from django.core.urlresolvers import reverse_lazy
    from .models import Village,Resident
    from .forms import VillageForm
    model = Village, Resident
    form_class = VillageForm
    template_name = 'werewolf/index.html'
    success_url = reverse_lazy('werewolf:index')
    def form_valid(self, form):
        from .forms import createVillage
        createVillage(request=self.request,form=form)
        return super(OpenVillageIndexView, self).form_valid(form)
    def get_context_data(self, *args, **kwargs):
        from .models import getOpenVillageObjects
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = getOpenVillageObjects()
        return context

class PalVillageIndexView(OpenVillageIndexView):
    from django.core.urlresolvers import reverse_lazy
    template_name = 'werewolf/pal.html'
    success_url = reverse_lazy('werewolf:pal')
    def get_context_data(self, *args, **kwargs):
        from .models import getPalVillageObjects
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = getPalVillageObjects()
        return context

class EndVillageIndexView(ListView):
    from .models import Village,getEndVillageObjects
    model = Village
    queryset = getEndVillageObjects()
    template_name = 'werewolf/log.html'

def VillageView(request,village_id):
    from .models import getVillageObject
    village_object = getVillageObject(village_id=village_id)
    if request.method == 'POST':
        if request.POST['form'] == 'remark':
            from .forms import remarkPost
            do_redirect = remarkPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'resident':
            from .forms import residentPost
            do_redirect = residentPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'start':
            from .forms import startPost
            do_redirect = startPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'vote':
            from .forms import votePost
            do_redirect = votePost(request=request,village_object=village_object)
    else:
        from django.utils import timezone
        from .models import calculateUpdateTime
        next_update_time = calculateUpdateTime(village_object=village_object)
        if bool(village_object.startflag) and timezone.now() > next_update_time:
            from .forms import villageUpdate,residentUpdate
            residentUpdate(village_object=village_object)
            villageUpdate(village_object=village_object)
            do_redirect = True
        else:
            from .forms import getVillageContext
            context = getVillageContext(request=request,village_object=village_object,next_update_time=next_update_time)
            from django.shortcuts import render
            return render(request, 'werewolf/village.html', context)
    if do_redirect:
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
