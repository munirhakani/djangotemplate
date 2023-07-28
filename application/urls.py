from django.urls import path
from application.views import DeviceListView
from application.views import ProductListView
from application.views import OrderFormView
from application.views import OrderProductDeleteView
from application.views import OrderSubmitted
from application.views import OrdersListView
from application.views import OrderDetailView
from application.views import OrderProductCreateUpdate, OrderProductDelete


app_name='application'
urlpatterns = [
    path('', DeviceListView.as_view(), name='DeviceListView'),
    path('<device_id>/product/', ProductListView.as_view(), name='ProductListView'),
    path('OrderProductCreateUpdate/<productid>/', OrderProductCreateUpdate, name='OrderProductCreateUpdate'),
    path('OrderProductDelete/<orderproductid>/', OrderProductDelete, name='OrderProductDelete'),
    path('cart/', OrderFormView.as_view(), name='OrderFormView'),
    path('<order_id>/submitted/', OrderSubmitted, name='OrderSubmitted'),
    path('<product_id>/orderproductdeleteproduct/', OrderProductDeleteView.as_view(), name='OrderProductDeleteView'),
    path('orders/', OrdersListView.as_view(), name='OrdersListView'),
    path('order/<pk>/', OrderDetailView.as_view(), name='OrderDetailView'),
]