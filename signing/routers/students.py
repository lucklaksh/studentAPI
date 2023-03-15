from fastapi import FastAPI, Depends , status, HTTPException,APIRouter, Response
from .. import schemas,models,database
from sqlalchemy.orm import Session
from ..hashing import Hash

router =APIRouter(
    prefix="/students",
    tags=["Students"]
)




@router.post("/signup",status_code=201,response_model= schemas.show_data)
def signup(request : schemas.structure, db :  Session = Depends(database.db_get)):
    try:
        user = models.User(user_name=request.user_name, email=request.email , password = Hash.bcrypt(request.password) ,contact= request.contact, address = request.address)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        return e


@router.get("/{contact}", status_code=201, response_model=schemas.show_data)
def get_student( contact : str, db: Session= Depends(database.db_get)):
    try:
        user = db.query(models.User).filter(models.User.contact == contact).first()
        return (user)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with contact {contact} not available')
        return user
    except Exception as e:
        return e