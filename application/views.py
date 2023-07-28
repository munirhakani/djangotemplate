from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from application.forms import OrderForm
from application.models import Device, Order, OrderProduct, Product


class DeviceListView(ListView):
    model = Device

    def get_queryset(self):
        return super().get_queryset().filter(active=1).order_by('brand__isnotpopular', 'brand__name', 'name')


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return super().get_queryset().filter(device_id=self.kwargs['device_id'], stock__gt=0)


@login_required
def OrderProductCreateUpdate(request, productid):
    product = Product.objects.get(pk=productid)
    quantity = request.POST['product_id_'+productid]
    orderproduct = OrderProduct.createupdate(product, quantity)
    context = {
        'product': product,
        'orderproduct': orderproduct,
    }
    return render(request, 'application/deletebutton.html', context)


@login_required
def OrderProductDelete(request, orderproductid):
    OrderProduct.objectdelete(orderproductid)
    return HttpResponse('In Cart: 0')


class OrderFormView(LoginRequiredMixin, FormView):
    form_class = OrderForm
    template_name = 'application/orderproduct_list.html'

    def get_context_data(self, **kwargs):
        _context_data = super().get_context_data(**kwargs)
        _getobjectts = "OrderProduct.objects.filter(order=Order.objects.filter(submitted=None).filter(user=self.request.user).first())"
        _context_data['object_list'] = eval(_getobjectts)
        _context_data['total'] = '{:.2f}'.format(sum(float(object.amount) for object in eval(_getobjectts)))
        return _context_data
    
    def form_valid(self, form):
        order = Order.objects.filter(submitted=None).filter(user=self.request.user).first()
        order.notes = form.cleaned_data['notes']
        order.submitted = datetime.now()
        order.save()
        self.success_url = reverse('application:OrderSubmitted', kwargs={'order_id': order.id})
        return super().form_valid(form)


def OrderSubmitted(request, order_id):
    return render(request, 'application/submitted.html', {'order_id': order_id})


class OrderProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, product_id):
       object = OrderProduct.objects.get(id=product_id)
       object.delete()
       return redirect(reverse('application:OrderFormView'))


class OrdersListView(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-pk')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        _context_data = super().get_context_data(**kwargs)
        _getobjectts = "OrderProduct.objects.filter(order_id=self.kwargs['pk'])"
        _context_data['object_list'] = eval(_getobjectts)
        _context_data['total'] = '{:.2f}'.format(sum(float(object.amount) for object in eval(_getobjectts)))
        return _context_data