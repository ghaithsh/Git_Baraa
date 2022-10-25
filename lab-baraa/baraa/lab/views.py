
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import product, category, image_product
from django.contrib.auth.decorators import login_required

from django.template.defaulttags import register


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_image(image_list, url):
    return image_list[0].Image


@register.filter
def get_url(image, result):
    return image.url


def product_list(request, id):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    product_lists = product.objects.filter(id=id, active=True)
    if not product_lists:
        return redirect("http://127.0.0.1:8000/product/notfound")
    image_products = image_product.objects.filter(
        product_name__id=id)
    if not image_products:
        return redirect("http://127.0.0.1:8000/product/notfound")
    context = {'product_lists': product_lists, "images": image_products}
    return render(request, '../templates/product.html', context)


def category_list(request):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    category_lists = category.objects.filter(
        parant__isnull=True, Image__isnull=False)
    context = {'category_lists': category_lists}

    return render(request, '../templates/home.html', context)


def sub_category_list(request, id):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    try:
        category_lists = category.objects.filter(
            parant=category.objects.get(id=id), Image__isnull=False)
        if not category_lists:
            return redirect("http://127.0.0.1:8000/sub/"+str(id)+"/products")
        context = {'category_lists': category_lists}
        return render(request, '../templates/home.html', context)
    except ObjectDoesNotExist:
        pass


@login_required(login_url='http://127.0.0.1:8000/admin/login/?next=/admin/')
def product_page(request):
    if request.method == 'POST':
        if request.POST.get("search"):
            quary = request.POST["search"]
            if not quary:
                return redirect("http://127.0.0.1:8000/product/notfound")
            return redirect("http://127.0.0.1:8000/products/"+quary)
        if not request.POST["name"] or not request.POST["category"] or not request.POST["color"] or product.objects.filter(name=request.POST["name"]):
            return redirect("http://127.0.0.1:8000/product/error")
        images = request.FILES.getlist('images')
        name = request.POST["name"]
        category_projuct = request.POST["category"]
        description = request.POST["description"]
        color = request.POST["color"]
        price = request.POST["price"]
        pro = product.objects.create(
            name=name, category_name=category.objects.get(id=category_projuct), description=description, color_pro=color, price=price)
        pro.save()
        for img in images:
            if img == images[0]:
                im = image_product.objects.create(
                    product_name=product.objects.get(id=pro.id), Image=img, main_image=True)
            else:
                im = image_product.objects.create(
                    product_name=product.objects.get(id=pro.id), Image=img)
            im.save()
    lists = category.objects.all()
    context = {'category_lists': lists}
    return render(request, '../templates/add_product.html', context)
    # Create your views here.


def not_found(request):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    return render(request, '../templates/notfound.html')


def error(request):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    return render(request, '../templates/error_add.html')


@login_required(login_url='http://127.0.0.1:8000/admin/login/?next=/admin/')
def edit_price(request):
    if request.method == 'POST':
        if request.POST.get("search"):
            quary = request.POST["search"]
            if not quary:
                return redirect("http://127.0.0.1:8000/product/notfound")
            return redirect("http://127.0.0.1:8000/products/"+quary)
        cat = request.POST["category"]
        op = request.POST["opration"]
        val = request.POST["value"]
        product_lists = product.objects.filter(
            category_name__id=cat)
        if not product_lists or not val:
            return redirect("http://127.0.0.1:8000/product/error")
        for i in product_lists:
            if op == "+":
                i.price += i.price*(int(val)/100)
            else:
                i.price -= i.price*(int(val)/100)
            i.save()
    category_lists = category.objects.filter(
        parant__isnull=False)
    context = {'category_lists': category_lists}
    return render(request, '../templates/edit_price.html', context)


def products(request, id):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    context = {}
    dic = {}
    ii = 1
    product_lists = product.objects.filter(
        category_name=category.objects.get(id=id), active=True)
    if not product_lists:
        return redirect("http://127.0.0.1:8000/product/notfound")
    for i in product_lists:
        image_products = image_product.objects.filter(
            product_name=product.objects.get(id=i.id), main_image=True)
        if not image_products:
            continue
        dic['id'] = i.id
        dic['name'] = i.name
        dic['category'] = i.category_name.main_category
        dic['color'] = i.color_pro
        dic['description'] = i.description
        dic['price'] = i.price
        dic['image'] = image_products
        context['product'+str(ii)] = dic
        dic = {}
        ii += 1

    return render(request, '../templates/products_views.html', {'context': context})


def products_search(request, quary):
    if request.method == 'POST':
        quary = request.POST['search']
        if not quary:
            return redirect("http://127.0.0.1:8000/product/notfound")
        return redirect("http://127.0.0.1:8000/products/"+quary)
    product_lists = product.objects.filter(
        name__contains=quary, active=True)
    if not product_lists:
        return redirect("http://127.0.0.1:8000/product/notfound")
    context = {}
    dic = {}
    ii = 1
    for i in product_lists:
        image_products = image_product.objects.filter(
            product_name=product.objects.get(id=i.id), main_image=True)
        if not image_products:
            continue
        dic['id'] = i.id
        dic['name'] = i.name
        dic['category'] = i.category_name.main_category
        dic['color'] = i.color_pro
        dic['description'] = i.description
        dic['price'] = i.price
        dic['image'] = image_products
        context['product'+str(ii)] = dic
        dic = {}
        ii += 1
    return render(request, '../templates/products_views.html', {'context': context})


def test(request):
    return render(request, '../templates/test.html')
