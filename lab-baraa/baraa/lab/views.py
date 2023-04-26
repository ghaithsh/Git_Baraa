
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


def search(request):
    query = request.POST['search']
    if not query:
        return redirect("http://"+"64.226.77.150:5050"+"/product/notfound")
    return redirect("http://"+"64.226.77.150:5050"+"/products/"+query)


def product_list(request, id):
    if request.method == 'POST':
        return search(request)
    product_lists = product.objects.filter(id=id, active=True)
    if not product_lists:
        return redirect("http://"+"64.226.77.150:5050"+"/product/notfound")
    image_products = image_product.objects.filter(
        product_name__id=id)
    if not image_products:
        return redirect("http://"+"64.226.77.150:5050"+"/product/notfound")
    context = {'product_lists': product_lists, "images": image_products}
    return render(request, '../templates/product.html', context)


def category_list(request):
    if request.method == 'POST':
        return search(request)
    category_lists = category.objects.filter(
        parent__isnull=True, Image__isnull=False)
    context = {'category_lists': category_lists}

    return render(request, '../templates/home.html', context)


def sub_category_list(request, id):
    if request.method == 'POST':
        return search(request)
    try:
        category_lists = category.objects.filter(
            parent=category.objects.get(id=id), Image__isnull=False)
        if not category_lists:
            return redirect("http://"+"64.226.77.150:5050"+"/sub/"+str(id)+"/products")
        context = {'category_lists': category_lists}
        return render(request, '../templates/home.html', context)
    except ObjectDoesNotExist:
        pass


@login_required(login_url='http://"+"64.226.77.150:5050"+"/admin/login/?next=/admin/')
def product_page(request):
    if request.method == 'POST':
        if request.POST.get("search"):
            query = request.POST["search"]
            if not query:
                return redirect("http://"+"64.226.77.150:5050"+"/product/notfound")
            return redirect("http://"+"64.226.77.150:5050"+"/products/"+query)
        if not request.POST["name"] or not request.POST["category"] or not request.POST["color"] or product.objects.filter(name=request.POST["name"]):
            return redirect("http://"+"64.226.77.150:5050"+"/product/error")
        images = request.FILES.getlist('images')
        name = request.POST["name"]
        category_project = request.POST["category"]
        description = request.POST["description"]
        color = request.POST["color"]
        price = request.POST["price"]
        pro = product.objects.create(
            name=name, category_name=category.objects.get(id=category_project), description=description, color_pro=color, price=price)
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
        return search(request)
    return render(request, '../templates/notfound.html')


def error(request):
    if request.method == 'POST':
        query = request.POST['search']
        if not query:
            return redirect("http://"+"64.226.77.150:5050"+"/notfound")
        return redirect("http://"+"64.226.77.150:5050"+"/products/"+query)
    return render(request, '../templates/error_add.html')


@login_required(login_url='http://"+"64.226.77.150:5050"+"/admin/login/?next=/admin/')
def edit_price(request):
    if request.method == 'POST':
        if request.POST.get("search"):
            query = request.POST["search"]
            if not query:
                return redirect("http://"+"64.226.77.150:5050"+"/product/notfound")
            return redirect("http://"+"64.226.77.150:5050"+"/products/"+query)
        cat = request.POST["category"]
        op = request.POST["operation"]
        val = request.POST["value"]
        product_lists = product.objects.filter(
            category_name__id=cat)
        if not product_lists or not val:
            return redirect("http://"+"64.226.77.150:5050"+"/product/error")
        for i in product_lists:
            if op == "+":
                i.price += i.price*(int(val)/100)
            else:
                i.price -= i.price*(int(val)/100)
            i.save()
    category_lists = category.objects.filter(
        parent__isnull=False)
    context = {'category_lists': category_lists}
    return render(request, '../templates/edit_price.html', context)


def products(request, id):
    if request.method == 'POST':
        return search(request)
    context = {}
    dic = {}
    ii = 1
    product_lists = product.objects.filter(
        category_name=category.objects.get(id=id), active=True)
    if not product_lists:
        return redirect("http://"+"64.226.77.150:5050"+"/product/notfound")
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


def products_search(request, query):
    if request.method == 'POST':
        return search(request)
    product_lists = product.objects.filter(
        name__contains=query, active=True)
    if not product_lists:
        return redirect("http://"+"64.226.77.150:5050"+"/notfound")
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
