from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timezone

class Candidato(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    pais: str = "Brasil"
    linkedin: Optional[str]
    portifolio: Optional[str]
    pretensao_salarial: Optional[float]
    area_interesse: Optional[str]
    curriculo_url: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))