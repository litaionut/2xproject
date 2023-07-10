from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Step, UserProfile
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class StepForm(forms.ModelForm):
    unit_number = forms.FloatField(
        label="Unit Number",
        widget=forms.NumberInput(attrs={'step': 'any', 'required': True})
    )
    def clean_unit_number(self):
        unit_number = self.cleaned_data['unit_number']
        if unit_number == 0:
            raise forms.ValidationError("Unit number cannot be zero.")
        return unit_number
    class Meta:
        model = Step
        fields = ['step_title', 'step_description', 'unit_number']
    