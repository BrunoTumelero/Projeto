from pandas.core.frame import DataFrame
import requests, json, re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen

url_base = 'https://www.saloncentric.com/'

def request_data(url, tag, attr):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    data = bs.find_all(tag, {"class": attr})
    return data

data = request_data(url_base, 'div', 'sub_nav_left')
all_categories = {}
products = DataFrame()
prod_name, price, brand, sku = [], [], [], []

for categories in data:
    cat_array = categories.findChildren("a", {"level_2_left_link link nav_l2"})
    for cat in cat_array:
        category_name = (cat.text)
        ##Replace every white-space character with none data:
        category_name = re.sub('\s', '', category_name)
        all_categories[category_name] = cat.get("href").replace('\n', '')
        cat_url = url_base + cat.get("href").replace('\n', '')
        
        """
        ## NORMALIZAÇÃO DE DADOS MANUAL
        prod_data = request_data(cat_url, 'div', 'page_context_data')
        for prod in prod_data:
        #prod_data = prod_data.text
        #print(prod_data)
            prod = re.sub('<div class="page_context_data"><!--', '', str(prod))
            prod = re.sub('--></div>', '', prod)
            #prod = prod.replace("\\", '')
        """

        html = """<div class="page_context_data"><!--{"trackerData":{"pageID":"Category: Hair Care","categoryID":"hair-care","searchString":"","searchResults":0,"productCategory":"Hair Care","categoryBreakout":"Home  Hair Care","advanceEcommerce":{"advanceImpressions":[{"price":"2.5","brand":"Biolage","name":"ColorLast Shampoo","variant":"884486151551","id":"SCMX-BIOLAGE-COLORLASTshamp","category":"Curated Stores / Spice It Up Sale","manufacturerSKU":null,"list":"list-result-range","position":6},{"price":"60","brand":"Olaplex","name":"Bond Maintenance Conditioner No.5","variant":"896364002565","id":"SCOLP-BondCond","category":"Hair Care / Conditioner","manufacturerSKU":null,"list":"list-result-range","position":7},{"price":"2.5","brand":"Biolage","name":"ColorLast Conditioner","variant":"884486151643","id":"SCMX-BIOLAGE-COLORLASTcond","category":"Curated Stores / Spice It Up Sale","manufacturerSKU":null,"list":"list-result-range","position":8},{"price":"23.18","brand":"Pureology","name":"Color Fanatic Multi-Tasking Leave-In Spray","variant":"884486437877","id":"pureology-color-fanatic-spray","category":"Hair Care / Treatment / Leave-In","manufacturerSKU":null,"list":"list-result-range","position":9},{"price":"14","brand":"Olaplex","name":"Bond Maintenance Shampoo No.4","variant":"896364002428","id":"SCOLP-BondShamp","category":"Hair Care / Shampoo","manufacturerSKU":null,"list":"list-result-range","position":10},{"price":"11.85","brand":"Redken","name":"Color Extend Magnetics Sulfate Free Shampoo for Color Treated Hair","variant":"884486453327","id":"redken-color-extend-magnetics-shampoo","category":"Hair Care / Shampoo","manufacturerSKU":null,"list":"list-result-range","position":11},{"price":"22","brand":"Biolage","name":"HydraSource Moisturizing Conditioning Balm for Dry Hair","variant":"884486151384","id":"biolage-hydrasource-moisturizing-conditioning-balm","category":"Curated Stores / Spice It Up Sale","manufacturerSKU":null,"list":"list-result-range","position":12},{"price":"11.85","brand":"Redken","name":"Color Extend Magnetics Sulfate Free Conditioner for Color Treated Hair","variant":"884486453310","id":"redken-color-extend-magnetics-conditioner","category":"Hair Care / Conditioner","manufacturerSKU":null,"list":"list-result-range","position":13},{"price":"2.5","brand":"Biolage","name":"HydraSource Moisturizing Shampoo for Dry Hair","variant":"884486151346","id":"biolage-hydrasource-moisturizing-shampoo","category":"Curated Stores / Spice It Up Sale","manufacturerSKU":null,"list":"list-result-range","position":14},{"price":"4.38","brand":"Pureology","name":"Hydrate Shampoo","variant":"884486437136","id":"pureology-hydrate-shampoo","category":"Hair Care / Shampoo","manufacturerSKU":null,"list":"list-result-range","position":15},{"price":"13.39","brand":"Pureology","name":"Hydrate Conditioner","variant":"884486437167","id":"pureology-hydrate-conditioner","category":"Hair Care / Conditioner","manufacturerSKU":null,"list":"list-result-range","position":16},{"price":"10","brand":"Biolage","name":"HydraSource Detangling Solution for Dry Hair","variant":"884486152244","id":"biolage-hydrasource-detangling-solution","category":"Curated Stores / Cyberbusters","manufacturerSKU":null,"list":"list-result-range","position":17},{"price":"8.5","brand":"Matrix","name":"So Silver Color Depositing Purple Shampoo for Blonde and Silver Hair","variant":"884486228055","id":"matrix-total-results-so-silver-purple-shampoo","dimension23":"Total Results","category":"Hair Care / Shampoo","manufacturerSKU":null,"list":"list-result-range","position":18},{"price":"14","brand":"Olaplex","name":"Bond Smoother No.6 3.3 oz.","variant":"896364002602","id":"896364002602","category":" / Chain Custom Catalogs / Sassoon Salons / chain-sassoon-subcategory","manufacturerSKU":"PP073888","list":"list-result-range"},{"price":"16","brand":"Biolage","name":"Ultra HydraSource Moisturizing Shampoo for Very Dry Hair","variant":"884486151278","id":"biolage-ultra-hydrasource-moisturizing-shampoo-for-dry-hair","category":"Curated Stores / Cyberbusters","manufacturerSKU":null,"list":"list-result-range"},{"price":"15.45","brand":"Redken","name":"All Soft™ Shampoo with Argan Oil for Dry Hair","variant":"884486452948","id":"redken-all-soft-moisturizing-shampoo","category":"Hair Care / Shampoo","manufacturerSKU":null,"list":"list-result-range"},{"price":"15.45","brand":"Redken","name":"All Soft™ Conditioner with Argan Oil for Dry Hair","variant":"884486452931","id":"redken-all-soft-moisturizing-conditioner","category":"Hair Care / Conditioner","manufacturerSKU":null,"list":"list-result-range"},{"price":"14","brand":"Olaplex","name":"No. 4P Blonde Enhancer™ Toning Shampoo","variant":"850018802192","id":"olaplex-4p-shampoo","category":"Brands / Olaplex / Hair Care / Shampoo","manufacturerSKU":null,"list":"list-result-range"}]},"ecommerce":{"impressions":[]},"refinements":["","","Category Page: Items Per Page: 18"],"pageType":"Product Category","itemsPerPage":18,"totalItems":985},"currentPage":"plp","showAddToCart":false,"og_frequency":""}--></div>"""
        soup = BeautifulSoup(html, 'html.parser')
        res = soup.find('div')
        json_object = json.loads(res.contents[0])
        #print(json_object)

        for data in json_object["trackerData"]["advanceEcommerce"]["advanceImpressions"]:
            prod_name.append(data["name"])
            price.append(data["price"])
            brand.append(data["brand"])
            sku.append(None)
        
products['Product name'] = pd.Series(prod_name, dtype=str)
products['Price'] = pd.Series(price, dtype=str)
products['Brand'] = pd.Series(brand, dtype=str)
products['SKU'] = pd.Series(sku, dtype=str)

df = pd.DataFrame(
    all_categories,
    index=["Links"],
    dtype="category"
)
df = df.T

products.to_csv('info.csv', encoding='utf-8')

print("Informações coletadas!")
with open('products.json', 'w', encoding= 'utf8') as jFile:
    json.dump(json_object, jFile, indent= 2)
        
with open('products.json', 'r') as jFile:
    json_data = json.loads(jFile)

df = pd.DataFrame(all_categories, index=[np.arange(1)])
print(df)