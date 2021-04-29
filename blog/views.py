from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView
from django import urls


from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostList(generic.TemplateView):
    template_name = "blog/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().prefetch_related("comments")
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self, **kwargs):
        post_id = self.kwargs['pk']
        queryset = Post.objects.filter(id=post_id).prefetch_related("comments")
        return queryset


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


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class CommentNewView(CreateView):
    model = Comment
    template_name = 'blog/new_comment.html'
    fields = ['text', 'created_by']
    # success_url = reverse_lazy(PostList)

    def form_valid(self, form, **kwargs):
        comment = form.save(commit=False)
        post_id = self.kwargs['post_id']
        comment.published_date = timezone.now()
        comment.post_id = post_id
        comment.save()
        return HttpResponseRedirect('/')
