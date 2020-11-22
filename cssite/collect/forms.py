from django import forms
from django.contrib.auth.models import User
from .models import Account, Task, ParsedFile, Participation, MappingInfo


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class GradeForm(forms.ModelForm):
    pass_state = forms.BooleanField(required=False)
    class Meta:
        model = ParsedFile
        fields = ['grading_score', 'pass_state']
