from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blogapp.forms import ArticleForm, CommentForm
from blogapp.models import Article

home_page = 'blogapp:home'
login_page = 'blogapp:login'
detail_article_page = 'blogapp:detail_article'

create_modify_article_html = 'blogapp/create_modify_article.html'

# Create your views here.
@require_http_methods(["GET"])
def home_view(request):
    articles = Article.objects.all().order_by('-created_at')
    paginator = Paginator(articles, 5)  # Show 5 articles per page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {'articles': articles} # Retrieve all articles ordered by creation date (newest first)
    return render(request, 'blogapp/index.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect(login_page)  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(home_page)  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'blogapp/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST': 
       logout(request)
       return redirect(home_page)
    logout(request)
    return redirect(login_page)  # Redirect to the login page after logout


@login_required
def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.autor = request.user
            new_article.save()

            return redirect(detail_article_page, pk=new_article.pk)  # Redirect to the article detail page after successful creation
        else:
            form = ArticleForm(request.POST)  # Reinitialize the form with the submitted data to display errors
            return render(request, create_modify_article_html, {'form': form, 'action': 'create'})
    
    return render(request, create_modify_article_html, {'action': 'create'})


def detail_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm() # Retrieve all comments related to the article
    context = {'article': article, 'comment_form': comment_form}
    return render(request, 'blogapp/detail_article.html', context)


def modify_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.autor:
        return redirect(detail_article_page, pk=article.pk)  # Redirect to the article detail page if the user is not the author

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect(detail_article_page, pk=article.pk)  # Redirect to the article detail page after successful modification
    else:
        form = ArticleForm(instance=article)
    
    context = {'form': form, 'action': 'modify', 'article': article}

    return render(request, create_modify_article_html, context)


@login_required
def delete_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.autor:
        return redirect(detail_article_page, pk=article.pk)  # Redirect to the article detail page if the user is not the author

    if request.method == 'POST':
        article.delete()
        return redirect(home_page)  # Redirect to the home page after successful deletion

    context = {'article': article}
    return render(request, 'blogapp/delete_article.html', context)


def add_comment_view(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if article.autor == request.user:
       # On pourrait afficher un message d'erreur avec django.contrib.messages
       # Pour la simplicité "bébé", on redirige simplement sans rien faire.
       return redirect('blogapp:detail_article', pk=article.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.autor = request.user
            new_comment.save()
            return redirect(detail_article_page, pk=article.pk)  # Redirect to the article detail page after successful comment submission
    else:
        form = CommentForm()

    context = {'form': form, 'article': article}
    return render(request, 'blogapp/detail_article.html', context)


def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    articles = Article.objects.filter(autor=user).order_by('-created_at')
    context = {'user': user, 'articles': articles}
    return render(request, 'blogapp/user_profile.html', context)