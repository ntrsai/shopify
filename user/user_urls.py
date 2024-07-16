from django.urls import path
from user import views
urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('add-to-cart/<product_id>', views.add_to_cart),
    path('cart/', views.cart),
    path('cart/<flag>/<cart_id>', views.update_cart_quantity),
    path('category/<category_value>', views.filter_by_category),
    path('sort/<flag>', views.sort_by_price),
    path('search/', views.search),
    path('delete/<cart_id>',views.delete_cart_items),
    path('order-summary/',views.order_summary),
    
]