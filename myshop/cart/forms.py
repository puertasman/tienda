from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=[], coerce=int, label="Cantidad")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        max_quantity = kwargs.pop('max_quantity', 0)  # Extraer max_quantity antes de super
        print(max_quantity)
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        if max_quantity > 0:
            quantity_choices = [(i, str(i)) for i in range(1, min(max_quantity + 1, 11))]
            self.fields['quantity'].choices = quantity_choices
        else:
            self.fields['quantity'].choices = [(0, "Sin disponibilidad")]
            self.fields['quantity'].disabled = True