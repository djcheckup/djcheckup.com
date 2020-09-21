from django import forms


class URLSubmitForm(forms.Form):
    url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter the full URL for your Django site. (required)",
                "autofocus": "autofocus",
                "tabindex": "1",
            }
        ),
    )
