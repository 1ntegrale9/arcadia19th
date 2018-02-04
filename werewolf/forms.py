from django import forms
from django.utils import timezone
from random import choice
from .models import Village,Remark,Resident,Execute,getAliveResidentObjects,getRemarkObjects,getResidentObjects,getExecuteObjects
from .charasetTable import getCharasetChoices,getCharacterTable,getCharacterImgURL,getCharacterName,getRandomCharacterImgURL
from collections import defaultdict

# Utility Functions  
def generateSelectForm(choices):
    return forms.ChoiceField(widget=forms.Select, choices=choices)
def applyFormControl(target, fields):
    for f in fields:
        target.fields[f].widget.attrs['class'] = 'form-control'
def applyPlaceholder(target, messages):
    for f,s in messages.items():
        target.fields[f].widget.attrs['placeholder'] = s

# 村作成フォーム
class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('name','daytime_seconds','nighttime_seconds','charaset','palflag',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, self.fields)
        applyPlaceholder(self, self.getVillageFormPlaceholderTable())
    def getVillageFormPlaceholderTable(self):
        return {
            'name':'村の名前を入力',
            'daytime_seconds':'昼時間(秒)',
            'nighttime_seconds':'夜時間(秒)',
        }
    def getPalflagChoices():
        return (
            (0,'誰でも歓迎'),
            (1,'身内限定'),
        )
    charaset = generateSelectForm(getCharasetChoices())
    palflag = generateSelectForm(getPalflagChoices())

# 発言フォーム
class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'rows': 3}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, self.fields)

# 入村フォーム
class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ('character',)

    def __init__(self, village_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, self.fields)
        self.fields['character'].choices = getCharacterTable(village_object.charaset)

    character = forms.ChoiceField(widget=forms.Select)

# 開始フォーム
class StartForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ()

# 実行フォーム
class ExecuteForm(forms.ModelForm):
    class Meta:
        model = Execute
        fields = ('target',)

    def __init__(self, village_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, self.fields)
        self.fields['target'] = forms.ModelChoiceField(queryset=getAliveResidentObjects(village_id=village_object.id), empty_label='対象を選択してください')

# 発言
def remarkPost(request,village_object):
    remark_form = RemarkForm(data=request.POST)
    if remark_form.is_valid():
        resident_self = Resident.objects.get(village=village_object.id,resident=request.user)
        remark_object = remark_form.save(commit=False)
        remark_object.remarker = request.user
        remark_object.remarker_name = request.user.username
        remark_object.village_id = village_object.id
        remark_object.day = village_object.day
        remark_object.nightflag = village_object.nightflag
        remark_object.character = resident_self.character
        remark_object.charaset = resident_self.charaset
        remark_object.icon_url = getCharacterImgURL(remark_object.charaset, remark_object.character)
        remark_object.save()
        return True
    else:
        return False

def residentPost(request,village_object):
    resident_form = ResidentForm(data=request.POST,village_object=village_object)
    if resident_form.is_valid():
        resident_object = resident_form.save(commit=False)
        resident_object.resident = request.user
        resident_object.village_id = village_object.id
        resident_object.charaset = village_object.charaset
        resident_object.icon_url = getCharacterImgURL(resident_object.charaset, resident_object.character)
        resident_object.save()
        return True
    else:
        return False

def startPost(request,village_object):
    start_form = StartForm(data=request.POST)
    if start_form.is_valid():
        village_object.nightflag = 1
        village_object.startflag = 1
        village_object.started_date = timezone.now()
        village_object.save()
        # 参加者に役職を振り分ける
        # 開始通知を出す
        return True
    else:
        return False

def votePost(request,village_object):
    vote_form = ExecuteForm(data=request.POST,village_object=village_object)
    if vote_form.is_valid():
        vote_object = vote_form.save(commit=False)
        vote_object.village_id = village_object.id
        vote_object.executer_id = request.user.id
        vote_object.execute_type = 'vote'
        vote_object.day = village_object.day
        vote_object.save()
        return True
    else:
        return False

