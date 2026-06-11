from django import forms
from .models import SoilData

class SoilDataForm(forms.ModelForm):
    class Meta:
        model = SoilData
        fields = [
            'nitrogen',
            'phosphorus',
            'potassium',
            'ph',
            'rainfall',
            'location'
        ]

    def clean_nitrogen(self):
        val = self.cleaned_data['nitrogen']
        if val < 0 or val > 200:
            raise forms.ValidationError("Nitrogen must be between 0 and 200.")
        return val

    def clean_phosphorus(self):
        val = self.cleaned_data['phosphorus']
        if val < 0 or val > 200:
            raise forms.ValidationError("Phosphorus must be between 0 and 200.")
        return val

    def clean_potassium(self):
        val = self.cleaned_data['potassium']
        if val < 0 or val > 200:
            raise forms.ValidationError("Potassium must be between 0 and 200.")
        return val

    def clean_ph(self):
        val = self.cleaned_data['ph']
        if val < 0 or val > 14:
            raise forms.ValidationError("pH must be between 0 and 14.")
        return val

    def clean_rainfall(self):
        val = self.cleaned_data['rainfall']
        if val < 0 or val > 5000:
            raise forms.ValidationError("Rainfall must be between 0 and 5000 mm.")
        return val