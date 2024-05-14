from django.urls import path
from django.contrib.auth.decorators import login_required  # Importez login_required depuis django.contrib.auth.decorators
from . import views
from django.contrib.auth import views as auth_views 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('post_create/', views.PostCreate.as_view(), name='post_create'),  
    path('blog/post/<int:pk>/modifpost/', views.ModifPost.as_view(), name='modifpost'),
    path('blog/<int:pk>/supprimer/', views.deletPost.as_view(), name='supppost'), 
    path('login/', views.user_login, name='login'),  # Ajoutez l'URL pour la vue de connexion
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]


