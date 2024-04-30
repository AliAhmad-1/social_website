from django import forms
from .models import Post,Comment
class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4,'placeholder':"What's happening?"}), 
     
        }

