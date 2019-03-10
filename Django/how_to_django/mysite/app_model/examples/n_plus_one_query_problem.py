from app_model.models import Category, Product
from app_model.helpers import debugger_queries


@debugger_queries
def products_list():
    products = []
    for product in Product.objects.all():
        products.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })
    return products

@debugger_queries
def products_list_with_select_related():
    products = []
    for product in Product.objects.select_related('category').all():
        products.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })
    return products


@debugger_queries
def products_list_without_category():
    products = []
    for product in Product.objects.all():
        products.append({
            'id': product.id,
            'title': product.title,
        })
    return products

@debugger_queries
def category_list():
    category = []
    for product in Category.objects.first().product_set.all():
        category.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })

    return category
    
@debugger_queries
def category_list_with_select_related():
    category = []
    for product in Category.objects.select_related('product').first().product_set.all():
    #for product in Category.objects.first().product_set.select_related('product').all():
        category.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })

    return category
       