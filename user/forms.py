from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "Kullanıcı Adı:", max_length=20, min_length=3)
    password = forms.CharField(max_length = 20, label = "Parola:", widget = forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 20, min_length = 3, label = "Kullanıcı Adı:")
    password = forms.CharField(max_length = 20, min_length = 6, label = "Parola:", widget = forms.PasswordInput)
    confirm = forms.CharField(max_length = 20, label = "Paraloyı Doğrulayın:", widget = forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor!")
        
        values = {
            "username": username,
            "password": password
        }
        return values
