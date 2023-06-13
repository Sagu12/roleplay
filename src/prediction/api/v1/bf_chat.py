from fastapi import  APIRouter
from src.prediction.services.v1.bf_chat import MissTm
from pydantic import BaseModel

class Model(BaseModel):
    txt: str
    user_id: str
Misstm= MissTm()
predict= APIRouter()

@predict.post('/bf_chat/v1')
async def api_predict(model: Model) -> None:
    res= await Misstm.draft_bf_message(model.txt, model.user_id)
    return res