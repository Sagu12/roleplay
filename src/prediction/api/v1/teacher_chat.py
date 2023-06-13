from fastapi import  APIRouter
from src.prediction.services.v1.teacher_chat import MissTm
from pydantic import BaseModel

class Model(BaseModel):
    txt: str
    user_id: str
Misstm= MissTm()
predict= APIRouter()

@predict.post('/teacher_chat/v1')
async def api_predict(model: Model) -> None:
    res= await Misstm.draft_teacher_message(model.txt, model.user_id)
    return res