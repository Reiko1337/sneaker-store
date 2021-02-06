from django import forms
from .models import Size


class SizeForm(forms.ModelForm):
    size = forms.CharField(widget=forms.CheckboxInput())

    class Meta:
        model = Size
        fields = ('size',)


SizeFormSet = forms.modelformset_factory(Size, form=SizeForm, extra=0)
