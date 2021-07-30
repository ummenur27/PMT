from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, ProjectItem


class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectDateForm(forms.Form):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProjectForm(forms.ModelForm):

    class Meta:
        widgets = {'start_date' : DateInput(), 'end_date' : DateInput()}
        model = Project
        fields = ('title', 'user', 'content', 'start_date', 'end_date')


class ProjectItemForm(forms.ModelForm):
    class Meta:
        widgets = {'start_date' : DateInput(), 'end_date' : DateInput()}
        model = ProjectItem
        fields = ('content', 'start_date', 'end_date')

class ProjectItemStatusForm(forms.ModelForm):
    class Meta:
        model = ProjectItem
        fields = ('status', )

# class UserProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('status', )
