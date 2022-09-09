from django.urls import path
from . import views

urlpatterns = [
    path('',views.OrderCreateListView.as_view(),name='orders'),
    path('<int:order_id>/',views.OrderDetailListView.as_view(),name='detailview'),
    path('order-status/<int:order_id>/',views.OrderStatusUpdateView.as_view(),name='Statusview'),
    path('user/<int:user_id>/orders/',views.UserOrdersView.as_view(),name='users_orders'),
    path('user/<int:user_id>/order/<int:order_id>/',views.UserOrderDetailView.as_view(),name='user_order_detail'),
]
