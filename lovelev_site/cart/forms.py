from django import forms
from clothes.models import Product


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Количество',
                                      choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

    class Meta:
        model = Product
        fields = ['sizes']

    def __init__(self, pk, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        sizes = tuple(Product.objects.get(pk=pk).sizes)
        sizes_list = []
        for item in sizes:
            sizes_list.append((item, item))
        self.fields['sizes'] = forms.ChoiceField(choices=sizes_list, label='Размер',)

