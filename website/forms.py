from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Question, Answer, Challenge

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'image']
        
        labels = {
        	'title': 'Questão',
			'body': 'Detalhes',
            'image': 'Imagem',
		}
        
        widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título', 'rows': 2}),
			'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto', 'rows': 5}),
		}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
        
        labels = {
			'body': 'Resposta',
		}
        
        widgets = {
			'body': forms.Textarea(attrs={'class': 'form-control', 'title': 'Resposta', 'placeholder': 'Texto', 'rows': 5}),
		}
        
class ChallengeAnswerForm(forms.Form):
    user_answer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resposta', 'maxlength': '255'})
    )
    
    def clean_user_answer(self):
        cleaned_data = self.cleaned_data
        user_answer = cleaned_data.get('user_answer')
        return user_answer