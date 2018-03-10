from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .models import Village,Resident,getEndVillageObjects,getOpenVillageObjects,getStartVillageObjects,getPalVillageObjects,getVillageObject,calculateUpdateTime
from .forms import remarkPost,residentPost,startPost,votePost,VillageForm,createVillage,villageUpdate,residentUpdate,getVillageContext
from django.shortcuts import render

# トップページ
class AboutPageView(TemplateView):
    template_name = 'werewolf/about.html'

## キャラセット情報
class CharasetView(TemplateView):
    template_name = 'index/charaset.html'

# 村を建てる
class CreateVillageView(CreateView):
    form_class = VillageForm
    template_name = 'werewolf/create.html'
    success_url = reverse_lazy('werewolf:open')
    def form_valid(self, form):
        createVillage(request=self.request,form=form)
        return super().form_valid(form)

# 募集中
class OpenVillageIndexView(ListView):
    model = Village
    queryset = getOpenVillageObjects()
    template_name = 'werewolf/index.html'

# 進行中
class StartVillageIndexView(ListView):
    model = Village
    queryset = getStartVillageObjects()
    template_name = 'werewolf/index.html'

# 過去村
class EndVillageIndexView(ListView):
    model = Village
    queryset = getEndVillageObjects()
    template_name = 'werewolf/index.html'

# 身内村
class PalVillageIndexView(ListView):
    model = Village
    queryset = getPalVillageObjects()
    template_name = 'werewolf/index.html'

# 入村後
def VillageView(request,village_id):
    village_object = getVillageObject(village_id=village_id)
    # フォーム送信
    if request.method == 'POST':
        if request.POST['form'] in 'remark': # 発言
            do_redirect = remarkPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'vote': # 投票
            do_redirect = votePost(request=request,village_object=village_object)
        elif request.POST['form'] == 'resident': # 入村
            do_redirect = residentPost(request=request,village_object=village_object)
        elif request.POST['form'] == 'start': # 開始
            do_redirect = startPost(request=request,village_object=village_object)
    # 更新処理
    else:
        next_update_time = calculateUpdateTime(village_object=village_object)
        if bool(village_object.startflag) and timezone.now() > next_update_time:
            residentUpdate(village_object=village_object)
            villageUpdate(village_object=village_object)
            do_redirect = True
        else:
            context = getVillageContext(request=request,village_object=village_object,next_update_time=next_update_time)
            return render(request, 'werewolf/village.html', context)
    # リロード
    if do_redirect:
        return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
