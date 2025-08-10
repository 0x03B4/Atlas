from django import forms
from django.contrib.auth.models import User
from .models import Student, Qualification

class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
    }))

    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
    }))
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
    }))

    current_year = forms.TypedChoiceField(
        coerce=int, empty_value=None, required=False,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 dropdown-arrow bg-white'})
    )

    current_semester = forms.TypedChoiceField(
        coerce=int, empty_value=None, required=False,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 dropdown-arrow bg-white'})
    )

    class Meta:
        model = Student
        fields = ['qualification', 'current_year', 'current_semester']
        widgets = {
            'qualification': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 dropdown-arrow bg-white'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
        
        self.fields['qualification'].queryset = Qualification.objects.all()
        self.fields['qualification'].empty_label = "Select a Qualification"
        self.fields['current_year'].choices = [('', 'Select Year')] + [(i, f'Year {i}') for i in range(1, 5)]
        self.fields['current_semester'].choices = [('', 'Select Semester')] + [(i, f'Semester {i}') for i in range(1, 3)]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email

    def save(self, commit=True):
        student = super().save(commit=False)
        
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        new_email = self.cleaned_data['email']
        if self.user.email != new_email:
            self.user.email = new_email
            self.user.username = new_email

        if commit:
            self.user.save()
            student.save()
        return student