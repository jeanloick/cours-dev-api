
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto

router = APIRouter(
    prefix='/guitars',
    tags=['Guitars']
)

# Read
@router.get('')
async def get_Guitars(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_guitars = cursor.query(models_orm.Guitars).limit(limit).offset(offset).all() # Lancement de la requête
    guitars_count= cursor.query(func.count(models_orm.Guitars.id)).scalar()
    return {
        "guitars": all_guitars,
        "limit": limit,
        "total": guitars_count,
        "skip":offset
    }



# Read by id
@router.get('/{guitar_id}', response_model=schemas_dto.Guitar_GETID_Response)
async def get_guitar(guitar_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_guitar = cursor.query(models_orm.Guitars).filter(models_orm.Guitars.id == guitar_id).first()
    if(corresponding_guitar):  
        return corresponding_guitar
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guitar not found with id: {guitar_id}, an another guitar lost into the void..."
        )

# CREATE / POST 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_guitar(payload: schemas_dto.Guitar_POST_Body, cursor:Session= Depends(get_cursor)):
    new_guitar = models_orm.Guitars(name=payload.guitarName,brand=payload.guitarBrand,type=payload.guitarType,color=payload.guitarColor, price=payload.guitarPrice,availibility= payload.guitarAvaibility) # build the insert
    cursor.add(new_guitar) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_guitar)
    return {"message" : f"Guitar sucessfully added to the flow of metal and rock and roll, his name is : the {new_guitar.brand} {new_guitar.name} with the id : {new_guitar.id}, such a great choice ;)"} 

# DELETE ? 
@router.delete('/{guitar_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_guitar(guitar_id:int, cursor:Session=Depends(get_cursor)):
    # Recherche sur le produit existe ? 
    corresponding_guitar = cursor.query(models_orm.Guitars).filter(models_orm.Guitars.id == guitar_id)
    if(corresponding_guitar.first()):
        # Continue to delete
        corresponding_guitar.delete() # supprime
        cursor.commit() # commit the stated changes (changement latent)
        return 
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Guitar not found with id: {guitar_id}, an another guitar lost into the void...'
        )

# Update
@router.patch('/{guitar_id}')
async def update_guitar(guitar_id: int, payload:schemas_dto.Guitar_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # trouver le produit correspodant
    corresponding_guitar = cursor.query(models_orm.Guitars).filter(models_orm.Guitars.id == guitar_id)
    if(corresponding_guitar.first()):
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_guitar.update({'featured':payload.newFeatured})
        cursor.commit()
        return corresponding_guitar.first() 
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Guitar not found with id: {guitar_id}, an another guitar lost into the void...'
        )