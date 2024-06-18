from django import forms
from .models import Donor, BloodBank, BloodGroup
from datetime import date  # Import the date class from the datetime module

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'date_of_birth', 'weight', 'blood_group', 'location', 'disease', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        weight = cleaned_data.get("weight")
        disease = cleaned_data.get("disease")

        # Calculate age from date of birth
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - (
                (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
            )
            if age < 18:
                raise forms.ValidationError("Donor must be at least 18 years old.")
        
        # Check if the donor's weight is at least 50 kg
        if weight and weight < 50:
            raise forms.ValidationError("Donor must weigh at least 50 kg.")

        # Check if the donor has any diseases
        if disease:
            raise forms.ValidationError("Donor must not have any diseases.")
        
        return cleaned_data

class BloodBankForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        fields = ['name', 'location']  # Ensure this matches your BloodBank model

class BloodGroupForm(forms.ModelForm):
    class Meta:
        model = BloodGroup
        fields = ['blood_group_name', 'quantity_available']

BloodGroupFormSet = forms.inlineformset_factory(
    BloodBank,  # Parent model
    BloodGroup,  # Child model
    fields=['blood_group_name', 'quantity_available'],  # Correct field name
    extra=1,  # Number of extra forms
    can_delete=True  # Allow deletion of forms
)
