from django import forms

class ContactForm(forms.Form):
    subject     = forms.CharField(max_length=100)
    message     = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))
    sender      = forms.EmailField()
    cc_myself   = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'filled-in', 'checked':'checked'}) , required=False)