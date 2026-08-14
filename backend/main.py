from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth_router, detection_router

## start the fastapi app
app = FastAPI(
     title="Pipe Proctor API",
     description="Backend API for satellite anomaly detection and dashboard operations",
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
app.include_router(detection_router)

## check the liveness of the backend
@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status":"healthy",
        "service":"pipe-proctor-api",
        "message":"Server is running properly"
    }
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
       "main:app",
       host="0.0.0.0",
       port=8000,
       reload=True
    )
    
