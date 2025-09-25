from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
from datetime import date

class ConsultationForm(forms.Form):
    clinic_name = forms.CharField(
        max_length=100, 
        required=True,
        error_messages={
            'required': 'Clinic name is required.',
            'max_length': 'Clinic name cannot exceed 100 characters.'
        }
    )
    clinic_logo = forms.ImageField(
        required=True,
        error_messages={
            'required': 'Clinic logo is required.'
        }
    )
    physician_name = forms.CharField(
        max_length=100, 
        required=True,
        error_messages={
            'required': 'Physician name is required.',
            'max_length': 'Physician name cannot exceed 100 characters.'
        }
    )
    physician_contact = forms.CharField(
        max_length=10, 
        min_length=10,
        required=True,
        error_messages={
            'required': 'Physician contact is required.',
            'max_length': 'Contact must be 10 digits.',
            'min_length': 'Contact must be 10 digits.'
        }
    )
    patient_first_name = forms.CharField(
        max_length=50,
        required=True,
        error_messages={
            'required': 'Patient first name is required.',
            'max_length': 'First name cannot exceed 50 characters.'
        }
    )
    patient_last_name = forms.CharField(
        max_length=50,
        required=True,
        error_messages={
            'required': 'Patient last name is required.',
            'max_length': 'Last name cannot exceed 50 characters.'
        }
    )
    patient_contact = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        error_messages={
            'required': 'Patient contact is required.',
            'max_length': 'Contact must be 10 digits.',
            'min_length': 'Contact must be 10 digits.'
        }
    )
    patient_dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        error_messages={
            'required': 'Patient date of birth is required.',
            'invalid': 'Enter a valid date.'
        }
    )
    chief_complaint = forms.CharField(
        widget=CKEditorWidget(config_name='default'),
        required=True,
        error_messages={'required': 'Chief complaint is required.'}
    )
    consultation_note = forms.CharField(
        widget=CKEditorWidget(config_name='default'),
        required=True,
        error_messages={'required': 'Consultation note is required.'}
    )

    # Custom field validations
    def clean_patient_dob(self):
        dob = self.cleaned_data.get('patient_dob')
        today = date.today()
        if dob > today:
            raise ValidationError("Date of Birth cannot be in the future.")
        return dob

    def clean_physician_contact(self):
        contact = self.cleaned_data.get('physician_contact')
        if not contact.isdigit():
            raise ValidationError("Physician contact must contain only digits.")
        return contact

    def clean_patient_contact(self):
        contact = self.cleaned_data.get('patient_contact')
        if not contact.isdigit():
            raise ValidationError("Patient contact must contain only digits.")
        return contact

    def clean_clinic_logo(self):
        image = self.cleaned_data.get('clinic_logo')

        if not image:
            raise ValidationError('Clinic logo is required.')

        if not image.content_type.startswith('image/'):
            raise ValidationError('Uploaded file must be an image.')

        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if image.content_type not in allowed_types:
            raise ValidationError('Image must be JPEG, PNG, or GIF format.')

        # Optional: restrict file size (e.g., max 2MB)
        max_size = 2 * 1024 * 1024  # 2MB
        if image.size > max_size:
            raise ValidationError('Image file size must be under 2MB.')

        return image
