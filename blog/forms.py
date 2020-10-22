from django import forms
from . import models

# codestart:SearchForm
class SearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id':'search-keyword',
            'class':'form-control',
        })
    )
# codeend:SearchForm

# codestart:CommentForm
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['status'].choices = models.CommentStatus.get_choices()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Comment
        fields = ('name_text', 'comment_text', 'status')
# codeend:CommentForm
