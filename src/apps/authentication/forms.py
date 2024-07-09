from django import forms
from django.contrib.auth import authenticate


class SignInForm(forms.Form):
  login = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Matrícula ou e-mail'}))
  password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

  def clean(self):
    cleaned_data = super().clean()
    login = cleaned_data.get('login')
    password = cleaned_data.get('password')

    if not login or not password:
      raise forms.ValidationError('Por favor, preencha todos os campos.')
    return cleaned_data
  
  def save(self):
    credentials = authenticate(
      username=self.cleaned_data.get('login'),
      password=self.cleaned_data.get('password')
    )

    if not credentials:
      raise forms.ValidationError('Usuário ou senha inválidos.')
    
    return credentials
  
class SignUpForm(forms.Form):
  registration = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Matrícula'}))


  def save(self):
    pass