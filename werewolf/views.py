from django.views.generic import ListView, CreateView
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .models import Village,Resident,getEndVillageObjects,getOpenVillageObjects,getPalVillageObjects,getVillageObject,calculateUpdateTime
from .forms import remarkPost,residentPost,startPost,votePost,VillageForm,createVillage,villageUpdate,residentUpdate,getVillageContext
from django.shortcuts import render

class OpenVillageIndexView(CreateView):
    model = Village, Resident
    form_class = VillageForm
    template_name = 'werewolf/index.html'
    success_url = reverse_lazy('werewolf:index')
    def form_valid(self, form):
        createVillage(request=self.request,form=form)
        return super(OpenVillageIndexView, self).form_valid(form)
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = getOpenVillageObjects()
        return context

class PalVillageIndexView(OpenVillageIndexView):
    template_name = 'werewolf/pal.html'
    success_url = reverse_lazy('werewolf:pal')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = getPalVillageObjects()
        return context

class EndVillageIndexView(ListView):
    model = Village
    queryset = getEndVillageObjects()
    template_name = 'werewolf/log.html'

def VillageView(request,village_id):
    village_object = getVillageObject(village_id=village_id)
    if request.method == 'POST':
        if request.POST['form'] == 'remark':
            do_redirect = remarkPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'resident':
            do_redirect = residentPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'start':
            do_redirect = startPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'vote':
            do_redirect = votePost(request=request,village_object=village_object)
    else:
        next_update_time = calculateUpdateTime(village_object=village_object)
        if bool(village_object.startflag) and timezone.now() > next_update_time:
            residentUpdate(village_object=village_object)
            villageUpdate(village_object=village_object)
            do_redirect = True
        else:
            context = getVillageContext(request=request,village_object=village_object,next_update_time=next_update_time)
            return render(request, 'werewolf/village.html', context)
    if do_redirect:
        return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
