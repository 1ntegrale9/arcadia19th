from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Village, Remark, Resident
from .forms import VillageForm, RemarkForm, ResidentForm, StartForm
from random import randint
from .charasetTable import *
from django.utils import timezone

class VillageIndex(CreateView):
    model = Village, Resident
    form_class = VillageForm
    template_name = 'werewolf/index.html'
    success_url = reverse_lazy('werewolf:index')

    def form_valid(self, form):
        form.instance.auther = self.request.user.username
        form.instance.character_name = getCharacterName(form.cleaned_data['character'])
        form.instance.character_img_url = getRandomCharacterImgURL(form.cleaned_data['character'])
        print(form.instance.character_img_url)
        return super(VillageIndex, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Village.objects.filter(palflag=0,endflag=0, delflag=0).order_by('-created_date')
        return context

class VillagePalIndex(VillageIndex):
    template_name = 'werewolf/pal.html'
    success_url = reverse_lazy('werewolf:pal')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Village.objects.filter(palflag=1,endflag=0, delflag=0).order_by('-created_date')
        return context

class VillageLog(ListView):
    model = Village
    template_name = 'werewolf/log.html'
    queryset = Village.objects.filter(endflag=1, delflag=0).order_by('-created_date')

def VillageView(request, village_id):
    this_village = Village.objects.get(id=village_id)
    limittime = this_village.daytime_length if this_village.nightflag == 0 else this_village.nighttime_length   
    update_time = timezone.timedelta(seconds=limittime) + this_village.updated_date
    if request.method == 'POST':
        if 'remark' in request.POST:
            remark_form = RemarkForm(request.POST)
            if remark_form.is_valid():
                post = remark_form.save(commit=False)
                post.user_id = request.user
                post.user = request.user.username
                post.village_id = village_id
                resident_self = Resident.objects.get(village=village_id, resident=request.user)
                post.days = this_village.days
                post.nightflag = this_village.nightflag
                post.character = resident_self.character
                post.charaset = resident_self.charaset
                post.character_img_url = getCharacterImgURL(post.charaset, post.character)
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
        elif 'resident' in request.POST:
            resident_form = ResidentForm(request.POST)
            resident_form.fields['character'].choices = getCharacterTable(this_village.character)
            if resident_form.is_valid():
                post = resident_form.save(commit=False)
                post.resident = request.user
                post.village_id = village_id
                post.charaset = this_village.character
                post.character_img_url = getCharacterImgURL(post.charaset, post.character)
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
        elif 'start' in request.POST:
            start_form = StartForm(request.POST)
            if start_form.is_valid():
                this_village.nightflag = 1
                this_village.startflag = 1
                this_village.started_date = timezone.now()
                this_village.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
    elif this_village.startflag and timezone.now() > update_time:
        if this_village.nightflag == 1:
            this_village.days += 1
        this_village.nightflag = 1 - this_village.nightflag
        this_village.updated_date = timezone.now()
        this_village.save()
        return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
    else:
        resident_form = ResidentForm()
        resident_form.fields['character'].choices = getCharacterTable(this_village.character)
        resident_list = Resident.objects.filter(village=village_id)
        remark_list   = Remark.objects.filter(
            delflag   = 0,
            village   = village_id,
            days      = this_village.days,
            nightflag = this_village.nightflag
            ).order_by('-date')[:100]
        context = {
            'start_form'   : StartForm(),
            'remark_form'  : RemarkForm(),
            'resident_form': resident_form,
            'remark_list'  : remark_list,
            'resident_list': resident_list,
            'village_info' : this_village,
            'update_time'  : update_time,
        }
        try:
            context['residentinfo'] = resident_list.get(resident=request.user)
            context['isResident'] = True
            context['isAuther'] = this_village.auther == request.user.username
            context['notStarted'] = this_village.startflag == 0
            context['icon_url'] = context['residentinfo'].character_img_url
        except:
            context['isResident'] = False
            context['notStarted'] = True
            context['icon_url'] = this_village.character_img_url
    return render(request, 'werewolf/village.html', context)
