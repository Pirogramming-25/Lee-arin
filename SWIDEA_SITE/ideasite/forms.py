from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Idea

class IdeaRegisterForm(forms.ModelForm):    # modelfrom) devtool이 foreignkey인걸 앎
    class Meta:
        model = Idea
        fields = ['image', 'title', 'interest', 'content', 'devtool']
