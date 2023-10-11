from django.urls import path
from . import views
urlpatterns = [
    path('', views.login,name="home"),
    path('login', views.login,name="login"),
    path('register', views.register,name="register"),
    path('generator', views.generator,name="generator"),
    path('logout', views.logout,name="logout"),
    # path('forgot_password', views.forgot_pass,name="forgot_pass"),
    path('vault', views.vault,name="vault"),
    path('vault/delete=<id>', views.vault_delete,name="vault"),
    path('vault/update=<id>+<username>+<password>', views.vault_update,name="vault"),
]