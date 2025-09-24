from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
from datetime import date

class ConsultationForm(forms.Form):
    clinic_name = forms.CharField(max_length=100, required=True)
    clinic_logo = forms.ImageField(required=True)
    physician_name = forms.CharField(max_length=100, required=True)
    physician_contact = forms.CharField(max_length=10, required=True)
    patient_first_name = forms.CharField(max_length=50, required=True)
    patient_last_name = forms.CharField(max_length=50, required=True)
    patient_contact = forms.CharField(max_length=10, required=True)
    patient_dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chief_complaint = forms.CharField(widget=CKEditorWidget(config_name='default'), required=True)
    consultation_note = forms.CharField(widget=CKEditorWidget(config_name='default'), required=True)


    def clean_patient_dob(self):
        dob = self.cleaned_data.get('patient_dob')
        today = date.today()
        if dob > today:
            raise ValidationError("Date of Birth cannot be in the future.")
        return dob