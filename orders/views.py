from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from baskets.models import Basket
from orders.models import Order, OrderItem
from orders.forms import OrderItemForm
from products.models import Product


class OrderList(ListView):
    model = Order
    extra_context = {'title': 'GeekShop - Заказы'}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(OrderList, self).dispatch(request, *args, **kwargs)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        total_quantity = None
        total_sum = None
        if self.request.POST:
            formset = order_formset(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                total_quantity = basket_items[0].total_quantity()
                total_sum = basket_items[0].total_sum()
            if len(basket_items):
                order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = order_formset()
                for num, form in enumerate(formset.forms):
                    form.initial.update({
                        'product': basket_items[num].product,
                        'quantity': basket_items[num].quantity,
                        'price': basket_items[num].product.price,
                    })
                basket_items.delete()
            else:
                formset = order_formset()
        data.update({
            'orderitems': formset,
            'total_sum': total_sum,
            'total_quantity': total_quantity,
        })
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(OrderItemsCreate, self).dispatch(request, *args, **kwargs)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = order_formset(self.request.POST, instance=self.object)
        else:
            formset = order_formset(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(OrderItemsUpdate, self).dispatch(request, *args, **kwargs)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:orders_list')

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(OrderDelete, self).dispatch(request, *args, **kwargs)


class OrderRead(DetailView):
    model = Order
    extra_context = {'title': 'заказ/просмотр'}

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(OrderRead, self).dispatch(request, *args, **kwargs)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:orders_list'))


@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})
