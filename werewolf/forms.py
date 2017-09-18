from django import forms
from .models import Village, Remark, Resident
from .charasetTable import getCharasetChoices

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('name','daytime_length','nighttime_length','character',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder']             = '村の名前を入力'
        self.fields['name'].widget.attrs['class']                   = 'form-control'
        self.fields['daytime_length'].widget.attrs['placeholder']   = '昼時間(秒)'
        self.fields['daytime_length'].widget.attrs['class']         = 'form-control'
        self.fields['nighttime_length'].widget.attrs['placeholder'] = '夜時間(秒)'
        self.fields['nighttime_length'].widget.attrs['class']       = 'form-control'
        self.fields['character'].widget.attrs['class']              = 'form-control'
        self.fields['palflag'].widget.attrs['class']                = 'form-control'

    character = forms.ChoiceField(widget=forms.Select, choices=getCharasetChoices())
    palflag = forms.ChoiceField(widget=forms.Select, choices=((0,'誰でも歓迎'),(1,'身内限定'),))

class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

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
