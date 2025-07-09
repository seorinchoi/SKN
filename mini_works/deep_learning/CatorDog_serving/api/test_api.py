from fastapi import FastAPI
from pydantic import BaseModel
import base64
import io
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms

# ✅ 클래스 라벨
class_names = ["고양이", "강아지"]

# ✅ FastAPI 앱
app = FastAPI()

# ✅ 모델 로드
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("/home/seorin0224/workspace/api/model/model_epoch_2.pth", map_location=torch.device("cpu")))
model.eval()

# ✅ 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ✅ 요청 데이터 모델
class ImageItem(BaseModel):
    image_data: str

# ✅ 예측 엔드포인트
@app.post("/predict/")
async def inference(item: ImageItem):
    try:
        # base64 디코딩
        img_bytes = base64.b64decode(item.image_data)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # 전처리
        input_tensor = transform(image).unsqueeze(0)  # [1, 3, 224, 224]

        # 예측
        with torch.no_grad():
            outputs = model(input_tensor)
            _, pred = torch.max(outputs, 1)
            label = class_names[pred.item()]

        return {"message": f"이 이미지는 {label}입니다!"}

    except Exception as e:
        return {"error": str(e)}

# ✅ 테스트용 엔드포인트
@app.get("/")
async def root():
    return {"message": "서버가 잘 작동 중입니다!"}
