from django import forms
from .models import Village, Remark, Resident
from .charasetTable import getCharasetChoices

def generateChoiceField(choices):
    return forms.ChoiceField(widget=forms.Select, choices=choices)
def applyFormControl(target, fields):
    for f in fields:
        target.fields[f].widget.attrs['class'] = 'form-control'
def applyPlaceholder(target, messages):
    for f,s in messages.items():
        target.fields[f].widget.attrs['placeholder'] = s

def getVillageFormfields():
    return ('name','daytime_length','nighttime_length','character','palflag',)
def getVillageFormPlaceholderTable():
    return {
        'name':'村の名前を入力',
        'daytime_length':'昼時間(秒)',
        'nighttime_length':'夜時間(秒)',
    }
def getPalflagChoices():
    return (
        (0,'誰でも歓迎'),
        (1,'身内限定'),
    )
class VillageForm(forms.ModelForm):

    class Meta:
        model = Village
        fields = getVillageFormfields()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, getVillageFormfields())
        applyPlaceholder(self, getVillageFormPlaceholderTable())

    character = generateChoiceField(getCharasetChoices())
    palflag = generateChoiceField(getPalflagChoices())

def getRemarkFormfields():
    return ('text',)
class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = getRemarkFormfields()
        widgets = {'text': forms.Textarea(attrs={'rows': 3}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, getRemarkFormfields())

def getResidentFormfields():
    return ('character',)
def getResidentPlaceholderTable():
    return {'character':'キャラクターを選択',}
class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = getResidentFormfields()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        applyFormControl(self, getResidentFormfields())
        applyPlaceholder(self, getResidentPlaceholderTable())

    character = forms.ChoiceField(widget=forms.Select)

class StartForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ()
