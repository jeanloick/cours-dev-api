from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel


app = FastAPI() #variable names for the server

#Data models / Schema / DTO
class Guitar (BaseModel):
    guitarBrand: str
    guitarType:str
    guitarName: str
    guitarColor: str
    guitarPrice: float
    #availability: bool = True #default / optionnel
    #rating: Optional[int] # completement optionnel


@app.get("/message")
async def root():
    return {"message":"with great power comes great responsibility"}

guitarList = [{"guitarBrand":"Gibson", "guitarType":"electric", "guitarName": "flying V 1966", "guitarPrice":1350, "guitarColor": "black"},
              {"guitarBrand":"Gibson","guitarType":"electric", "guitarName": "SG signature Angus YOUNG 1988", "guitarPrice":2988, "guitarColor": "red"}]

@app.get("/guitars")
async def getGuitars():
    return { "Guitars": guitarList,
              "limits": 10,
              "total": 2,
              "skip": 0
        }
@app.post("/guitars")
async def create_post(payload: Guitar, response: Response):
    print(payload.guitarName)
    guitarList.append(payload.dict())

    response.status_code = status.HTTP_201_CREATED
    return {"message": f"guitar sucessfully added to the flow of metal and rock and roll, his name is : {payload.guitarBrand +' '+ payload.guitarName}, such a great choice ;)"}

@app.get("/guitars/{guitarId}")
async def getGutar(guitarId: int, response: Response ):
    try: 
        correspondingGuitar = guitarList[guitarId -1]# pck ID begin to 1 and index to 0 
        return correspondingGuitar 
    
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Guitar lost in the void T-T"
        )
  