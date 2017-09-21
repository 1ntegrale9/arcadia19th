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
        from .charasetTable import getCharacterName,getRandomCharacterImgURL
        form.instance.auther = self.request.user.username
        form.instance.character_name = getCharacterName(form.cleaned_data['character'])
        form.instance.character_img_url = getRandomCharacterImgURL(form.cleaned_data['character'])
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

def VillageView(request, village_id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import getVillageObject
    village_object = getVillageObject(village_id=village_id)
    if request.method == 'POST':
        if 'remark' in request.POST:
            from .forms import RemarkForm
            remark_form = RemarkForm(data=request.POST)
            if remark_form.is_valid():
                from .models import Resident
                from .charasetTable import getCharacterImgURL
                post = remark_form.save(commit=False)
                post.user_id = request.user
                post.user = request.user.username
                post.village_id = village_id
                resident_self = Resident.objects.get(village=village_id, resident=request.user)
                post.days = village_object.days
                post.nightflag = village_object.nightflag
                post.character = resident_self.character
                post.charaset = resident_self.charaset
                post.character_img_url = getCharacterImgURL(post.charaset, post.character)
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
            else:
                print(remark_form.errors.as_data())
        elif 'resident' in request.POST:
            from .forms import ResidentForm
            resident_form = ResidentForm(data=request.POST, village_object=village_object)
            if resident_form.is_valid():
                from .charasetTable import getCharacterImgURL
                post = resident_form.save(commit=False)
                post.resident = request.user
                post.village_id = village_id
                post.charaset = village_object.character
                post.character_img_url = getCharacterImgURL(post.charaset, post.character)
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
        elif 'start' in request.POST:
            from .forms import StartForm
            start_form = StartForm(data=request.POST)
            if start_form.is_valid():
                from django.utils import timezone
                village_object.nightflag = 1
                village_object.startflag = 1
                village_object.started_date = timezone.now()
                village_object.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
    else:
        from django.utils import timezone
        from .models import calculateUpdateTime
        next_update_time = calculateUpdateTime(village_object=village_object)
        if bool(village_object.startflag) and timezone.now() > next_update_time:
            village_object.days += village_object.nightflag
            village_object.nightflag = 1 - village_object.nightflag
            village_object.updated_date = timezone.now()
            village_object.save()
            return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
        else:
            from .forms import RemarkForm,ResidentForm,StartForm
            from .models import getRemarkObjects,getResidentObjects
            context = {
                'start_form'   : StartForm(),
                'remark_form'  : RemarkForm(),
                'resident_form': ResidentForm(village_object=village_object),
                'remark_list'  : getRemarkObjects(village_object=village_object)[:100],
                'resident_list': getResidentObjects(village_id=village_id),
                'village_info' : village_object,
                'update_time'  : next_update_time,
            }
            # クソ実装
            try:
                context['residentinfo'] = context['resident_list'].get(resident=request.user)
                context['isResident'] = True
                context['isAuther'] = village_object.auther == request.user.username
                context['notStarted'] = not bool(village_object.startflag)
                context['icon_url'] = context['residentinfo'].character_img_url
            except:
                context['isResident'] = False
                context['notStarted'] = True
                context['icon_url'] = village_object.character_img_url
        from django.shortcuts import render
        return render(request, 'werewolf/village.html', context)
