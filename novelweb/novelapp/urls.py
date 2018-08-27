"""novelweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from . import wapview
from . import mangaview

urlpatterns = [
    path("novelList/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>", views.getNovelList, name='getNovelList'),
    path("searchNovelList/keyword/<str:keyword>/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>",
         views.searchNovelList, name='searchNovelList'),
    path("bookid/<str:bookid>/chapterid/<str:chapterid>", views.getChapterById, name='getChapterById'),
    path("bookid/<str:bookid>/chapterStartNumber/<int:chapterStartNumber>/chapterEndNumber/<int:chapterEndNumber>",
         views.getChapterList, name='getChapterList'),
    path("categoryName/<str:categoryName>/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>",
         views.getCategoryNovelList, name='getCategoryNovelList'),

    path("wap", wapview.index, name='index'),
    path("wap/getNovelInfo/bookid/<str:bookid>", wapview.getNovelInfo, name='getNovelInfo'),
    path("wap/getChapterInfo/bookid/<str:bookid>/chapterid/<str:chapterid>", wapview.getChapterInfo,
         name='getChapterInfo'),
    path("wap/search", wapview.search, name='search'),


    path("mangaList/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>", mangaview.getMangaList, name='getMangaList'),
    path("searchMangaList/keyword/<str:keyword>/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>",
         mangaview.searchMangalList, name='searchMangalList'),
    path("mangaid/<str:mangaid>/chapterid/<str:chapterid>", mangaview.getMangaChapterById, name='getMangaChapterById'),
    path("manage/categoryName/<str:categoryName>/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>",
         mangaview.getCategoryMangaList, name='getCategoryMangaList'),
]
