# Pipe Proctor, An Intelligent Satellite-Based Threat Detection and Monitoring System for the Niger–Benin Oil Pipeline


## Project Structure


### Data cleaning pipeline

### Backend

### Frontend
The detailed frontend [documentation](/frontend/README.md) is in the frontend folder




## How to Run the APP
#### Clone the repository
```bash
git clone https://github.com/Aicha-code/Pipe_Proctor.git
cd https://github.com/Aicha-code/Pipe_Proctor.git
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

#### Run the Frontend
```bash
# All command that can be copy-pasted
cd frontend
npm install
npm run dev
```

## Work plan

| Milestone | Responsible (and Reviegit pull origin feat/frontendwer) | Timeline |
|-----------|-------------|----------|
| Frontend | Buhendwa Ange Asifiwe, Uwintwali Jean de Dieu | Aug 10 - Aug 14 |
| Backend | Uwintwali Jean de Dieu, Buhendwa Ange Asifiwe | Aug 11 - Aug 13 |
| Data curation and model design | Baraka Jonathan Kashabira, Abari Ilior Aichetou | Aug 8 - Aug 10 |
| Model Training and Evaluation | Baraka Jonathan Kashabira, Abari Ilior Aichetou | Aug 11 - Aug 13 |
| Project integration (Model + interface) | Umwintwali Jean de Dieu, Buhendwa Ange, Baraka Jonathan K., Abari Ilioe Aichetou | Aug 14 |



