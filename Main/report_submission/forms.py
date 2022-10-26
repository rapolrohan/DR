from django import forms
from .models import Patient_Report
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PatientForm(forms.ModelForm):
    
    class Meta:
        model = Patient_Report
        fields = ['patient_name', 'mobile_no', 'weight', 'years_diabetes', 'leftRetina', 'rightRetina']
        
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user