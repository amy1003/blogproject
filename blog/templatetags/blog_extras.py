from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count
from blog.models import Category

register = template.Library()

# 最新文章
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=3):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


# 归档
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    data_list = Post.objects.datetimes('created_time', 'month', order='DESC')

    blog_dates_dict = {}  # 构造一个字典存放日期数据
    for blog_date in data_list:
        blog_count = Post.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    return {
        'blog_dates_dict': blog_dates_dict,
    }

#分类
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }

#标签云
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }


