from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth import login, authenticate
from django.views.generic import RedirectView
from django.views.generic.list import ListView
from theme.models import Post, Comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from theme.forms import (
    PostModelCreat,
    CommentModelForm,
)


class PostListView(ListView):
    model = Post
    paginate_by = 6
    template_name = 'theme/indexList'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        query = self.request.GET.get('search_text')
        if query:
            return Post.objects.filter(post_title__icontains=search_text)
        else:
            return Post.objects.order_by('-view_count')
             


class RedirectLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        user = self.request.user
        url_ = post.get_absolute_url()
        if user.is_authenticated:
            if user in post.like_count.all():
                post.like_count.remove(user)
            else:
                post.like_count.add(user)
        return url_




def index(request):
    # if request.method == 'POST':
        # latest_post_list = Post.objects.filter(
            # post_title__icontains=request.POST['search_text'])
    # else:
        # latest_post_list = Post.objects.order_by('-view_count')

    latest_post_list =  Post.objects.order_by('-view_count')
    query = request.GET.get('q')
    if query:
        latest_post_list = Post.objects.filter(
            post_title__icontains=query)

    # search_text = request.GET.get('search_text')
    # if search_text:
    #     latest_post_list = Post.objects.filter(post_title__icontains=search_text)
    # else:
    #     latest_post_list = Post.objects.order_by('-view_count')
    paginator = Paginator(latest_post_list, 6)
    page = request.GET.get('page')

    if page is None:
        page = 1
    posts = paginator.page(page)



    context = {
        'posts': posts
    }
    return render(request, 'theme/index.html', context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentModelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and request.user:
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect(reverse('theme:detail', args=(slug,)))

    Post.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    post.view_count += 1

    comments = post.comment_set.order_by('-pub_date')
    context = {
        'post': post,
        'comment': comments,
        'form': form
    }
    return render(request, 'theme/detail.html', context)


@login_required(login_url='user:log_in')
def creat(request):
    form = PostModelCreat(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        try:
            post.slug = post.generate_slug()
            post.save()
        except:
            messages.error(request, 'post with this title is already exist')
            return redirect(reverse('theme:creat'))
        

        return redirect(reverse('theme:index'))
    context = {
        'form': form
    }
    return render(request, 'theme/creat_post.html', context)


@login_required(login_url='user:log_in')
def edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostModelCreat(request.POST or None, instance=post)
    if request.user == post.author:
        if request.POST and form.is_valid():
            form.save()
            return redirect(reverse('theme:detail', args=(slug,)))
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'theme/edit.html', context)
    return HttpResponseNotFound()


@login_required(login_url='user:log_in')
def delete_own_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect(reverse('theme:detail', args=(comment.post.slug,)))


@login_required(login_url='user:log_in')
def delete_own_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        messages.success(request, 'post delete successful')
        post.delete()
    return redirect(reverse('theme:index'))
