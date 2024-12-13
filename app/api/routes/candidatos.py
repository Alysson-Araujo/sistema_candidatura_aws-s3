from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from pydantic import EmailStr
import json
from io import BytesIO
from app.services.s3_service import S3Service
from app.services.candidato_service import create_candidato, candidato_exists_by_email
from app.models.candidato_model import Candidato
from fastapi.encoders import jsonable_encoder
import uuid

router = APIRouter()
s3_service = S3Service()

@router.post("/save_candidato")
async def save_candidato(
    nome: str = Form(...),
    email: EmailStr = Form(...),
    telefone: str = Form(None),
    cidade: str = Form(None),
    estado: str = Form(None),
    pais: str = Form("Brasil"),
    linkedin: str = Form(None),
    portifolio: str = Form(None),
    pretensao_salarial: str = Form(None),
    area_interesse: str = Form(None),
    curriculo: UploadFile = File(...),
    ):
    unique_id = uuid.uuid4().hex

    try:
        if curriculo.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
        candidate_exists = await candidato_exists_by_email(email)
        
        if candidate_exists:
            raise HTTPException(status_code=400, detail="Candidate already registered.")
        
        curriculo.filename = f"{unique_id}_{replace_spaces(curriculo.filename)}"
        
        candidato_data = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cidade": cidade,
            "estado": estado,
            "pais": pais,
            "linkedin": linkedin,
            "portifolio": portifolio,
            "pretensao_salarial": pretensao_salarial,
            "area_interesse": area_interesse,
            "curriculo_url": "",
        }
        
        file_data = await curriculo.read()
        file_stream = BytesIO(file_data)
        
        file_url = s3_service.upload_file(
            file=file_stream,
            object=curriculo.filename,
        )
        
        if not file_url:
            raise HTTPException(status_code=500, detail="Failed to save file in S3.")
        
        candidato_data["curriculo_url"] = file_url

        candidad_obj = Candidato(**candidato_data)
        candidato_created = await create_candidato(candidad_obj)
        
        if not candidato_created:
            raise HTTPException(status_code=500, detail="Failed to save candidate in database.")
        
        candidato_created = jsonable_encoder(candidato_created)
        
        return Response(status_code=201, content=json.dumps(candidato_created))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error on upload: {e}")

def replace_spaces(string):
    return string.replace(" ", "_")