from fastapi import  APIRouter
from src.prediction.services.v1.fitnesscoach_chat import MissTm
from pydantic import BaseModel

class Model(BaseModel):
    txt: str
    user_id: str
Misstm= MissTm()
predict= APIRouter()

@predict.post('/fitness_coach_chat/v1')
async def api_predict(model: Model) -> None:
    res= await Misstm.draft_fitnesscoach_message(model.txt, model.user_id)
    return res