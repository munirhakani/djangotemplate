from crum import get_current_user
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings


class Category(models.Model):
    data = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name='Category Name', help_text='Enter Category Name')
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    data = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name='Brand Name', help_text='Enter Brand Name')
    isnotpopular = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    code = models.CharField(max_length=20)
    data = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name='Device Name', help_text='Enter Device Name')
    active = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name   


from os import path
def upload_to(instance, filename):
    return path.join(instance.device.code, filename)

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=255, editable=False)
    stock = models.SmallIntegerField(default=0)
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    code = models.CharField(max_length=15, null=True, blank=True, editable=False)
    device = models.ForeignKey(Device, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    image = models.ImageField(
        max_length=250, upload_to=upload_to,
        null=True, blank=True, editable=False,
        verbose_name='Product Image', help_text='Select image file to upload'
    )

    class Meta:
        ordering = ['sku', ]

    def __str__(self):
        return self.sku
    
    @property
    def quantityincart(self):
        orderproduct =  OrderProduct.objects \
            .filter(order=Order.objects.filter(submitted=None).filter(user=get_current_user()).first()) \
            .filter(product_id=self.id).values('quantity', 'id').first()
        return orderproduct


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    notes = models.CharField(max_length=255, blank=True, null=True)
    submitted = models.DateTimeField(null=True, blank=True, default=None)
    processed = models.DateTimeField(null=True, blank=True, default=None)
    objects = models.Manager()

    def __str__(self):
        return f'Order # is {self.id}'

    @property
    def total(self):
        return sum(orderproduct.amount for orderproduct in OrderProduct.objects.filter(order=self))
    
    @classmethod
    def pre_save(cls, sender, instance, *args, **kwargs):
        if not instance.pk:
            instance.user = get_current_user()
pre_save.connect(Order.pre_save, sender=Order)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.SmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Product is {self.product.sku} and quantities are {self.quantity}'

    @property
    def amount(self):
        return self.quantity*self.price

    def createupdate(product, quantity):
        order = Order.objects.filter(submitted=None).filter(user=get_current_user()).first()
        if not order:
            order = Order.objects.create()
        orderproduct = OrderProduct.objects.filter(order=order).filter(product=product).first()
        if orderproduct:
            orderproduct.quantity = int(quantity)
            orderproduct.save()
        else:
            orderproduct = OrderProduct.objects.create(
                product=product,
                price=product.price,
                quantity=quantity,
                order=order,
            )
        return orderproduct
    
    def objectdelete(orderproductid):
        OrderProduct.objects.filter(id=orderproductid).delete()
    
    @classmethod
    def pre_save(cls, sender, instance, *args, **kwargs):
        if not instance.pk:
            order = Order.objects.filter(submitted=None).filter(user=get_current_user()).first()
            if not order:
                order = Order.objects.create()
            instance.order = order
pre_save.connect(OrderProduct.pre_save, sender=OrderProduct)