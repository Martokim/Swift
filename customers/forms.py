from django import forms

from customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your name'}),
            'admission_number': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter your admission number'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your email'}),
            'gender': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your gender'}),
            'age': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter your age'}),
            'image': forms.ClearableFileInput(attrs={
                'Class': 'form-control',
                'accept':'images/*',
                'title':'upload your image here'})


        }