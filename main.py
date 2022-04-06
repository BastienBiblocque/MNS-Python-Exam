import json

from fastapi import Request, FastAPI
from json import JSONDecodeError
# import JSONDecodeError

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import Vehicule

app = FastAPI()

allVehicule = []

allowedType = ['Bateau', 'Voiture', 'Avion', 'Moto']


@app.get('/test')
def univ():
    return {'info': 'L\'api fonctionne !'}


@app.post('/vehicule')
async def postVehicule(request: Request):
    try:
        if request.query_params['type'] in allowedType:
            dataToSend = {
                'type': request.query_params['type'],
                'nom': request.query_params['nom'],
                'marque': request.query_params['marque'],
                'vitesse': request.query_params['vitesse'],
                'km': request.query_params['km'],
            }
            newVehicule = Vehicule.Vehicule(dataToSend)
            newVehicule.save(allVehicule)
            if newVehicule:
                return JSONResponse({"success": 'Element created', 'data': newVehicule.__dict__})
            else:
                return JSONResponse({"error": 'Element not created'})
        else:
            return JSONResponse({"error": 'Type not allowed'})
    except:
        return JSONResponse({'error': 'Il manque un ou plusieurs parametres'})


@app.get('/vehicule')
async def getNumberOfVehicule():
    return JSONResponse({"nombre de véhicule": len(allVehicule)})


@app.get('/vehiculePerType')
async def getNumberOfVehiculePerType(request: Request):
    numberOfElement = 0
    if not 'type' in request.query_params:
        return JSONResponse({"error": 'type is required'})
    for element in allVehicule:
        if getattr(element, 'type') == request.query_params['type']:
            numberOfElement += 1
    return JSONResponse({"nombre du type recherché": numberOfElement})


@app.get('/search')
def searchVehicule(request: Request):
    dataToReturn = []
    for element in allVehicule:
        save = True
        for params in request.query_params:
            if request.query_params[params] != getattr(element, params):
                save = False
        if save:
            dataToReturn.append(element.__dict__)

    if len(dataToReturn) == 0:
        return JSONResponse({"nombre du type recherché": 'Element not found'})
    else:
        return JSONResponse({"nombre du type recherché": dataToReturn})


@app.get('/save')
def save(request: Request):
    if 'FileName' in request.query_params:
        filename = request.query_params['FileName'] + '.txt'
        with open(filename, 'w') as file:
            for element in allVehicule:
                file.write(json.dumps(element.__dict__) + '\n')

        return JSONResponse({"succes": "all save"})
    else:
        return JSONResponse({"error": "FileName is required"})


@app.get('/load')
def load(request: Request):
    if 'FileName' in request.query_params:
        filename = request.query_params['FileName'] + '.txt'
        with open(filename, 'r') as file:
            for line in file:
                data = json.loads(line)
                dataToSend = {
                    'type': data['type'],
                    'nom': data['nom'],
                    'marque': data['marque'],
                    'vitesse': data['vitesse'],
                    'km': data['km'],
                }
                newVehicule = Vehicule.Vehicule(dataToSend)
                newVehicule.save(allVehicule)
        print(allVehicule)
        return JSONResponse({"succes": "all load"})
    else:
        return JSONResponse({"error": "FileName is required"})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse({"message": "Route not found"})
