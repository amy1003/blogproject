from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'blog'
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
    path('file/', views.file, name='file'),
    path('fileyear/<int:year>', views.fileyear, name='fileyear'),
    path('classification/', views.classification, name='classification'),
    path('classifica/<int:pk>', views.classifica, name='classifica'),
    path('tagfile/', views.tagfile, name='tagfile'),
    path('tagselect/<int:pk>', views.tagselect, name='tagselect'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

