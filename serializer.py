import random
import json
import re



# ================================================  HELPERS  =================================================
def genSku():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    return ''.join(''.join(random.choice(seq) for _ in range(5)) for _ in range(2))
def clamp(n, minn, maxn):
    return round(float(max(min(maxn, n), minn)),1)
# ============================================================================================================




class WooCommerceProduct:
    title = ""
    real_link = ""
    image_links = []
    real_price = 0.00
    description = ""
    category = ""
    variants = {
        'Size': ['US 7 - EU 40', 'US 7.5 - EU 40.5', 'US 8 - EU 41', 'US 8.5 - EU 42', 'US 9 - EU 42.5', 'US 9.5 - EU 43', 'US 10 - EU 44', 'US 10.5 - EU 44.5', 'US 11 - EU 45', 'US 11.5 - EU 45.5', 'US 12 - EU 46', 'US 12.5 - EU 47', 'US 13 - EU 47.5', 'US 13.5 - EU 48', 'US 14 - EU 48.5']
    }    
    
    
    
    def __init__(
        self,
        real_link,
        title,
        image_links,
        real_price,
        description,
        category
        ):
        self.title = title
        self.real_link = real_link
        self.image_links = image_links
        self.real_price = real_price
        self.description = description
        self.category = category
        self.weight = str(round(random.randint(2900,3900)/1000,2))
        # Generate price
        try:
            
            if self.real_price < 120:
                self.price = clamp(int(self.real_price * 0.55),30,70)
            elif self.real_price < 200:
                    self.price = clamp(
                        int(self.real_price * 0.45),40,80
                    )
            elif self.real_price < 500:
                self.price = clamp(
                    int(self.real_price * 0.35),50,90
                )
            else:
                self.price = clamp(
                    int(self.real_price * 0.25),65,125
                )
        except Exception as ex:
            self.price = random.randint(75,110)



    def generateCsvLines(self,OUTPUT_FILE):
        # Check if output file has the columns header
        check_line = ""
        with open(OUTPUT_FILE,'r') as f:
            check_line = f.readline().strip()
        columns_header = 'Type,SKU,Name,Published,Is featured?,Visibility in catalog,Short description,Description,Tax status,Tax class,In stock?,Sold individually?,Weight (kg),Allow customer reviews?,Categories,Tags,Images,Parent,Sale price,Regular price,Position,Attribute 1 name,Attribute 1 value(s),Attribute 1 visible,Attribute 1 global,Attribute 1 default'
        if not columns_header in check_line:
            with open(OUTPUT_FILE,'w') as f:
                f.write(columns_header+"\n") # Don't forget the newline char
        
        
        
        # Rows that will be appeneded to CSV
        append_rows = []
        
        # Generate master row
        master_row = {}
        master_row['Type'] = "variable"
        master_row['SKU'] = genSku()
        master_row['Name'] = self.title
        master_row['Published'] = 1
        master_row['Is featured?'] = 0
        master_row['Visibility in catalog'] = 'visible'
        master_row['Short description'] = ''
        master_row['Description'] = self.description
        master_row['Tax status'] = 'none'
        master_row['Tax class'] = ''
        master_row['In stock?'] = '1'
        master_row['Sold individually?'] = '0'
        master_row['Weight (kg)'] = self.weight
        master_row['Allow customer reviews?'] = 1
        master_row['Categories'] = self.category.upper() 
        master_row['Tags'] = "\""+ ", ".join(self.category.split(" ")) + ", " + ", ".join(self.category.split(" ")) + "\""
        master_row['Images'] = "\"" + ",".join(self.image_links) + "\""
        master_row['Parent'] = "" # Empty as this is master element / not variant
        master_row['Sale price'] = '' # Empty as this is master element / not variant
        master_row['Regular price'] = '' # Empty as this is master element / not variant
        master_row['Position'] = 0 # Grows with each variant
        master_row['Attribute 1 name'] = 'Size'
        master_row['Attribute 1 value(s)'] = "\""+ ",".join(self.variants['Size']) +"\""
        master_row['Attribute 1 visible'] = 1 # HIDDEN on VARIANT
        master_row['Attribute 1 global'] = 0
        master_row['Attribute 1 default'] = self.variants['Size'][0]
        
        append_rows.append(master_row)
        # Each variant has a different row
        for i in range(0,len(self.variants['Size'])):
            cur_variant = self.variants['Size'][i]
            woo_row['Type'] = "variation"
            woo_row['SKU'] = ''
            woo_row['Name'] = master_row['Name'] + ' - ' + self.['Option1 Value']
            woo_row['Published'] = str(1)
            woo_row['Is featured?'] = str(0)
            woo_row['Visibility in catalog'] = 'visible'
            woo_row['Short description'] = ''
            woo_row['Description'] = self.description
            woo_row['Tax status'] = 'none'
            woo_row['Tax class'] = 'parent'
            woo_row['In stock?'] = '1'
            woo_row['Sold individually?'] = '0'
            woo_row['Weight (kg)'] = self.weight
            woo_row['Allow customer reviews?'] = 1
            woo_row['Categories'] = master_row['Categories'].upper()
            woo_row['Tags'] =   "\"" + (", ".join(master_row['Categories'].split(" ")) + ", " + ", ".join(master_row['Name'].split(" "))).strip(',') + "\""
            woo_row['Images'] = '' 
            woo_row['Parent'] = master_row['SKU'] # Empty as this is master element / not variant
            woo_row['Sale price'] = str() # Empty as this is master element / not variant
            woo_row['Regular price'] = str(self.real_price) # Empty as this is master element / not variant
            woo_row['Position'] = str(i+1) # Grows with each variant
            woo_row['Attribute 1 name'] = 'Size'
            woo_row['Attribute 1 value(s)'] = cur_variant
            woo_row['Attribute 1 visible'] = '' # HIDDEN on VARIANT
            woo_row['Attribute 1 global'] = str(0)
            woo_row['Attribute 1 default'] = ''