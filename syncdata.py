import dotenv
import os
import django


dotenv.read_dotenv()
os.environ['DJANGO_SETTINGS_MODULE'] = 'projectfiles.settings'
django.setup()
from downupload.main import download, removefile


# from downupload.main import fullcatalogue
# print('Downloading full-catalogue.xlsx')
# download('https://www.hrwireless.com/download/full-catalogue', 'full-catalogue.xlsx')
# print('Populating full-catalogue.xlsx')
# fullcatalogue()
# print('Removing full-catalogue.xlsx')
# removefile('full-catalogue.xlsx')


from downupload.main import productsstockfull
print('Downloading products-stock-full.xlsx')
download('http://www.hrwireless.com/account/user-downloads/quantity-full/export/excel', 'products-stock-full.xlsx')
print('Populating products-stock-full.xlsx')
productsstockfull()
print('Removing products-stock-full.xlsx')
removefile('products-stock-full.xlsx')


from downupload.main import catalog
# print('Populating catalog.xlsx')
# catalog()
print('Removing catalog.xlsx')
removefile('catalog.xlsx')



# https://www.hrwireless.com/download/full-catalogue (excel)
# http://www.hrwireless.com/account/user-downloads/quantity-full/export/csv
# http://www.hrwireless.com/account/user-downloads/quantity-full/export/excel
# https://www.hrwireless.com/account/user-downloads/catalog/export/csv
# https://www.hrwireless.com/account/user-downloads/catalog/export/excel