from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
import markdown,re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.contrib import messages
from django.db.models import Q
import django.utils.timezone as timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list= paginator.page(page)
    except PageNotAnInteger:
        post_list= paginator.page(1)
    except EmptyPage:
        post_list= paginator.page(paginator.num_pages)

    tag_list = {}
    for post in post_list:
        tag_list[post] = post.tags.all()
    return render(request, 'blog/index.html',context={'post_list': post_list,'tag_list': tag_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk= pk)
    post_list = Post.objects.filter(category= cate).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context= {'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list})

def search(request):
    search = request.GET.get('search')
    if not search:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', {'post_list': post_list})


def about(request):
    return render(request, 'blog/about.html')


def file(request):
    date_list = Post.objects.datetimes('created_time', 'year', order='DESC')
    year_max = timezone.now().year
    post_list = Post.objects.filter(created_time__year=year_max).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    tag_list = {}
    for post in post_list:
        tag_list[post] = post.tags.all()
    return render(request,'blog/file.html',{'date_list': date_list,'post_list':post_list,'tag_list': tag_list})

def fileyear(request,year):
    post_list = Post.objects.filter(created_time__year=year).order_by('-created_time')
    date_list = Post.objects.datetimes('created_time', 'year', order='DESC')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/file.html', context={'date_list': date_list,'post_list': post_list})

def classification(request):
    category_list = Category.objects.all()
    first_category = Category.objects.first()
    post_list = Post.objects.filter(category=first_category).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'blog/classification.html',{'category_list': category_list,'post_list':post_list})

def classifica( request, pk):
    cate = get_object_or_404(Category, pk=pk)
    category_list = Category.objects.all()
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/classification.html', context={'post_list': post_list,'category_list':category_list})


def tagfile(request):
    tag_list = Tag.objects.all()
    first_tag = Tag.objects.first()
    post_list = Post.objects.filter(tags=first_tag).order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/tagfile.html', {'tag_list': tag_list,'post_list': post_list})

def tagselect(request,pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    tag_list = Tag.objects.all()
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/tagfile.html', context={'post_list': post_list,'tag_list':tag_list})




















