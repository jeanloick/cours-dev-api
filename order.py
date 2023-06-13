from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI() #variable names for the server

#Data models / Schema / DTO
class Order (BaseModel):
    orderCode: str
    client :
        lastName:str
        adress: str
        email : str
        postalCode: int
        memberCode: float
    
  


OrderList = [{"firstName":"Jerry", "lastName":"Tyler", "adress": "1 rue du pont", "email": "jerry@gmail.com" , "postalCode": 85521, "memberCode": "855989EDF"},
              {"firstName":"Rick", "lastName":"Grames", "adress": "the commonwelth, sector 2", "email": "rick@gmail.com" , "postalCode": 45632, "memberCode": "7844999PKFZ5"}]
