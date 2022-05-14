from django import forms
from .models import Board
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class BoardWriteForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={"placeholder": "Title of Contents"},
        ),
        required=True,
    )

    contents = SummernoteTextField()

    options = (
        ("Python", "Python Board"),
        ("JavaScript", "JavaScript Board"),
    )

    board_name = forms.ChoiceField(
        label="Choose Board",
        widget=forms.Select(),
        choices=options,
    )

    field_order = [
        "title",
        "board_name",
        "contents",
    ]

    class Meta:
        model = Board
        fields = [
            "title",
            "contents",
            "board_name",
        ]
        widgets = {
            "contents": SummernoteWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title", "")
        contents = cleaned_data.get("contents", "")
        board_name = cleaned_data.get("board_name", "Python")

        if title == "":
            self.add_error("title", "Please fill in the title.")
        elif contents == "":
            self.add_error("contents", "Please write contents.")
        else:
            self.title = title
            self.contetns = contents
            self.board_name = board_name
