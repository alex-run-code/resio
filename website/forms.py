from django import forms
from .models import Hospital, Specialty, Service

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ('city', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Hospital.objects.none()