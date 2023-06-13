from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel

api_description = description = """
Guitar's client API helps they become a better guitarist

## Clients

you will be able to : 

* Forge new guitar guys
* Gets all Guitar guys
* Update Client
* Delete Client, a another guitarist who choose bass T-T...

"""

# Liste des tags utilises dans la doc
tags_metadata = [
    {
        "name" : "Clients, Guitarist not bassist ;)!",
        "description": "Add, get, update and delate guitar guy, and there are a doc !!",
        "externalsDocs" : {
            "description": "items external docs",
            "url": "https://fastapi.tiangolo.com/"
        }
    }
]

app = FastAPI(
    title="Client API",
    description=api_description,
    openapi_tags= tags_metadata
) #variable names for the server

#Data models / Schema / DTO
class Client (BaseModel):
    firstName: str
    lastName:str
    adress: str
    email : str
    postalCode: int
    payementInfo: str 


clientList = [{"firstName":"Jerry", "lastName":"Tyler", "adress": "1 rue du pont", "email": "jerry@gmail.com" , "postalCode": 85521, "payementInfo": "ici se retrouveras les info des payements"},
              {"firstName":"Rick", "lastName":"Grames", "adress": "the commonwelth, sector 2", "email": "rick@gmail.com" , "postalCode": 45632, "payementInfo": "ici se retrouveras les info des payements"}]

#Get Clients

@app.get("/clients", tags=["Client"])
async def getClients():
    return { "Clients": clientList,
              "limits": 10,
              "total": 2,
              "skip": 0
        }

# Create Clients

@app.post("/clients", tags=["Client"])
async def createClient(payload: Client, response: Response):
    print(payload.firstName)
    clientList.append(payload.dict())

    response.status_code = status.HTTP_201_CREATED
    return {"message": f"Client sucessfully added, his name is : Mr/Ms {payload.firstName +' '+ payload.lastName}"}


# Get specific user 

@app.get("/clients/{clientId}", tags=["Client"])
async def getclient(clientId: int, payload : Client, response: Response ):
    try: 
        correspondingClient = clientList[clientId -1]# pck ID begin to 1 and index to 0 
        return correspondingClient 
    
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=  { f"client not found, Mr/Ms {payload.firstName +' '+ payload.lastName} is lost into NightCity T-T"} 
        )



# Delete Clients

@app.delete("/clients/{clientId}", tags=["Client"])
async def deleteClient(clientId: int, payload: Client, response: Response):
    try: 
        clientList.pop(clientId -1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return 
    
    except: 
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=  { f"client not found, Mr/Ms {payload.firstName +' '+ payload.lastName} is lost into NightCity T-T"} 
        )



#Put Clients 

@app.put("/clients/{clientId}", tags=["Client"])
async def updateClient(clientId: int, payload: Client, reposnse: Response):
    try: 
        clientList[clientId -1] = payload.dict()
        return  {"message" : f"Guitar successfully refine, bring more light into {payload.firstName} "}
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=  { f"client not found, Mr/Ms {payload.firstName +' '+ payload.lastName} is lost into NightCity T-T"} 
        )
