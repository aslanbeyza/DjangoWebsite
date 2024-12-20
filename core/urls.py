
from django.contrib import admin
from django.urls import path
from AppEcommerce.views import *
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("logout/", Logout, name="logout"),
    path("category/", category, name="category"),
    path("basket/", basket, name="basket"),
    path("product-detail/<int:product_id>", product_detail, name="product-detail"),

    #Authenticated
    path('login/', Login, name='login'),
    path('register/', Register, name='register'),
    path("profil/", profil, name="profil"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),

    path("set_language/<str:language>", set_language, name="set-language"),
    
    ]