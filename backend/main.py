from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diffusers import DiffusionPipeline
import torch
import io
import base64
from pathlib import Path

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
try:
    pipe = DiffusionPipeline.from_pretrained(
        "Tongyi-MAI/Z-Image-Turbo",
        trust_remote_code=True
    )
    if torch.cuda.is_available():
        pipe.to("cuda")
    else:
        pipe.to("cpu")
except Exception as e:
    print(f"Error loading model: {e}")
    # Fallback for testing without GPU or if model fails to load
    pipe = None

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_inference_steps: int = 4
    guidance_scale: float = 7.5

@app.post("/generate")
async def generate_image(request: GenerateRequest):
    if pipe is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        image = pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
        ).images[0]

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {"image": f"data:image/png;base64,{img_str}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
