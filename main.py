from typing import Optional
from fastapi import FastAPI, Body
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