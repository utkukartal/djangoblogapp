"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings            # Bu
from django.conf.urls.static import static  # ve bu file upload için eklendi
from article import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = "index"),  # Urllerimze isimler verebiliriz, bu sayede redirect işlemini rahat bir şekilde gerçekleştirebiliriz.
    path('about/', views.about, name = "about"),
    path('articles/', include("article.urls")),  # İlk olarak localhost:8000/articles/ geldiğinde bu urls.py de path aranacak ve bu komut ile karşılaşılacak, biz bu dosyada bu path ile gelenleri bir nevi article'ın altındaki urls.py dosyasına yönlendiriyoruz.
    path('user/', include("user.urls")),  # Yukarıdaki gibi user ile başlayan urlleri user urls.py ye bağlıyor
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # File upload için
