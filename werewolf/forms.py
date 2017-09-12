from django import forms
from .models import Village, Remark

class VillageForm(forms.ModelForm):
	class Meta:
		model = Village
		fields = ('name',)

class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
