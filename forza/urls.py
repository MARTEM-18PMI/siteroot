from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.get_main, name="index"),
    path('inner', views.get_inner, name='inner'),
    path('tunings/<int:blog_id>', views.blog, name="blog_by_id"),
    path('tunings', views.get_tunings_list, name='tunings'),
    path('login', views.log_in, name="login"),
    path('signup', views.sign_up, name="signup"),
    path('logout', views.log_out, name="logout")
]

