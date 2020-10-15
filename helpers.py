import random
import json






def genSku():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    return ''.join(''.join(random.choice(seq) for _ in range(5)) for _ in range(2))
    
    
    
def debug(data):
    exit(
        json.dumps(
            data,
            indent=4,
            sort_keys =  True
        )
    )
    
def appendToCsv(rows,create = False):
    text = "" if not create else 'Type,SKU,Name,Published,Is featured?,Visibility in catalog,Short description,Description,Tax status,Tax class,In stock?,Sold individually?,Weight (kg),Allow customer reviews?,Categories,Tags,Images,Parent,Sale price,Regular price,Position,Attribute 1 name,Attribute 1 value(s),Attribute 1 visible,Attribute 1 global,Attribute 1 default\n'
    
    for row in rows:
        vals = []
        for k in row:
            vals.append(str(row[k]))
        text += ",".join(vals)+"\n"
        vals = []    
    
    with open('woo.csv','w+' if create else 'a') as f:
        f.write(text)