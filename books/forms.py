from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea
from .models import Articles, Comments, Profile, Tag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title', 'post', 'image_p', 'tags', 'writer')

    # tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices={'class': 'form-control'})
    widgets = {
        'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        # self.fields['text'].widget = Textarea(attrs={'rows': 5})


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

        labels = {
            'username': "Имя пользователя",
            'password': "Пароль",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields['username'].label = 'Имя пользователя'
            self.fields['password'].label = 'Пароль'
            self.fields[i].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': "Имя пользователя",
            'password': "Пароль",
        }
        help_texts = {
            'username': None,
            'password': "Пароль и Имя пользователя не должны быть более 150 символов и могут содержать только цифры, буквы, а также символы: @/./+/-/",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия",
            'email': "Email адрес",
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        birth_date = forms.DateField(widget=forms.SelectDateWidget)
        fields = ('bio', 'location', 'birth_date', 'profile_avatar')
        widgets = {
            'birth_date': DateInput()
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for i in self.fields:
                self.fields[i].widget.attrs['class'] = 'form-control'


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['tittle']
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['tittle'].lower()
            if new_slug == 'create':
                raise ValidationError('Slug не может быть создан')
            if Tag.objects.filter(slug__iexact=new_slug).count():
                raise ValidationError('Slug должен быть уникальным. "{}" уже существует'.format(new_slug))
            return new_slug


