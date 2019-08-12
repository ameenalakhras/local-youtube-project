from django import forms


class DownloadUrl(forms.Form):
    """A form for reveiving a url for a youtube video to download"""
    question = forms.CharField(
        label='',
        max_length=300,
    )

    def __init__(self, *args, **kwargs):
        super(DownloadUrl, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['placeholder'] = 'Enter youtube video url here '


class DownloadListUrl(forms.Form):
    """A form to receive a url for a youtube video list"""
    question = forms.CharField(
        label="",
        max_length=300,
    )

    def __init__(self, *args, **kwargs):
        super(DownloadListUrl, self).__init__(*args, **kwargs)
        self.fields["question"].widget.attrs["placeholder"] = "Enter youtube list URL to download"
