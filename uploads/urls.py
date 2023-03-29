from django.urls import path
from .views import upload,home,index,login,dashboard
from .views import upload,home
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('upload/',upload,name="upload"),
    path('',home,name="home"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('data/',views.DatasetView.as_view(),name="dataset")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)