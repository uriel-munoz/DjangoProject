from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )