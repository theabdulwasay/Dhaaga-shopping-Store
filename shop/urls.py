from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("collection/", views.product_list, name="product_list"),
    path("collection/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/success/", views.order_success, name="order_success"),
    path("order/track/", views.order_track, name="order_track"),
    path("contact/", views.contact, name="contact"),
    path("api/chat/", views.chat_api, name="chat_api"),
]
