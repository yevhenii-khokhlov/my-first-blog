from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.db.models import Prefetch
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment
from .forms import PostForm, SignUpUserForm


def sign_up_request(request):
    if request.method == "POST":
        form = SignUpUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post-list")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = SignUpUserForm
    return render(request=request, template_name="blog/sign_up.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("post-list")
            messages.error(request, "Invalid username or password.")
        messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": form})


@login_required()
def logout_request(request):
    logout(request)
    return redirect("post-list")


@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def about(request):
    return render(request, 'blog/about.html', {})


class PostList(generic.TemplateView):
    template_name = "blog/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().prefetch_related("comments").order_by('-created_date')
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self, **kwargs):
        post_id = self.kwargs['pk']
        queryset = Post.objects.filter(id=post_id) \
            .prefetch_related(Prefetch("comments", queryset=Comment.objects.order_by('-created_date')))
        return queryset


class CommentNewView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'login'
    model = Comment
    template_name = 'blog/new_comment.html'
    fields = ['text']

    def form_valid(self, form, **kwargs):
        comment = form.save(commit=False)
        post_id = self.kwargs['post_id']
        comment.published_date = timezone.now()
        comment.post_id = post_id
        comment.created_by = self.request.user.username
        comment.save()
        return HttpResponseRedirect('/')
