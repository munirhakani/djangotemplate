from django.apps import apps
from django.core.files import File
from imghdr import what
from os import remove
from PIL import Image
from pandas import read_excel, isna
from requests import get
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
from application.models import Product
from downupload.price import getPrice

def download(url, filename):
    content = get(url).content
    file = open(filename, 'wb')
    file.write(content)
    file.close()

def removefile(filename):
    remove(filename)

def downloadImage(image_url, filename):
    print(f'Downloading {filename} ...')
    content = get(image_url, headers=headers).content
    with open(filename, 'wb') as handler:
        print(f'Saving {filename} ...')
        handler.write(content)

    if what(filename):
        print(f'Converting RBB and resizing {filename} ...')
        image = Image.open(filename).convert('RGB').save(filename)
        image = Image.open(filename)
        _image = image.resize((300, 300))
        _image.save(filename)

def getid(model, column, data):
    kwargs = {'{0}__{1}'.format(column, 'exact'): data}
    _model = apps.get_model('application', model)
    try:
        return _model.objects.get(**kwargs).id
    except:
        return None

def create(model, kwargs):
    _model = apps.get_model('application', model)
    return _model.objects.create(**kwargs)

def fullcatalogue():
    data = read_excel('full-catalogue.xlsx')
    for index, row in data.iterrows():
        print(f'Index:{index}, SKU:{row.SKU}')
        # Product
        productid = getid('Product', 'sku', row.SKU)
        if productid is None:
            # Category
            categoryid = getid('Category', 'data', row.Category)
            if categoryid is None:
                # Create Category
                kwargs = {
                    'data': row.Category,
                    'name': row.Category,
                }
                categoryid = create('Category', kwargs).id
                print(f'Category {row.Category}, ID:{categoryid} successfully create.')
            # Device
            deviceid = getid('Device', 'data', row['Product Model'])
            if deviceid is None:
                # Brand
                brandid = getid('Brand', 'data', row.Brand)
                if brandid is None:
                    # Create Brand
                    kwargs = {
                        'data': row.Brand,
                        'name': row.Brand,
                    }
                    brandid = create('Brand', kwargs).id
                    print(f'Brand {row.Brand}, ID:{brandid} successfully create.')
                # Create Device
                kwargs = {
                    'code': row['Group ID'][row['Group ID'].rfind('-')+1:],
                    'data': row['Product Model'],
                    'name': row['Product Model'],
                    'brand_id': brandid,
                }
                deviceid = create('Device', kwargs).id
                print(f"Device {row['Product Model']}, ID:{deviceid} successfully create.")
            # Create Product
            print(f'Creating {row.SKU} ...')
            kwargs = {
                'sku': row.SKU,
                'title': row.Title,
                'stock': int(row.Stock),
                'code': None if isna(row['UPC Code']) else row['UPC Code'],
                'device_id': int(deviceid),
                'category_id': int(categoryid),
                'image': None,
            }
            print(kwargs)
            product = create('Product', kwargs)
            product.save()
            if isna(row['Large Image']) is False and 'http' in row['Large Image']:
                filename = row.SKU + row['Large Image'][row['Large Image'].rfind('.'):]
                downloadImage(row['Large Image'], filename)
                product.image.save(filename, File(open(filename, 'rb')))
                product.save()
                removefile(filename)
            print(f'Product {row.Title}, ID:{product.id} successfully create.')
            print()
        else:
            print(f'Updating {row.SKU} ...')
            product = Product.objects.get(id=productid)
            product.stock = int(row.Stock)
            product.save()
            if isna(row['Large Image']) is False and 'http' in row['Large Image'] and bool(product.image) is False:
                filename = row.SKU + row['Large Image'][row['Large Image'].rfind('.'):]
                downloadImage(row['Large Image'], filename)
                product.image.save(filename, File(open(filename, 'rb')))
                product.save()
                removefile(filename)
            print(f'Product {product.title} stock update to {product.stock}.')
        print()

def productsstockfull():
    data = read_excel('products-stock-full.xlsx')
    for index, row in data.iterrows():
        print(f'Index:{index}, SKU:{row.SKU}')
        try:
            product = Product.objects.get(sku=row.SKU)
            print(f'Updating {row.SKU} ...')
            product.stock = int(row.Stock)
            product.save()
        except:
            pass
        print()

def catalog():
    data = read_excel('catalog.xlsx')
    for index, row in data.iterrows():
        print(f'Index:{index}, SKU:{row.SKU}')
        # Product
        productid = getid('Product', 'sku', row.SKU)
        if productid is None:
            # Category
            categoryid = getid('Category', 'data', row.Category)
            if categoryid is None:
                # Create Category
                kwargs = {
                    'data': row.Category,
                    'name': row.Category,
                }
                categoryid = create('Category', kwargs).id
                print(f'Category {row.Category}, ID:{categoryid} successfully create.')
            # Device
            deviceid = getid('Device', 'data', row['Product Model'])
            if deviceid is None:
                # Brand
                brandid = getid('Brand', 'data', row.Brand)
                if brandid is None:
                    # Create Brand
                    kwargs = {
                        'data': row.Brand,
                        'name': row.Brand,
                    }
                    brandid = create('Brand', kwargs).id
                    print(f'Brand {row.Brand}, ID:{brandid} successfully create.')
                # Create Device
                kwargs = {
                    'code': row['Group ID'][row['Group ID'].rfind('-')+1:],
                    'data': row['Product Model'],
                    'name': row['Product Model'],
                    'brand_id': brandid,
                }
                deviceid = create('Device', kwargs).id
                print(f"Device {row['Product Model']}, ID:{deviceid} successfully create.")
            # Create Product
            print(f'Creating {row.SKU} ...')
            kwargs = {
                'sku': row.SKU,
                'title': row.Title,
                'stock': int(row.Stock),
                'cost': float(row.Price[1:]),
                'price': getPrice(float(row.Price[1:])),
                'code': None if isna(row['UPC Code']) else row['UPC Code'],
                'device_id': int(deviceid),
                'category_id': int(categoryid),
                'image': None,
            }
            print(kwargs)
            product = create('Product', kwargs)
            product.save()
            if isna(row['Large Image']) is False and 'http' in row['Large Image']:
                filename = row.SKU + row['Large Image'][row['Large Image'].rfind('.'):]
                downloadImage(row['Large Image'], filename)
                product.image.save(filename, File(open(filename, 'rb')))
                product.save()
                removefile(filename)
            print(f'Product {row.Title}, ID:{product.id} successfully create.')
            print()
        else:
            print(f'Updating {row.SKU} ...')
            product = Product.objects.get(id=productid)
            product.stock = int(row.Stock)
            product.cost = float(row.Price[1:])
            product.price = getPrice(float(row.Price[1:]))
            product.save()
            if isna(row['Large Image']) is False and 'http' in row['Large Image'] and bool(product.image) is False:
                filename = row.SKU + row['Large Image'][row['Large Image'].rfind('.'):]
                downloadImage(row['Large Image'], filename)
                product.image.save(filename, File(open(filename, 'rb')))
                product.save()
                removefile(filename)
            print(f'Product {product.title} stock update to {product.stock}.')
        print()