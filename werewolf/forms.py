from django import forms
from .models import Remark

class RemarkForm(forms.ModelForm):

    class Meta:
        model = Remark
        fields = ('user', 'text')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
