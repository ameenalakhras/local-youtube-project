from django import forms


class UploadUrl(forms.Form):
    question = forms.CharField(
        label='',
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        super(UploadUrl, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['placeholder'] = 'Enter youtube video url here '
