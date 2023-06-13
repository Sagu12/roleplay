from fastapi import  APIRouter
from src.prediction.services.v1.doctor_chat import MissTm
from pydantic import BaseModel

class Model(BaseModel):
    txt: str
    user_id: str
Misstm= MissTm()
predict= APIRouter()

@predict.post('/doctor_chat/v1')
async def api_predict(model: Model) -> None:
    res= await Misstm.draft_doctor_message(model.txt,model.user_id)
    return res