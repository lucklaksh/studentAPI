from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,database,models, token
from sqlalchemy.orm import Session
from ..hashing import Hash
from datetime import datetime
import random

router =APIRouter(
    tags=['Authentication']
)


# ,response_model=schemas.show_secret_data

@router.post("/login", status_code=201)
def login( request: schemas.login_details, db: Session= Depends(database.db_get)):
    # try:
    user = db.query(models.User).filter(models.User.email== request.email ).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with email {request.email} not found")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="incorrect password")
    print(f"user is working {str(user)}")


    access_token = token.create_access_token(data={"sub": user.email})
    # return {"access_token": access_token, "token_type": "bearer"}

    auth_key = db.query(models.DataSecret).filter(models.DataSecret.studentID == user.id).first()
    if not auth_key:
        rand = random.randint(10000,99999)
        new_secret_data = models.DataSecret(jwt= access_token, created_date = datetime.utcnow(),last_updated= datetime.utcnow(),otp=rand,studentID= user.id)
        db.add(new_secret_data)
        db.commit()
        db.refresh(new_secret_data)
        return (rand , new_secret_data)

    if auth_key.otp != request.otp :
        return (f"entered otp : {request.otp} is incorrect ")
    return ("sucessfully logged in....")
    # except Exception as e:
    #     return e


@router.post("/{contact}/generate_otp", status_code=201)
def generate_otp( contact : str, db: Session = Depends(database.db_get)):
    # try:
    user = db.query(models.User).filter(models.User.contact == contact).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with contact: {contact} not found")

    auth_key = db.query(models.DataSecret).filter(models.DataSecret.studentID == user.id).first()
    if not auth_key:
        return (" you have not logged in pls login...")

    rand = random.randint(10000, 99999)
    auth_key.otp = rand
    auth_key.last_updated = auth_key.created_date
    auth_key.created_date = datetime.utcnow()
    db.add(auth_key)
    db.commit()
    db.refresh(auth_key)
    return (rand, auth_key)




