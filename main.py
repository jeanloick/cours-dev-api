from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel

api_description = description = """
Guitar API helps you to be a better guitarist

## Guitars

you will be able to : 

* Forge new guitars
* Gets all guitars 
* Refine Guitars
* Delete Guitars T-T

"""

# Liste des tags utilises dans la doc
tags_metadata = [
    {
        "name" : "Guitars",
        "description": "Forge, refine and sell Guitars, the only way to bring more light into this shady world, and there are a doc !!",
        "externalsDocs" : {
            "description": "items external docs",
            "url": "https://fastapi.tiangolo.com/"
        }
    }
]

app = FastAPI(
    title="Guitar API",
    description=api_description,
    openapi_tags= tags_metadata
) #variable names for the server

#Data models / Schema / DTO
class Guitar (BaseModel):
    guitarBrand: str
    guitarType:str
    guitarName: str
    guitarColor: str
    guitarPrice: float
    #availability: bool = True #default / optionnel
    #rating: Optional[int] # completement optionnel


@app.get("/")
async def root():
    return {"message":"with great power comes great responsibility"}

guitarList = [{"guitarBrand":"Gibson", "guitarType":"electric", "guitarName": "flying V 1966", "guitarPrice":1350, "guitarColor": "black"},
              {"guitarBrand":"Gibson","guitarType":"electric", "guitarName": "SG signature Angus YOUNG 1988", "guitarPrice":2988, "guitarColor": "red"}]

@app.get("/guitars", tags=["Guitars"])
async def getGuitars():
    return { "Guitars": guitarList,
              "limits": 10,
              "total": 2,
              "skip": 0
        }
@app.post("/guitars", tags=["Guitars"])
async def create_guitar(payload: Guitar, response: Response, tags=["Guitars"]):
    print(payload.guitarName)
    guitarList.append(payload.dict())

    response.status_code = status.HTTP_201_CREATED
    return {"message": f"Guitar sucessfully added to the flow of metal and rock and roll, his name is : {payload.guitarBrand +' '+ payload.guitarName}, such a great choice ;)"}

@app.get("/guitars/{guitarId}", tags=["Guitars"])
async def getGuitar(guitarId: int, response: Response, tags=["Guitars"]):
    try: 
        correspondingGuitar = guitarList[guitarId -1]# pck ID begin to 1 and index to 0 
        return correspondingGuitar 
    
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "GUitar not found, guitar lost into the void T-T"
        )
    

#DELETE: base du endpoint 

@app.delete("/guitars/{guitarId}", tags=["Guitars"])
async def deleteGuitar(guitarId: int, response: Response):
    try: 
        guitarList.pop(guitarId -1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return 
    
    except: 
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "GUitar not found, guitar lost into the void T-T"
        )

# PUT: ajouter mais sur l'existant

@app.put("/guitars/{guitarId}", tags=["Guitars"])
async def updateGuitar(guitarId: int, payload: Guitar, reposnse: Response):
    try: 
        guitarList[guitarId -1] = payload.dict()
        return  {"message" : f"Guitar successfully refine, bring more light into {payload.guitarName} "}
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "GUitar not found, guitar lost into the void T-T"
        )