def villageUpdate(village_object):
    village_object.updated_date = timezone.now()
    village_object.day += village_object.nightflag
    village_object.nightflag = 1 - village_object.nightflag
    village_object.save()

def executeVote(village_object):
    alive_resident_objects = getAliveResidentObjects(village_id=village_object.id)
    execute_objects = getExecuteObjects(village_object=village_object)
    votes = defaultdict(int)
    targets = {}
    for resident in alive_resident_objects:
        execute_object,is_created = execute_objects.get_or_create(
            executer=resident,
            defaults={
                'village':village_object,
                'target':choice(alive_resident_objects),
                'execute_type':'vote',
                'day':village_object.day,
            }
        )
        votes[execute_object.target] += 1
        targets[execute_object.executer] = execute_object.target
    Remark(
        village = village_object,
        remarker_id = 1,
        day = village_object.day,
        nightflag = 0,
        remark_type = 'vote',
        remarker_name = resident.resident.username,
        character = resident.character,
        charaset = resident.charaset,
        icon_url = 'A.png',
        text = '投票を締め切りました。',
    ).save()
    for resident in alive_resident_objects:
        Remark(
            village = village_object,
            remarker = resident.resident,
            day = village_object.day,
            nightflag = 0,
            remark_type = 'vote',
            remarker_name = resident.resident.username,
            character = resident.character,
            charaset = resident.charaset,
            icon_url = getCharacterImgURL(resident.charaset,resident.character),
            text = "投票先：{0}\n得票数：{1}".format(targets[resident],votes[resident]),
        ).save()
    Remark(
        village = village_object,
        remarker_id = 1,
        day = village_object.day,
        nightflag = 0,
        remark_type = 'vote',
        remarker_name = resident.resident.username,
        character = resident.character,
        charaset = resident.charaset,
        icon_url = 'A.png',
        text = '{}が処刑されましたが、\n不思議な力で生き返りました。'.format('a19th'),
    ).save()

# 参加者の更新
def residentUpdate(village_object):
    if village_object.nightflag == 0:
        executeVote(village_object=village_object) #投票
    else:
        pass
        # executeRevelation(village_object=village_object) #占い
        # executeNecropsy(village_object=village_object) #霊能
        # executeEscort(village_object=village_object) #護衛
        # executeMurder(village_object=village_object) #襲撃

# フォームとレコードを渡す
def getVillageContext(request,village_object,next_update_time):
    context = {
        'start_form'   : StartForm(),
        'remark_form'  : RemarkForm(),
        'resident_form': ResidentForm(village_object=village_object),
        'execute_form' : ExecuteForm(village_object=village_object),
        'remark_list'  : getRemarkObjects(village_object=village_object)[:100],
        'resident_list': getResidentObjects(village_id=village_object.id),
        'village_info' : village_object,
        'status_turn'  : '夜' if village_object.nightflag else '昼',
        'is_started'   : bool(village_object.startflag),
        'update_time'  : next_update_time
    }
    # 参加者か否かで渡すcontextを変える
    try:
        context['residentinfo'] = context['resident_list'].get(resident=request.user)
        context['status_death'] = '死亡' if context['residentinfo'].deathflag else '生存'
        context['job'] = context['residentinfo'].job
        context['isAuther'] = village_object.auther == request.user
        context['icon_url'] = context['residentinfo'].icon_url
        context['isResident'] = True
    except:
        context['icon_url'] = village_object.icon_url
        context['isResident'] = False
    try:
        context['vote_object'] = Execute.objects.get(
            village = village_object,
            executer_id = request.user.id,
            execute_type = 'vote',
            day = village_object.day
        )
    except:
        context['vote_object'] = False
    return context

# 村を作成
def createVillage(request,form):
    form.instance.auther = request.user
    form.instance.auther_name = request.user.username
    form.instance.charaset_name = getCharacterName(form.cleaned_data['charaset'])
    form.instance.icon_url = getRandomCharacterImgURL(form.cleaned_data['charaset'])
