from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .forms import *
from .models import *
from django.http import Http404 , JsonResponse
from hitcount.views import HitCountDetailView
import json
from django.contrib import messages
import datetime
from .filters import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Blog
from plugins.forms import SliderForm , BrandForm
from plugins.models import Slider , Brand
from urllib.parse import unquote
# Create your views here.

def paginator_my(request,paginate_by,queryset):
    # start paginate
    # create the paginator
    paginator = Paginator(queryset, paginate_by)
    # get the page number from the request
    page_number = request.GET.get('page')
    try:
        # get the page object
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # if the page is not an integer, return the first page
        page = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, raise a 404 error
        raise Http404
    page = page
    # end paginate
    return page

class CreateShop(View):
    def get(self ,request):
        try:
            user_has_shop = Shop.objects.get(user=request.user)
            if user_has_shop != None:
                return redirect('shop-management')
        except:
            pass
        form = ShopForm()
        context = {
            'form':form,
        }
        return render(request , 'shop/create_shop.html' , context)
    def post(self , request):
        form = ShopForm(request.POST , request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            user = request.user
            myform.user = user
            myform.save()
            return redirect('shop-management')
        context = {
            'form':form,
        }
        return render(request , 'shop/create_shop.html' , context)

class ShopManagement(View):
    def post(self,request):
        shop_has_user = Shop.objects.get(user=request.user)
        shop_form = ShopForm(request.POST , request.FILES , instance=shop_has_user)
        # form to update shop
        if shop_form.is_valid():
            myform = shop_form.save(commit=False)
            myform.user = request.user
            myform.save()
            return redirect('shop-management')
        # form to product
        productform = ProductForm(request,request.POST , request.FILES)
        if productform.is_valid():
            myform = productform.save(commit=False)
            myform.shop = shop_has_user
            myform.save()
            return redirect('shop-management')
        # this to form slider
        sliderform = SliderForm(request.POST,request.FILES)
        if sliderform.is_valid():
            myform = sliderform.save(commit=False)
            myform.shop = shop_has_user
            myform.save()
            return redirect('shop-management')
        if request.method == "POST":
            if 'delete-slider' in request.POST:
                id_slider = request.POST['delete-slider']
                slider = Slider.objects.get(id=id_slider)
                slider.delete()
                return redirect('shop-management')
        #  this to form brand
        if request.method == "POST":
            if 'delete-brand' in request.POST:
                id_brand = request.POST['delete-brand']
                brand = Brand.objects.get(id=id_brand)
                brand.delete()
                return redirect('shop-management')
        brandform = BrandForm(request.POST,request.FILES)
        if brandform.is_valid():
            myform = brandform.save(commit=False)
            myform.shop = shop_has_user
            myform.save()
            return redirect('shop-management')
        context = {
            'shop':shop_has_user,
            'shop_form':shop_form,
            'productform':productform,
        }
        return render(request, 'shop/shop_management.html' , context)
    def get(self , request):
        shop_has_user = Shop.objects.get(user=request.user)
        shop_form = ShopForm(instance=shop_has_user)
        products = Product.objects.filter(shop=shop_has_user)
        categorieform = CategorieForm(request)
        # get counter views
        couner_products = products.count
        total_views = 0
        for pro in products:
            hitcount = HitCount.objects.get_for_object(pro)
            total_views += hitcount.hits
        paginate_by = 3
        filter = ProductFilter(request.GET , queryset=products)
        pagei = paginator_my(request , paginate_by ,filter.qs )
        products = pagei
        productform = ProductForm(request)
        sliderform = SliderForm()
        brandform = BrandForm()
        pageform = PageForm()
        # orders is  complete
        orders_complete = Order.objects.filter(shop=shop_has_user , complete=True)
        orders_complete = orders_complete.count 
        context = {
            'shop':shop_has_user,
            'shop_form':shop_form,
            'productform':productform,
            'products':products,
            'total_views':total_views,
            'orders_complete':orders_complete,
            'sliderform':sliderform,
            'brandform':brandform,
            'pageform':pageform,
            'filter':filter,
            'couner_products':couner_products,
            'categorieform':categorieform,
        }
        return render(request, 'shop/shop_management.html' , context)

def categorie(request):
    if request.method == "POST":
        if 'delete-categorie' in request.POST:
            categorie = Categorie.objects.get(id=request.POST['delete-categorie'])
            categorie.delete()
            messages.info(request, f" Has been deleted {categorie.name} ")
            return redirect('shop-management')
        form  = CategorieForm(request,request.POST,request.FILES)
        if form.is_valid():
            shop = Shop.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.shop = shop 
            myform.save()
            messages.info(request, f" Has been created {myform.name} ")
            return redirect('shop-management')


class ProductEdit(View):
    def get(self,request,id):
        get_product = Product.objects.get(id=id)
        shop = Shop.objects.get(user=request.user)
        if shop == get_product.shop:
            form = ProductForm(request,instance=get_product)
            context = {
                'shop':shop,
                'form':form,
            }
            return render(request , 'shop/product_edit.html' , context)
    def post(self,request,id):
        get_product = Product.objects.get(id=id)
        shop = Shop.objects.get(user=request.user)
        if shop == get_product.shop:
            form = ProductForm(request,request.POST,request.FILES , instance=get_product)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.shop = shop
                myform.save()
                return redirect(f'/shop/manage-shop/{id}/edit')

def create_page(request):
    shop_has_user = Shop.objects.get(user=request.user)
    pageform = PageForm(request.POST)
    if pageform.is_valid():
        myform = pageform.save(commit=False)
        myform.shop = shop_has_user
        myform.save()
        return redirect('shop-management')
    if request.method == 'POST':
        if 'delete-page' in request.POST:
            id = request.POST['delete-page']
            page = Page.objects.get(id=id)
            page.delete()
            return redirect('shop-management')

class OrdersComplete(View):
    def get(self,request):
        user = request.user
        get_shop = Shop.objects.get(user=user)
        # orders is  complete
        orders_complete = Order.objects.filter(shop=get_shop , complete=True)
        filter = OrderFilter(request.GET , queryset=orders_complete)
        orders_complete = filter.qs
        paginate_by = 1
        # start paginate
        queryset = orders_complete
        # create the paginator
        paginator = Paginator(queryset, paginate_by)
        # get the page number from the request
        page_number = self.request.GET.get('page')
        try:
            # get the page object
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # if the page is not an integer, return the first page
            page = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, raise a 404 error
            raise Http404
        page = page
        # end paginate

        context = {
            'shop':get_shop,
            'orders':page,
            'fiter':filter,
        }
        return render(request,'shop/orders_complete.html' , context)

class SubmitOrder(View):
    def get(self,request,id):
        current_user = request.user
        order = Order.objects.get(id=id)
        shop = Shop.objects.get(user=current_user)
        if order.shop == shop:
            form = StatusOrderForm(instance=order)
            shipping = ShippingAddress.objects.get(order=order)
            items = OrderItem.objects.filter(order=order)
            total = 0
            for i in items:
                total = total + i.get_total 

            context = {
                'shop':shop,
                'shipping':shipping,
                'order':order,
                'items':items,
                'total':total,
                'form':form,
            }
            return render(request, 'shop/submit_order.html' , context)
        else:
            return redirect('shop-management')
    def post(self,request,id):
        current_user = request.user
        order = Order.objects.get(id=id)
        shop = Shop.objects.get(user=current_user)
        if order.shop == shop:
            form = StatusOrderForm(request.POST , instance=order)
            if form.is_valid():
                form.save()
                return redirect('orders-copmlete')

class ShopView(View):
    def get(self,request , slug):
        decode = unquote(slug)
        get_shop = Shop.objects.get(slug=decode)
        products = Product.objects.filter(shop=get_shop)
        products_5 = Product.objects.filter(shop=get_shop)[:5]
        products_3 = Product.objects.filter(shop=get_shop)[:3]

        user_has_blog = get_shop.user
        try:
            get_blog = Blog.objects.get(user=user_has_blog)
        except:
            get_blog = None
        # get count to items to user request
        couner_items = None 
        if request.user.is_authenticated:
            customer = request.user.customer
            order , created = Order.objects.get_or_create(customer=customer ,complete=False  , shop=get_shop)
            items = OrderItem.objects.filter(order=order)
            couner_items = 0
            get_total_price = 0
            for item in items:
                if item.product.shop == get_shop:
                    get_total_price = get_total_price + item.get_total
                    couner_items = couner_items + item.quantity
        else:
            get_total_price =  0 
        context = {
            'shop':get_shop,
            'blog':get_blog,
            'total':get_total_price,
            'products':products,
            'couner_items':couner_items,
            'products_5':products_5,
            'products_3':products_3,
        }
        return render(request , 'shop/templates/nour/shop_view.html' , context)

class AllProduct(View):
    def get(self,request , slug):
        get_shop = Shop.objects.get(slug=slug)
        products = Product.objects.filter(shop=get_shop)
        filter = ProductFilter(request=request,data=request.GET, queryset=products)
        products = filter.qs
        user_has_blog = get_shop.user
        try:
            get_blog = Blog.objects.get(user=user_has_blog)
        except:
            get_blog = None
        # start paginate
        paginate_by = 6
        page = paginator_my(request,paginate_by,products)
        # end paginate
        # get count to items to user request
        couner_items = None 
        if request.user.is_authenticated:
            customer = request.user.customer
            order , created = Order.objects.get_or_create(customer=customer ,complete=False  , shop=get_shop)
            items = OrderItem.objects.filter(order=order)
            couner_items = 0
            get_total_price = 0
            for item in items:
                if item.product.shop == get_shop:
                    get_total_price = get_total_price + item.get_total
                    couner_items = couner_items + item.quantity
        else:
            get_total_price =  0 
        context = {
            'shop':get_shop,
            'total':get_total_price,
            'blog':get_blog,
            'products':page,
            'couner_items':couner_items,
            'filter':filter,
        }
        return render(request , 'shop/templates/nour/all_product.html' , context)

class ProductDetail(HitCountDetailView):
    model = Product
    template_name = 'shop/templates/nour/product_detail.html'
    context_object_name = 'product'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_shop = Shop.objects.get(slug=self.kwargs['shop'])
        product_5 = Product.objects.filter(shop=get_shop ).order_by('-created_date')[:5]
        product_4 = Product.objects.filter(shop=get_shop ).order_by('created_date')[:4]
        context['product_5'] =product_5
        context['product_4'] =product_4
        product_10 = Product.objects.filter(shop=get_shop)[:10]
        context['product_10'] =product_10
        context['shop'] = get_shop
        # get count to items to user request 
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order , created = Order.objects.get_or_create(customer=customer ,complete=False  , shop=get_shop)
            items = OrderItem.objects.filter(order=order)
            couner_items = 0
            get_total_price = 0
            for item in items:
                if item.product.shop == get_shop:
                    get_total_price = get_total_price + item.get_total
                    couner_items = couner_items + item.quantity
            context['couner_items'] = couner_items
            context['total'] = get_total_price
            #form reviews
            reviewform = ReviewForm()
            context['reviewform'] = reviewform
        return context
    def queryset(self):
        return Product.objects.filter(id=self.kwargs['id'])
    def get_object(self, queryset=None):
        queryset = self.queryset() if queryset is None else queryset
        product_object = super().get_object(queryset)
        if product_object.shop.slug != self.kwargs['shop']:
            raise Http404("product not found")
        return product_object
    def post(self , request, *args, **kwargs):
        try:
            get_shop = Shop.objects.get(slug=self.kwargs['shop'])
            product = Product.objects.filter(id=self.kwargs['id']).first()
            customer = request.user.customer
            reviewform = ReviewForm(request.POST)
            if reviewform.is_valid():
                myform = reviewform.save(commit=False)
                myform.product = product
                myform.created_by = customer
                myform.save()
                return redirect(f'/shop/{get_shop.name}/{product.slug}/{product.id}')
        except:
            return redirect('index')

class CartView(View):
    def get(self , request , shop):
        get_shop = Shop.objects.get(slug=shop)
        categories = Categorie.objects.filter(product__isnull=False ,shop=get_shop).distinct().first()
        product_2 = Product.objects.filter(shop=get_shop , categorie=categories)[:2]
        product_5 = Product.objects.filter(shop=get_shop ).order_by('-created_date')[:5]
        product_4 = Product.objects.filter(shop=get_shop ).order_by('created_date')[:4]
        if request.user.is_authenticated:
            customer = request.user.customer
            order , created = Order.objects.get_or_create(customer=customer ,complete=False , shop=get_shop )
            items = OrderItem.objects.filter(order=order)
            list_items_has_blog = []
            get_total_price = 0
            couner_items = 0
            for item in items:
                if item.product.shop == get_shop:
                    list_items_has_blog.append(item)
                    get_total_price = get_total_price + item.get_total
                    couner_items = couner_items + item.quantity
        else:
            items = None
            get_total_price = 0
            couner_items = None

        context = {
            'shop':get_shop,
            'items':items,
            'total':get_total_price,
            'couner_items':couner_items,
            'product_2':product_2,
            'product_4':product_4,
            'product_5':product_5,
            
        }
        return render(request , 'shop/templates/nour/cart.html' , context)

def updateItem(request , shop):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    get_shop = Shop.objects.get(slug=shop)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer , complete=False , shop=get_shop)
    orderItem , created = OrderItem.objects.get_or_create(order=order ,product=product )
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item whs added' , safe=False)

