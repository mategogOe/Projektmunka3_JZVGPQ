import xml.etree.ElementTree as et
import pandavro as pdx
import pandas as pd
from forex_python.converter import CurrencyRates

def readfromxmltodict(path):
    # beolvassuk az XML fájlt
    tree = et.parse(path)
    root = tree.getroot()

    c = CurrencyRates()
    Currency = c.get_rate('USD', 'HUF')  #convert USD to HUF
    print(Currency)

    data = {}
    # gyűjtsük ki az adatokat az XML-ből
    i = 0
    for child in root:
        data[i] = []
        for ch in child:
            if(ch.tag == "price"):
                seged = ch.text
                ch.text = str(int(round(float(seged) * Currency)))
                data[i].append(ch.text + " HUF")
                print(data[i])
            data[i].append(ch.text)
        i+=1
    return data

dictData = readfromxmltodict("C:\\Users\\GógMáté\\Documents\\ProjMunka3\\bookstore.xml")

OUTPUT_PATH="C:\\Users\\GógMáté\\Documents\\ProjMunka3\\bookstore.avro"
y = 0
for x in dictData:
    pdx.to_avro(OUTPUT_PATH, pd.DataFrame.from_dict(dictData[y]))
    y+=1
    saved = pdx.read_avro(OUTPUT_PATH)
    print(saved)
    
print(pd.DataFrame.from_dict(dictData[1]))
