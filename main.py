from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import  RealDictCursor

# Connexion DB

connexion = psycopg2.connect(
    host="dpg-ci8rn3liuie0h35b9g30-a.frankfurt-postgres.render.com",
    database="guitar_center_render",
    user="geralt",
    password="slSywIr6hJQXXk72eaC0bewLDpA9qvgk",
    cursor_factory=RealDictCursor
)
cursor= connexion.cursor() # TODO  modifs à faire

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
    availability: bool = False #default / optionnel
    #rating: Optional[int] # completement optionnel


@app.get("/")
async def root():
    return {"message":"with great power comes great responsibility"}

guitarList = [{"guitarBrand":"Gibson", "guitarType":"electric", "guitarName": "flying V 1966", "guitarPrice":1350, "guitarColor": "black"},
              {"guitarBrand":"Gibson","guitarType":"electric", "guitarName": "SG signature Angus YOUNG 1988", "guitarPrice":2988, "guitarColor": "red"}]

@app.get("/guitars", tags=["Guitars"])
async def getGuitars():

    cursor.execute("SELECT * FROM guitar")

    dbGuitars= cursor.fetchall()

    return { "Guitars":  dbGuitars,
              #"limits": 10,
              #"total": 2,
             #"skip": 0
        }
@app.post("/guitars", tags=["Guitars"])
async def create_guitar(payload: Guitar, response: Response, tags=["Guitars"]):
   # cursor.execute(f"INSERT INTO guitar (name,brand,type,color,price,availability) VALUES ('{payload.guitarName}','{payload.guitarBrand}','{payload.guitarType}','{payload.guitarColor}',{payload.guitarPrice},{payload.availability}) RETURNING*;")
    cursor.execute ("INSERT INTO guitar (name,brand,type,color,price,availability) VALUES (%s,%s,%s,%s,%s,%s) RETURNING*;", (payload.guitarName, payload.guitarBrand, payload.guitarType, payload.guitarColor, payload.guitarPrice, payload.availability))
    connexion.commit() # Sauvegarde dans la base de donnée

    response.status_code = status.HTTP_201_CREATED
    return {"message": f"Guitar sucessfully added to the flow of metal and rock and roll, his name is : {payload.guitarBrand +' '+ payload.guitarName}, such a great choice ;)"}

@app.get("/guitars/{guitarId}", tags=["Guitars"])
async def getGuitar(guitarId: int, response: Response, tags=["Guitars"]):
    try: 
        cursor.execute(f"SELECT * FROM guitar WHERE id={guitarId}")
        correspondingGuitar = cursor.fetchone()
        if(correspondingGuitar):
            return correspondingGuitar
        else:
            raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Guitar not found, guitar lost into the void T-T"
        )
            
    
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Guitar not found, guitar lost into the void T-T"
        )
    

#DELETE: base du endpoint 

@app.delete("/guitars/{guitarId}", tags=["Guitars"])
async def deleteGuitar(guitarId: int, response: Response):
    try: 
         cursor.execute(
        'DELETE FROM guitar WHERE id=%s RETURNING *', (guitarId,)
        )
         connexion.commit()
         return {"message": f"Guitar succes... sucessfully destroy .... why?"}
    
    except: 
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Guitar not found, guitar lost into the void T-T"
        )

# PUT: ajouter mais sur l'existant

@app.put("/guitars/{guitarId}", tags=["Guitars"])
async def updateGuitar(guitarId: int, payload: Guitar, reposnse: Response):
        
    try: 
        cursor.execute('UPDATE guitar SET name=%s,brand=%s,type=%s,color=%s,price=%s,availability=%s  WHERE ID =%s;',(payload.guitarName, payload.guitarBrand, payload.guitarType, payload.guitarColor, payload.guitarPrice, payload.availability,guitarId))
        connexion.commit()
        return  {"message" : f"Guitar successfully refine, bring more light into {payload.guitarName} "}
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Guitar not found, guitar lost into the void T-T"
        )
