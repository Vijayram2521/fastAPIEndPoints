import uvicorn
from fastapi import FastAPI
from .views import router

# sys.path.append(str(Path(__file__).resolve().parent))
app = FastAPI(title="AdviNow Interview Challenge", version="1.6")

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8013)