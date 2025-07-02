from fastapi import APIRouter, UploadFile, File
from backend.services.analyzer import analyze_trades
import tempfile

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        result = analyze_trades(tmp.name)
    return result
