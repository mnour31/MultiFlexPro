from django import forms
from .models import Shop  , Product  , ShippingAddress , Customer , Order , Review , Page , Categorie


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name' , 'logo' , 'bio' , 'lang' , 'template' ,'currency' ,'facebook' , 'instagram' , 'twitter' ,'linkedin','pinterest' , 'is_slider' , 'is_brands']


class ProductForm(forms.ModelForm):
    def __init__(self,request , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        shop = Shop.objects.get(user=self.request.user)
        self.fields['categorie'].queryset = Categorie.objects.filter(shop=shop)
    class Meta:
        model = Product
        fields = [
            'title',
            'categorie',
            'desc',
            'content',
            'price',
            'discount',
            'digital',
            'image',
        ]

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'address',
            'city',
            'state',
            'zipcode',
        ]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email']

class StatusOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping','delivery' , 'throwback']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','content' ]

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title','content' ]

class CategorieForm(forms.ModelForm):
    def __init__(self,request , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        shop = Shop.objects.get(user=self.request.user)
        self.fields['father'].queryset = Categorie.objects.filter(shop=shop , is_father=True)
    class Meta:
        model = Categorie
        fields = [
            'name',
            'father',
            'is_father',
            'img',
        ]