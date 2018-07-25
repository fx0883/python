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

urlpatterns = [
    path("pageIndex/<int:pageIndex>/pageSize/<int:pageSize>",views.getNovelList,name='getNovelList'),
    path("keyword/<str:keyword>/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>",views.searchNovelList,name='searchNovelList'),
    path("bookid/<str:bookid>/chapterid/<str:chapterid>", views.getChapterById,name='getChapterById'),
    path("bookid/<str:bookid>/chapterStartNumber/<int:chapterStartNumber>/chapterEndNumber/<int:chapterEndNumber>", views.getChapterList, name='getChapterList'),
    path("categoryName/<str:categoryName>/pageIndex/<int:pageIndex>/pageSize/<int:pageSize>", views.getCategoryNovelList, name='getCategoryNovelList'),
]
