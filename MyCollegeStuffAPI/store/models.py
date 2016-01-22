from django.contrib.auth.models import User
from django.db import models
from django import forms

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields= ('first_name','last_name', 'email', 'password')




class Product(models.Model):
    """
    Product Info.
    """
    # User will enter dollar. Always use DecimalField
    price = models.DecimalField(decimal_places=2, max_digits=7)
    product = models.CharField(max_length=50)
    description = models.TextField()
    student = models.ForeignKey(User)

    def __str__(self):
        return self.product
