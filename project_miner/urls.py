"""project_miner URL Configuration

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
from django.contrib import admin
from django.urls import path, include
import home_app.views
import account_app.views
import product_app.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', home_app.views.searcher, name='search'),
    path('', home_app.views.index, name='homepage'),
    path('login/', account_app.views.login, name='login'),
    path('signup/', account_app.views.signup, name='signup'),
    path('logout/', account_app.views.logout, name='logout'),
    path('faq/', home_app.views.faq, name='FAQ'),
    path('about_us/', home_app.views.about, name='about'),
    path('err/', home_app.views.error, name='error'),
    path('', include('product_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
