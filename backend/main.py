from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth_router

## start the fastapi app
app = FastAPI(
     title="user Authentication API",
     description="Pipe proctor's user Registration and Login Screens",
     version="1.0.0"
 )
 
 ## Enable CORS to allow frontend make a request to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production we need to specify specific domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## add the authentication routes
app.include_router(auth_router, prefix="/api/v1")

## check the liveness of the backend
@app.get("/")
@app.get("/health")

## create a function to test backed and make sure it is up and running.

def health_check():
    return {
        "status":"healthy",
        "service":"auth-api",
        "message":"Server is running properly"
        
    }
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
       "app.main:app",
       host="0.0.0.0",
       port=8000,
       reload=True
    )
    
