from django import forms


class SignupForm(forms.Form):
    id = forms.CharField(label="Id", required=True)
    name = forms.CharField(label="Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", required=True)
    phone_num = forms.CharField(label="Phone Number", required=True)


class LoginForm(forms.Form):
    phone_num = forms.CharField(label="Phone Number", required=True)
    password = forms.CharField(label="Password", required=True)


class SearchForm(forms.Form):
    phone_num = forms.CharField(label="Phone Number", required=True)


class SetPasswordForm(forms.Form):
    password = forms.CharField(label="Password", required=True)
