from fastapi import FastAPI
app = FastAPI() #variable names for the server

@app.get("/")
async def root():
    return {"message":"with great power comes great responsibility"}