from django import forms

from products.models import ProductCategory, Product
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User


class UserAdminRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Дата рождения'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    birthday = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control py-4', 'readonly': False}),
        required=False,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class ProductCategoryItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control py-4', 'readonly': False}),
        required=False
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'vCheckboxField', 'readonly': False}),
        required=False,
    )

    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')


class ProductItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'image', 'description', 'price', 'quantity', 'is_active')

    def __init__(self, *args, **kwargs):
        super(ProductItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'custom-file'
            elif field_name == 'is_active':
                field.widget.attrs['class'] = 'vCheckboxField'
            elif field_name == 'category':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'
