from django import forms
from seller.models import Product

class ImageForm(forms.ModelForm):
   class Meta:
      model=Product
      fields=['image']