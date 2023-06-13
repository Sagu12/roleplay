from transformers import CLIPProcessor, CLIPModel
import torch
import joblib
device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

joblib.dump(model, r'src/prediction/models/model.pk')
joblib.dump(processor, r'src/prediction/models/processor.pk')