class ViewPages(View):
    def get(self,request , **kwargs):
        get_shop = Shop.objects.get(slug=kwargs['shop'])
        get_page = Page.objects.get(id=self.kwargs['id'])
        if get_page.shop == get_shop:
            context = {
                'page':get_page,
                'shop':get_shop,
            }
            return render(request , 'shop/templates/nour/page_detail.html' , context)
        else:
            raise Http404("product not found")

class CheckoutView(View):
    def get(self , request , shop):
        get_shop = Shop.objects.get(slug=shop)
        product_5 = Product.objects.filter(shop=get_shop ).order_by('-created_date')[:5]
        product_4 = Product.objects.filter(shop=get_shop ).order_by('created_date')[:4]
        if request.user.is_authenticated:
            customer = request.user.customer
            order , created = Order.objects.get_or_create(customer=customer ,complete=False , shop=get_shop )
            items = OrderItem.objects.filter(order=order)
            form_2 = CustomerForm(instance=customer)
            list_items_has_shop = []
            get_total_price = 0
            couner_items = 0
            for item in items:
                if item.product.shop == get_shop:
                    list_items_has_shop.append(item)
                    get_total_price = get_total_price + item.get_total
                    couner_items = couner_items + item.quantity
        else:
            items = None
            get_total_price = 0
            couner_items = None
            form_2 = CustomerForm()
            list_items_has_shop = []
        form = ShippingAddressForm()
        
        context = {
            'shop':get_shop,
            'items':list_items_has_shop,
            'total':get_total_price,
            'couner_items':couner_items,
            'form':form,
            'form_2':form_2,
            'product_5':product_5,
            'product_4':product_4,
        }
        return render(request , 'shop/templates/nour/checkout.html' , context)
    def post(self, request, shop ):
        get_shop = Shop.objects.get(name=shop)
        transaction_id = datetime.datetime.now().timestamp()
        if request.user.is_authenticated:
            customer = request.user.customer
            order , created = Order.objects.get_or_create(customer=customer ,complete=False , shop=get_shop )
            items = OrderItem.objects.filter(order=order)
            order.transaction_id = transaction_id
            order.complete = True
            order.save()
            form = ShippingAddressForm(request.POST)
            form_2 = CustomerForm(request.POST , instance=customer)
            if form.is_valid() and form_2.is_valid():
                myform_2 = form_2.save(commit=False)
                myform_2.user = request.user
                myform = form.save(commit=False)
                myform.customer = customer
                myform.order = order
                myform_2.save()
                myform.save()

                return redirect(f'/shop/{shop}')