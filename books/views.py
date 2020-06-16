from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Articles, Profile, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import ArticleForm, AuthUserForm, RegisterUserForm, CommentForm, UserForm, ProfileForm, TagForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class HomeListView(ListView):
    model = Articles
    template_name = 'books/post.html'
    context_object_name = 'list_articles'


class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Articles
    template_name = 'books/post_page.html'
    context_object_name = 'get_article'
    form_class = CommentForm
    success_msg = 'Комментарий добавлен'

    def get_success_url(self):
        return reverse_lazy('detail_page', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def post(self, request, *args, **kwargs):
    # form = self.get_form()
    form = ArticleForm(request.POST, request.FILES)
    if form.is_valid():
        return self.form_valid(form)
    else:
        return self.form_invalid(form)


class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = Articles
    template_name = 'books/edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись создана '

    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by("-date")[:20]
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Articles
    template_name = 'books/edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись успешно обновлена'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    template_name = 'books/edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись удалена'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class FishingLoginView(LoginView):
    template_name = 'books/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit_page')

    def get_success_url(self):
        return self.success_url


class FishingRegisterView(CreateView):
    model = User
    template_name = 'books/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Успешная регистрация'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class FishingLogoutView(LogoutView):
    next_page = 'news_page'


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            if 'profile_avatar' in request.FILES:
                profile_form.photo = request.FILES['profile_avatar']
            user_form.save()
            profile_form.save()
            messages.success(request, ('Профиль успешно обновлен'))

            return HttpResponseRedirect(reverse_lazy('edit_page'))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'books/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'books/profile_page.html'
    context_object_name = 'get_profile'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.get_object().id})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'books/tag_page.html', context={'tags': tags})


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'books/tag_detail.html', context={'tag': tag})


class TagCreate(View):

    def get(self, request):
        form = TagForm()
        return render(request, 'books/tag_create.html', context={'form': form})

    def post(self, request):
        bound_form = TagForm(request.POST)
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'books/tag_create.html', context={'form': bound_form})


class TagUpdate(View):

    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form= TagForm(instance=tag)
        return render(request, 'books/tag_update.html', context={'form': bound_form, 'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(request.POST, instance=tag)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'books/tag_update.html', context={'form': bound_form, 'tag': tag})


class TagDelete(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        return render(request, 'books/tag_delete.html', context={'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        tag.delete()
        return redirect(reverse('tags_page'))
