from django import forms
from django.contrib.auth import authenticate


class SignInForm(forms.Form):
  login = forms.CharField(label='Login', max_length=100)
  password = forms.CharField(label='Senha', widget=forms.PasswordInput)

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