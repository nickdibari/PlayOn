from django import forms


class PlayListForm(forms.Form):
    playlist_uri = forms.CharField(label='You playlist URI', max_length=100)