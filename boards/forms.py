from django import forms
from .models import Topic, Board, Post


class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows': 5, 'placeholder': 'What is in your mind?'}
		),
		max_length=4000,
		help_text='The max max length of the text is 4000'
	)

	class Meta:
			model = Topic
			fields = ['subject', 'message']


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['message', ]


'''
class NewBoardForm(forms.ModelForm):

	message = forms.CharField(
		widget=

	),
	"""docstring for NewBoardForm"""
	def __init__(self, arg):
		super(NewBoardForm, self).__init__()
		self.arg = arg
		'''