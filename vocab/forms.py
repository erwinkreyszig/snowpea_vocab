from django import forms
from .models import Language

# language_choices =


class MainForm(forms.Form):
    date_added = forms.DateField(
        label="Date",
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "Date", "ari-label": "Date", "readonly": "readonly"}
        ),
        required=True,
    )
    word_or_phrase = forms.CharField(
        label="Word/Phrase",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    language = forms.CharField(
        label="Language",
        widget=forms.Select(
            attrs={"class": "form-control"}, choices=list(Language.objects.values_list("code", "desc"))
        ),
        required=True,
    )
    pronounciation = forms.CharField(
        label="Pronounciation",
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    is_native = forms.BooleanField(
        label="Is native?",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}, choices=((False, "No"), (True, "Yes"))),
    )
