from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, CreateView, ListView, DetailView,DeleteView
from django.urls import reverse_lazy
from .models import Poste
from .forms import PostForm
from django.contrib.auth.models import User, auth
from rest_framework import viewsets
from datetime import date
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required


class PostCreate(CreateView):
    # Définition de la vue pour créer un poste
    model = Poste
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')  # URL de redirection après la création du poste

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostList(ListView):
    # Vue pour afficher la liste des postes
    model = Poste
    template_name = 'post_list.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    # Vue pour afficher les détails d'un poste
    model = Poste
    template_name = 'post_detail.html'

class ModifPost(UpdateView):
    # Vue pour modifier un poste existant
    model = Poste
    template_name = 'modifpost.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

class deletPost(DeleteView):
    # Vue pour supprimer un poste
    model=Poste
    template_name='supppost.html'
    success_url = reverse_lazy('post_list')

def user_login(request):
    # Vue pour gérer l'authentification de l'utilisateur
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')  # Rediriger vers la page de base après la connexion réussie
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def home(request):
    # Vue pour la page d'accueil
    context = {'val': "Home Menu"}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def user_logout(request):
    # Vue pour gérer la déconnexion de l'utilisateur
    auth.logout(request)
    return redirect('login')

def register(request):
    # Vue pour gérer l'enregistrement des utilisateurs
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authentification de l'utilisateur
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f'Bienvenue, {username} ! Votre compte a été créé avec succès.')
                return redirect('post_list')
            else:
                messages.error(request, 'Erreur lors de l\'authentification.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='login')
def index(request):
    # Vue pour afficher les produits
    template = 'blog/post_list.html'
    Poste = PostList.objects.all()
    context = {'posts': Poste}
    return render(request, template, context)