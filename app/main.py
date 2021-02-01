from fastapi import FastAPI, Request, HTTPException
from fastapi import Form, File, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from app.routers import twoforms, unsplash, accordion
from starlette.responses import RedirectResponse

from typing import Optional, List
from pydantic import BaseModel, Field

app = FastAPI(debug = True)

templates = Jinja2Templates(directory = "templates")

app.mount("/static", StaticFiles(directory = "static"), name = "static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)

# my_num = 235478.875425
# s = "{:, .2f}".format(my_num)
# print(s)
    

@app.get("/")
def main():
    return RedirectResponse(url = "/api/inspection/current/")


'''
@app.get("/", response_class = HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("page.html", {"request": request, "data": fruits})


@app.get("/page/{page_name}", response_class = HTMLResponse)
async def page(request: Request, page_name: str):
    data = {
        "vehicle": page_name
    }
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
'''
'''
@app.get("/", response_class = HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
    
@app.get("/page/{page_name}", response_class = HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
'''
# ##################################################################

veicolo =  {
        "inspectionId": "3245345" , 
        "vehicle" : {
            "vin": "W322345234533453", 
            "regNum": "BL123AJ", 
            "category": "M", 
            "firstRegistrationDate" : "2011-12-24", 
            "fuelType" : "Diesel", 
            "environmentalCategory": "Euro5",
            "measurements" : {
                "brakesParameters": {
                    "numberOfAxles": 4,
                    "brakeSystem": {
                        "systemType": 1,
                        "minBrakeSystemEfficacy": 1,
                        "pneumaticBrakePressure": 4,
                        "maxPermitedLadenMass": 3000
                    },
                    "handBrakeSystem": {
                        "minHandBrakeSystemEfficacy": 2,
                        "maxBrakingForceInequality": 0.3
                    }
                },
                "opacitySmokeParameters" : {
                    "engineType": 1, 
                    "maxOpacityValue": 2.35, 
                    "minEngineOilTemperature" : 45.0
                },    
                "gasEmissionsParameters" : {
                    "engineType": 2, 
                    "maxCOValue": 0.85, 
                    "minEngineOilTemperature" : 51.0, 
                    "minRPM" : 750
                }    
            }
        }
    }

provatestOPA = {
    "regNum": "BL123AJ", 
    "measurements" : [
        {
            "opacitySmokeResult": 1.2, 
            "rpmResult": 1892, 
            "engineOilTemperature" : 78.4
        }, 
        {
            "opacitySmokeResult": 2.56, 
            "rpmResult": 2100, 
            "engineOilTemperature" : 81.4
        }
    ]
}

provatestGAS = {
    "regNum": "BL123AJ", 
    "measurements" : [
        {
            "rpmResult": 1200, 
            "engineOilTemperature" : 78.4, 
            "copercent": 0.34, 
            "co2Percent": 7.4, 
            "o2Percent": 2.2, 
            "lambda": 0.987        
        }, 
        {
            "rpmResult": 1200, 
            "engineOilTemperature" : 78.4, 
            "copercent": 0.34, 
            "co2Percent": 7.4, 
            "o2Percent": 2.2, 
            "lambda": 0.987        
        }
    ]
}

provatestOBD = {
    "oilTemp": 91.6, 
    "rpm": 890
}


import random
import csv
import os
from time import gmtime, strftime
from datetime import datetime, time, timedelta

timestampOPA : List[dict] = []
timestampGAS : List[dict] = []
timestampOBD : List[dict] = []

# returns all fruit list
@app.get("/api/inspection/current")
async def veh_data():

    # miamisura.clear()
    timestampOPA.clear()
    timestampGAS.clear()
    timestampOBD.clear()

    # numero =  random.randint(0, 10)
    # if numero in range(8):
    return veicolo
    #elif numero == 9:
    #    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = None)
    #else:
    #    raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Something went wrong")


# field names
fieldsOBD = ['timestamp', 'oilTemp', 'rpm']

dialect = csv.excel
dialect.delimiter = ';'
dialect.quotechar = '"'
dialect.lineterminator = '\n'

# GAS -----------------------------------
class MisuraLiveGAS(BaseModel):
    location: str
    manufacturer: str
    model: str
    serialNumber: str
    softwareVersion: Optional[str] = None
    deviceRemark: Optional[str] = None
    coPercent: float
    co2Percent: float
    o2Percent: float
    hc : int
    rpmResult: int
    engineOilTemperature: int
#    Lambda: float = Field(..., alias = 'lambda')        


@app.post("/api/inspection/current/measurement/gas-emissions/live")
async def create_prova4(prova: MisuraLiveGAS):
    elemtimestamp = prova.dict() # Misura do dict
    now = datetime.now() # current date and time
    mio = "{:03d}".format(int(now.microsecond / 1000.0) )
    elemtimestamp["timestamp"] = now.strftime("%H:%M:%S.") + mio

    timestampGAS.append(elemtimestamp)

    return prova

# OPA -----------------------------------
class MisuraLiveOPA(BaseModel):
    location: str
    manufacturer: str
    model: str
    serialNumber: str
    softwareVersion: Optional[str] = None
    deviceRemark: Optional[str] = None
    opacitySmokeResult: float
    rpmResult: int
    engineOilTemperature: float

@app.post("/api/inspection/current/measurement/opacity-smoke/live")
async def create_prova2(prova: MisuraLiveOPA):
    elemtimestamp = prova.dict() # Misura do dict
    now = datetime.now() # current date and time
    mio = "{:03d}".format(int(now.microsecond / 1000.0) )
    elemtimestamp["timestamp"] = now.strftime("%H:%M:%S.") + mio

    timestampOPA.append(elemtimestamp)
    return prova


# OBD -----------------------------------
class MisuraLiveOBD(BaseModel):
    oilTemp: float
    rpm: int

@app.post("/api/inspection/current/live")
async def create_prova5(prova: MisuraLiveOBD):
    elemtimestamp = prova.dict() # Misura do dict
    now = datetime.now() # current date and time
    mio = "{:03d}".format(int(now.microsecond / 1000.0) )
    elemtimestamp["timestamp"] = now.strftime("%H:%M:%S.") + mio

    timestampOBD.append(elemtimestamp)

    return prova

# GAS ---------------------------------------------------
from enum import IntEnum

class FuelName(IntEnum):
    benzina = 1
    gpl = 2
    metano = 3

class MisuraGAS(BaseModel):
    coPercent: float
    co2Percent: float
    o2Percent: float
    hc : int
    airRatioLambda : float
    rpmResult: int
    engineOilTemperature: int
    fuelType: FuelName
#    Lambda: float = Field(..., alias = 'lambda')        

class ProvaGAS(BaseModel):
    location: str
    conductedDatetime: datetime
    manufacturer: str
    model: str
    serialNumber: str
    softwareVersion: Optional[str] = None
    deviceRemark: Optional[str] = None
    regNum: str
    measurements: List[MisuraGAS] = []

fieldsGAS = ['timestamp', 'location', 'manufacturer', \
            'model', 'serialNumber', 'softwareVersion', 'deviceRemark', \
            'coPercent', 'co2Percent', 'o2Percent', 'hc', 'rpmResult', 'engineOilTemperature']

@app.post("/api/inspection/current/measurement/gas-emissions")
async def create_prova3(prova: ProvaGAS):
    if os.path.exists('TestUfficialeGAS.csv'):
        os.remove('TestUfficialeGAS.csv')
    with open('TestUfficialeGAS.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldsGAS, dialect = dialect)
        writer.writeheader()
        for lll in timestampGAS:
            writer.writerow(lll)

    if os.path.exists('TestUfficialeOBD.csv'):
        os.remove('TestUfficialeOBD.csv')
    if bool(timestampOBD) is True:
        with open('TestUfficialeOBD.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fieldsOBD, dialect = dialect)
            writer.writeheader()
            for lll in timestampOBD:
                writer.writerow(lll)

    for elem in prova.measurements:
        print(elem.dict())

    return prova


###########################################
class MisuraOPA(BaseModel):
    opacitySmokeResult: float
    rpmResult: int
    engineOilTemperature: float

class ProvaOPA(BaseModel):
    location: str
    conductedDatetime: datetime
    manufacturer: str
    model: str
    serialNumber: str
    softwareVersion: Optional[str] = None
    deviceRemark: Optional[str] = None
    regNum: str
    measurements: List[MisuraOPA] = []

fieldsOPA = ['timestamp', 'location', 'manufacturer', \
            'model', 'serialNumber', 'softwareVersion', 'deviceRemark', \
            'opacitySmokeResult', 'rpmResult', 'engineOilTemperature']

# OPA -----------------------------------
@app.post("/api/inspection/current/measurement/opacity-smoke")
async def create_prova(prova: ProvaOPA):
    if os.path.exists('TestUfficialeOPA.csv'):
        os.remove('TestUfficialeOPA.csv')
    with open('TestUfficialeOPA.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldsOPA, dialect = dialect, )
        writer.writeheader()
        for lll in timestampOPA:
            writer.writerow(lll)

    if os.path.exists('TestUfficialeOBD.csv'):
        os.remove('TestUfficialeOBD.csv')
    if bool(timestampOBD) is True:
        with open('TestUfficialeOBD.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fieldsOBD, dialect = dialect)
            writer.writeheader()
            for lll in timestampOBD:
                writer.writerow(lll)

    for elem in prova.measurements:
        print(elem.dict())

    return prova


# type annotazione
#miamisura = List[MisuraOPA]

#aa : MisuraOPA = MisuraOPA(opacitySmokeResult = 1.2, rpmResult = 1000, engineOilTemperature = 12.8)
# print(aa.engineOilTemperature)
#bb : MisuraOPA = MisuraOPA(opacitySmokeResult = 2.2, rpmResult = 2000, engineOilTemperature = 13.8)
#cc : MisuraOPA = MisuraOPA(opacitySmokeResult = 4.2, rpmResult = 4000, engineOilTemperature = -12.8)
#x : miamisura = [aa, bb]
#x.append(cc)
# print(x)
# for lll in x:
#     print(lll.dict())




# http://localhost:8000/getuser/defaultuser?user_id=123
@app.get("/getuser/{username}/")  # path + query
async def index(username: str, user_id: int):
    return {"username": username, 'user_id': user_id}


from pydantic import BaseModel

class Basic(BaseModel):
    username : str
    userid : int
    designation : str
    pay : float    


# We are just returning the request body as a response
# Note the status code imported from status module
@app.post("/user/createuser", status_code = status.HTTP_201_CREATED)
async def create_user(user: Basic):
    return user

@app.post("/user/createuser2", status_code = status.HTTP_201_CREATED)
async def create_user2(username: str = Form(...), password: str = Form(..., min_length = 8)):
    return username

from fastapi import FastAPI, File, UploadFile


@app.post("/files/uploadfile", status_code = status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    return {"message": " Valid file uploaded", "filetype": file.content_type}

# Uploading a pdf file 
# API : http://localhost:8000/files/uploadfile    