from django import forms
from .models import *

class NewCommentpostForm(forms.ModelForm):

	class Meta:
		model = Commentposts
		fields = ['comment']
		
		
class NewArtForm(forms.ModelForm):
	class Meta:
		model = Art
		fields = [ 'title','description', 'pic', 'tags', 'category']
		
class NewCommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['comment']