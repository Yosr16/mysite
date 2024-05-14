from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ProduitForm, CommandeForm, UserRegistrationForm, FournisseurForm
from .models import Produit, Fournisseur, Commande, Categorie
from .forms import UserRegistrationForm  # Importez le formulaire de création d'utilisateur personnalisé
from django.contrib.auth.models import User, auth
from . import serializers
from rest_framework import viewsets
from datetime import date

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 

from django.shortcuts import render, redirect, get_object_or_404
from .models import Fournisseur
from .forms import FournisseurForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Fournisseur
from .forms import FournisseurForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView


class Modifier_fournisseur(UpdateView):
    model = Fournisseur
    template_name = 'magasin/modifier_fournisseur.html'
    form_class = FournisseurForm
    success_url = reverse_lazy('fournisseur.html')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class SupprimerFournisseur(DeleteView):
    model = Fournisseur
    template_name = 'magasin/supprimer_fournisseur.html'
    success_url = reverse_lazy('liste_fournisseurs')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProduitSerializer

    def get_queryset(self):
        queryset = Produit.objects.all()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset

class ProduitAPIView(APIView):
    def get(self, request, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = serializers.ProduitSerializer(produits, many=True)
        return Response(serializer.data)

class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bases')  # Redirigez l'utilisateur vers la page de base après la connexion réussie
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authentification de l'utilisateur
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)  # Utilisez l'utilisateur authentifié pour la connexion
                messages.success(request, f'Bienvenue, {username} ! Votre compte a été créé avec succès.')
                return redirect('bases')  # Redirigez l'utilisateur vers la page 'base'
            else:
                messages.error(request, 'Erreur lors de l\'authentification.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def home(request):
    context = {'val': "Home Menu"}
    return render(request, 'home.html', context)
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
def index(request):
    template = 'magasin/mesProduits.html'
    products = Produit.objects.all()
    context = {'products': products}
    return render(request, template, context)

def create_produit(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/magasin')
    else:
        form = ProduitForm()
    return render(request, 'magasin/majProduits.html', {'form': form})

def vitrine(request):
    product_list = Produit.objects.all()
    return render(request, 'vitrine.html', {'list': product_list})

def commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CommandeForm()
    return render(request, 'magasin/commande.html', {'form': form})

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'magasin/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

def catalogue(request):
    products = Produit.objects.all()
    return render(request, 'magasin/catalogue.html', {'produits': products})

def mes_produits(request):
    produits = Produit.objects.all()
    return render(request, 'magasin/mesProduits.html', {'produits': produits})

def acheter_produit(request, produit_id):
    # Logique pour acheter un produit
    # Vous devez ajouter la logique pour gérer l'achat du produit ici
    return render(request, 'magasin/acheter_produit.html', context={'produit_id': produit_id})

def recherche(request):
    if 'q' in request.GET:
        query = request.GET['q']
        results = Produit.objects.filter(libelle__icontains=query)
        return render(request, 'magasin/recherche.html', {'results': results, 'query': query})
    else:
        return render(request, 'magasin/recherche.html')

def nouveauFournisseur(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FournisseurForm()
    return render(request, 'magasin/fournisseur.html', {'form': form})
def Conn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')  # Redirigez l'utilisateur vers la page de base après la connexion réussie
    else:
        form = AuthenticationForm()
    return render(request, 'authenticate/login.html', {'form': form})


from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render

def panier_view(request):
    # Récupérer le panier depuis la session de l'utilisateur
    cart = request.session.get('cart', [])

    # Calculer le total du panier
    total = 0
    for item in cart:
        total += item['prix'] * item['quantite']

    # Passer les détails du panier à la template
    context = {
        'cart': cart,
        'total': total
    }

    return render(request, 'magasin/panier.html', context)

from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        price = request.POST.get('price')
        # Ajoutez la logique pour ajouter le produit au panier
        # Assurez-vous de stocker les détails du produit dans la session utilisateur
        cart = request.session.get('cart', [])
        cart.append({'product_id': product_id, 'price': price})
        request.session['cart'] = cart
        request.session.save()  # Sauvegardez la session après avoir modifié les données du panier
        return redirect('votre_vue_du_catalogue')
    else:
        return HttpResponseBadRequest('Invalid request method')
    
from django.shortcuts import render

def view_cart(request):
    cart = request.session.get('cart', [])
    # Utilisez les données du panier pour afficher le contenu du panier dans le template
    context = {'cart': cart}
    return render(request, 'magasin/panier.html', context)

