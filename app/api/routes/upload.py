from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.s3_service import S3Service
from io import BytesIO
import uuid

router = APIRouter()

s3_service = S3Service()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    unique_id = uuid.uuid4().hex
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")
        
        file.filename = f"{unique_id}_{replace_spaces(file.filename)}"
        
        file_data = await file.read()
        file_stream = BytesIO(file_data)
        file_url = s3_service.upload_file(
            file=file_stream,
            object=file.filename
        )
        if not file_url:
            raise HTTPException(status_code=500, detail="Falha ao salvar o arquivo no S3.")
        return {"file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {e}")

def replace_spaces(string):
    return string.replace(" ", "_")