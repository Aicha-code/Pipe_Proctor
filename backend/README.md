# Pipe Proctor, An Intelligent Satellite-Based Threat Detection and Monitoring System for the Niger–Benin Oil Pipeline


This is a backend for the pipe proctor project. Backend use FastAPI framework and SuperBase online database.

### Frontend
The detailed frontend [documentation](/frontend/README.md) is in the frontend folder

## How to Run the APP
#### Clone the repository
```bash
git clone https://github.com/Aicha-code/Pipe_Proctor.git
cd Pipe_Proctor
code .
```
#### Run the Backend
> To be completed by @UWINTWALI
#### Backend Setup

Be aware that the backend is build using **FastAPI** framework(for building API using Python language)

#### 1. Navigate to the backend folder or directory

```bash
cd backend
```

#### 2. Create a virtual environment: 
`This contains the copy of Python interpreter and all dependences.`

```bash
python -m venv .venv
```

#### 3. Activate the virtual environment

**Windows / Git Bash:** better when you have Git Bash command-line

```bash
source .venv/Scripts/activate
```


#### 4. Install dependencies: 
*all required / used dependences are in requirements.txt file*

```bash
pip install -r requirements.txt
```

#### 5. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```
#### Then check the backend liveness at:
```text
http://127.0.0.1:8000/api/health
```
#### 6. Open the API documentation

FastAPI automatically provides interactive API documentation at the following localhost address on port 8000

```text
http://127.0.0.1:8000/docs
```




## References

### FastAPI

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)

### Supabase

- [Supabase Python Client Reference](https://supabase.com/docs/reference/python)
- [Supabase Documentation](https://supabase.com/docs)

### FastAPI + Supabase Integration

- [Building a Supabase and FastAPI Project: A Modern Backend Stack](https://medium.com/@abhik12295/building-a-supabase-and-fastapi-project-a-modern-backend-stack-52030ca54ddf)
- [How to Connect and Integrate Supabase with Python: FastAPI](https://hrekov.com/blog/supabase-with-fastapi)
- [Building a CRUD API with FastAPI and Supabase: A Step-by-Step Guide](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide)
- [FastAPI with Supabase: Production Integration Guide [2026]](https://markaicode.com/integrate/fastapi-with-supabase/)
- [Integrating FastAPI with Supabase Auth](https://dev.to/j0/integrating-fastapi-with-supabase-auth-780)
- [Building an API with FastAPI and Supabase](https://medium.com/@lior_amsalem/building-an-api-with-fastapi-and-supabase-c61a74d4e2f4)








