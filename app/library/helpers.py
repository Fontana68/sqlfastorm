import os.path
import markdown

fruits =  {
        "page": 1 ,
        "vehicle" : {
            "vin": "TMB345234533453",
            "regNum": "CA33456CB",
            "category": "M"
        }
    }

def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "vehicle" : fruits,
        "text": html
    }
    return data
