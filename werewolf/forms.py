from django import forms

def generateSelectForm(choices):
    return forms.ChoiceField(widget=forms.Select, choices=choices)
def applyFormControl(target, fields):
    for f in fields:
        target.fields[f].widget.attrs['class'] = 'form-control'
def applyPlaceholder(target, messages):
    for f,s in messages.items():
        target.fields[f].widget.attrs['placeholder'] = s

class VillageForm(forms.ModelForm):
    class Meta:
        from .models import Village
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

    from .charasetTable import getCharasetChoices
    charaset = generateSelectForm(getCharasetChoices())
    palflag = generateSelectForm(getPalflagChoices())

class RemarkForm(forms.ModelForm):
    class Meta:
        from .models import Remark
        model = Remark
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'rows': 3}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, self.fields)

class ResidentForm(forms.ModelForm):
    class Meta:
        from .models import Resident
        model = Resident
        fields = ('character',)

    def __init__(self, village_object, *args, **kwargs):
        from .charasetTable import getCharacterTable
        super().__init__(*args, **kwargs)
        applyFormControl(self, self.fields)
        self.fields['character'].choices = getCharacterTable(village_object.charaset)

    character = forms.ChoiceField(widget=forms.Select)

class StartForm(forms.ModelForm):
    class Meta:
        from .models import Village
        model = Village
        fields = ()

def remarkPost(request,village_object):
    remark_form = RemarkForm(data=request.POST)
    if remark_form.is_valid():
        from .models import Resident
        from .charasetTable import getCharacterImgURL
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
        from .charasetTable import getCharacterImgURL
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
        from django.utils import timezone
        village_object.nightflag = 1
        village_object.startflag = 1
        village_object.started_date = timezone.now()
        village_object.save()
        return True
    else:
        return False

def villageUpdate(village_object):
    from django.utils import timezone
    village_object.updated_date = timezone.now()
    village_object.day += village_object.nightflag
    village_object.nightflag = 1 - village_object.nightflag
    village_object.save()

def executeVote(village_object):
    from .models import getAliveResidentObjects,getExecuteObjects
    getAliveResidentObjects(village_id=village_object.id)
    getExecuteObjects(village_object=village_object)    

def residentUpdate(village_object):
    if village_object.nightflag == 0:
        executeVote(village_object=village_object) #投票
    else:
        executeRevelation(village_object=village_object) #占い
        executeNecropsy(village_object=village_object) #霊能
        executeEscort(village_object=village_object) #護衛
        executeMurder(village_object=village_object) #襲撃

def getVillageContext(request,village_object,next_update_time):
    from .models import getRemarkObjects,getResidentObjects
    context = {
        'start_form'   : StartForm(),
        'remark_form'  : RemarkForm(),
        'resident_form': ResidentForm(village_object=village_object),
        'remark_list'  : getRemarkObjects(village_object=village_object)[:100],
        'resident_list': getResidentObjects(village_id=village_object.id),
        'village_info' : village_object,
        'update_time'  : next_update_time,
    }
    # クソ実装
    try:
        context['residentinfo'] = context['resident_list'].get(resident=request.user)
        context['isResident'] = True
        context['isAuther'] = village_object.auther == request.user
        context['notStarted'] = not bool(village_object.startflag)
        context['icon_url'] = context['residentinfo'].icon_url
    except:
        context['isResident'] = False
        context['notStarted'] = True
        context['icon_url'] = village_object.icon_url
    return context

def createVillage(request,form):
    from .charasetTable import getCharacterName,getRandomCharacterImgURL
    form.instance.auther = request.user
    form.instance.auther_name = request.user.username
    form.instance.charaset_name = getCharacterName(form.cleaned_data['charaset'])
    form.instance.icon_url = getRandomCharacterImgURL(form.cleaned_data['charaset'])
