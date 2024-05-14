from django.urls import path, include  # Importez include pour inclure les URLs d'authentification
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.conf import settings  # Importez les paramètres Django
from django.conf.urls.static import static  # Importez static pour les fichiers média
from .views import CategoryAPIView
from .views import ProduitAPIView
from . import views
from .views import Modifier_fournisseur
from .views import SupprimerFournisseur
from django.urls import path
from . import views
urlpatterns = [    
    path('', views.index, name='index'),

    
    path('panier/', views.panier_view, name='panier'),
    path('vitrine/', views.vitrine, name='vitrine'),
    path('create_produit/', views.create_produit, name='create_produit'),
    path('commande/', views.commande, name='commande'),
    path('recherche/', views.recherche, name='recherche'),
    path('fournisseur/', views.nouveauFournisseur, name='nouveauFour'),
    
    path('api/category/', CategoryAPIView.as_view()),
    path('api/produits/', ProduitAPIView.as_view()),
    path('api/produit/<int:category_id>', ProduitAPIView.as_view()),

    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('magasin/', views.mes_produits, name='magasin'),
    path('acheter/<int:produit_id>/', views.acheter_produit, name='acheter_produit'),
    path('<int:pk>/supprimer_fournisseur/', SupprimerFournisseur.as_view(), name='supprimer_fournisseur'),
    
    path('<int:pk>/modifier_fournisseur/', Modifier_fournisseur.as_view(), name='modifier_fournisseur'),
    path('logout', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),  
    path('register/', views.register, name='register'), 
    path('connexion/',views.Conn, name='Conn'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
