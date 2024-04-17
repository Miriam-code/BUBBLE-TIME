from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Nom', max_length=100, required=True)
    last_name = forms.CharField(label='Prénom', max_length=100, required=True)
    email = forms.EmailField(label='Email', max_length=254, required=True)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput, required=True)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # Vérification si les mots de passe correspondent
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return confirm_password
