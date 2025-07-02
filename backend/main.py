from fastapi import FastAPI
from backend.routes import analyze

app = FastAPI(title="TradeGuard API")
app.include_router(analyze.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
