from django import forms
from .models import Village, Remark, Resident
from .charasetTable import getCharasetChoices

def generateChoiceField(choices):
    return forms.ChoiceField(widget=forms.Select, choices=choices)

def getVillageFormfields():
    return ['name','daytime_length','nighttime_length','character','palflag',]
def getVillageFormDisplayTable():
    return {
        'name':'村の名前を入力',
        'daytime_length':'昼時間(秒)',
        'nighttime_length':'夜時間(秒)',
    }
class VillageForm(forms.ModelForm):

    class Meta:
        model = Village
        fields = getVillageFormfields()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in getVillageFormfields():
            self.fields[f].widget.attrs['class'] = 'form-control'
        for f,s in getVillageFormDisplayTable().items():
            self.fields[f].widget.attrs['placeholder'] = s

    character = generateChoiceField(getCharasetChoices())
    palflag = generateChoiceField(([0,'誰でも歓迎'],[1,'身内限定'],))

class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'rows': 3}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'form-control'

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ('character',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['character'].widget.attrs['class'] = 'form-control'
        self.fields['character'].widget.attrs['placeholder'] = 'キャラクターを選択'

    character = forms.ChoiceField(widget=forms.Select)

class StartForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ()
