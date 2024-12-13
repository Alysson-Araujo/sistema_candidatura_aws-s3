from app.core.database import MongoDBService
from app.models.candidato_model import Candidato
from pydantic import EmailStr


def serialize_candidato(candidato) -> dict:
    candidato["_id"] = str(candidato["_id"])
    return candidato

async def create_candidato(candidato: Candidato):
    db_service = MongoDBService() 
    candidato_dict = candidato.model_dump(by_alias=True)
    resultado = db_service.db["candidatos"].insert_one(candidato_dict)
    candidato_dict["_id"] = str(resultado.inserted_id)
    return candidato_dict

async def candidato_exists_by_email(email: EmailStr):
    db_service = MongoDBService() 
    candidato = db_service.db["candidatos"].find_one({"email": email})
    if candidato:
        return True
    return False
    