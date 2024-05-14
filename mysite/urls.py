from django.contrib import admin, auth
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Remplacez cela par `views` de `django.contrib.auth`
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework import routers
from magasin.views import ProductViewset, CategoryAPIView

router = routers.SimpleRouter()
router.register('produit', ProductViewset, basename='produit')

urlpatterns = [
    path('', views.index, name='home'),
    path('api/', include(router.urls)),
    path('blog/', include('blog.urls')),

    path('admin/', admin.site.urls),
    path('magasin/', include('magasin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
