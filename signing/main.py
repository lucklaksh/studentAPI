from fastapi import FastAPI
from .database import engine
from .models import  Base
from .routers import students,authentication





app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(students.router)




