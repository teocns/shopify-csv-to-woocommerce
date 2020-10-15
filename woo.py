import os
import json
import random
import re
from helpers import genSku,appendToCsv,debug


# Generate row from raw line
def genRow(rawLine):
    ret = {}
    lineArr = re.compile(r',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)').split(rawLine)
    
    for i in range(0,len(columnNames)):
        try:
            ret[columnNames[i]] = lineArr[i]
        except:
            pass
            
    return ret


shopify_csv_raw = ""

with open('shopify.csv','r',encoding="utf-8") as f:
    shopify_csv_raw = f.read()

shopify_csv_lines = shopify_csv_raw.split("\n")

# Extract first row from CSV
columnNames = shopify_csv_lines[0].split(',')


#genRow(columnNames,shopify_csv_lines[1])
csv_created = False
current_child_index = 0
woo_rows = [] # Contains all the generated rows relative to the product
master_row = {}
for i in range(1,len(shopify_csv_lines)):
    cur_line = shopify_csv_lines[i]
    cur = genRow(cur_line)
    woo_row = {}
    try:
        if cur['Title']:
            variant_found = False
            # Master round found. If there was a previous one, delete it.
            if current_child_index > 0:
                master_row['Images'] = "\""+master_row['Images']+"\""
                appendToCsv(woo_rows, True if not csv_created else False)
                csv_created = True
                woo_row = {}
                woo_rows = []
            current_child_index = 0
            woo_row['Type'] = "variable"
            woo_row['SKU'] = genSku()
            woo_row['Name'] = cur['Title']
            woo_row['Published'] = 1
            woo_row['Is featured?'] = 0
            woo_row['Visibility in catalog'] = 'visible'
            woo_row['Short description'] = ''
            woo_row['Description'] = cur['Body (HTML)']
            woo_row['Tax status'] = 'none'
            woo_row['Tax class'] = ''
            woo_row['In stock?'] = '1'
            woo_row['Sold individually?'] = '0'
            woo_row['Weight (kg)'] = str(round(random.randint(2900,3900)/1000,2))
            woo_row['Allow customer reviews?'] = 1
            woo_row['Categories'] = cur['Vendor'].upper() if 'Vendor' in cur else ''
            woo_row['Tags'] = "\""+ (", ".join(cur['Vendor'].split(" ")) + ", " + ", ".join(cur['Title'].split(" ")) if 'Vendor' in cur else ", ".join(cur['Title'].split(" "))).strip(',') + "\""
            woo_row['Images'] = cur['Image Src'] if 'Image Src' in cur else '' # We're also adding the rest later as we're iterating over children variants
            woo_row['Parent'] = "" # Empty as this is master element / not variant
            woo_row['Sale price'] = '' # Empty as this is master element / not variant
            woo_row['Regular price'] = '' # Empty as this is master element / not variant
            woo_row['Position'] = current_child_index # Grows with each variant
            woo_row['Attribute 1 name'] = 'Size'
            woo_row['Attribute 1 value(s)'] = "\"US 7 - EU 40,US 7.5 - EU 40.5,US 8 - EU 41,US 8.5 - EU 42,US 9 - EU 42.5,US 9.5 - EU 43,US 10 - EU 44,US 10.5 - EU 44.5,US 11 - EU 45,US 11.5 - EU 45.5,US 12 - EU 46,US 12.5 - EU 47,US 13 - EU 47.5,US 13.5 - EU 48,US 14 - EU 48.5\""
            woo_row['Attribute 1 visible'] = 1 # HIDDEN on VARIANT
            woo_row['Attribute 1 global'] = 0
            woo_row['Attribute 1 default'] = cur['Option1 Value']
            master_row = woo_row
        else: 
            current_child_index += 1
            woo_row['Type'] = "variation"
            woo_row['SKU'] = ''
            woo_row['Name'] = master_row['Name'] + ' - ' + cur['Option1 Value']
            woo_row['Published'] = str(1)
            woo_row['Is featured?'] = str(0)
            woo_row['Visibility in catalog'] = 'visible'
            woo_row['Short description'] = ''
            woo_row['Description'] = cur['Body (HTML)']
            woo_row['Tax status'] = 'none'
            woo_row['Tax class'] = 'parent'
            woo_row['In stock?'] = '1'
            woo_row['Sold individually?'] = '0'
            woo_row['Weight (kg)'] = str(round(random.randint(2900,3900)/1000,2))
            woo_row['Allow customer reviews?'] = 1
            woo_row['Categories'] = master_row['Categories'].upper()
            woo_row['Tags'] =   "\"" + (", ".join(master_row['Categories'].split(" ")) + ", " + ", ".join(master_row['Name'].split(" "))).strip(',') + "\""
            woo_row['Images'] = '' 
            woo_row['Parent'] = master_row['SKU'] # Empty as this is master element / not variant
            woo_row['Sale price'] = str(cur['Variant Price']) # Empty as this is master element / not variant
            woo_row['Regular price'] = str(cur['Variant Compare At Price']) # Empty as this is master element / not variant
            woo_row['Position'] = str(current_child_index) # Grows with each variant
            woo_row['Attribute 1 name'] = 'Size'
            woo_row['Attribute 1 value(s)'] = cur['Option1 Value']
            woo_row['Attribute 1 visible'] = '' # HIDDEN on VARIANT
            woo_row['Attribute 1 global'] = str(0)
            woo_row['Attribute 1 default'] = ''
            master_row['Images'] += "," + cur['Image Src'] if len(cur['Image Src']) > 0 else ''
    except Exception as ex:
        raise ex
        exit(cur)
    woo_rows.append(woo_row)

        

        

    
    
