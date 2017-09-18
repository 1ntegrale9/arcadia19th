from django import forms
from .models import Village, Remark, Resident

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('name','character')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = '村の名前を入力'
        self.fields['name'].widget.attrs['class']       = 'form-control'
        self.fields['character'].widget.attrs['class']  = 'form-control'
        self.fields['palflag'].widget.attrs['class']    = 'form-control'

    charaset = (
        ('rain','霧雨降る街'),
        ('rainBig','霧雨降る街(BIG)'),
        ('jewel','宝石箱《Jewel Box》'),
        ('ensou','演奏会'),
        ('free','フリーアイコン'),
    )
    character = forms.ChoiceField(widget=forms.Select, choices=charaset)
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