from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Blog,Posts,Comments


# from models import User #you can use get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth import forms
from django.contrib import admin


class UserCreationForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
    email=forms.EmailField()
    class Meta(UserCreationForm.Meta):
        model=User
        fields = UserCreationForm.Meta.fields + ( 'email',)


class UserSignupForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=Blog
        fields = ()


class UserLoginForm(forms.Form):
    email=forms.CharField(max_length=300,label='email',widget= forms.TextInput
                           (attrs={'placeholder':'Full Name'}))
    password=forms.CharField(label="password",max_length=32, widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['Email','Password']

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields = ['username','email']

class UserBlogUpdateForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ['Phone_Number','Profile_Picture','Status']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model=Posts
        exclude=['Likes','Remark','Date']
        fields = ['Title','Post','username']
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        exclude=['Likes','Date']
        fields = ['Comment','username','Post']

class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm

# admin.site.register(User)