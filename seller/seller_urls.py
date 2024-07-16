from django.urls import path, include
from seller import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.dashboard),
    path('add/', views.app_product),
    path('delete/<product_id>', views.delete_product),
    path('update/<product_id>', views.update_product)
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
