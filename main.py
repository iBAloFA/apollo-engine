import uvicorn
import os
from routers import medipay, wattwise, insurecrop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="The Apollo Engine",
    description="A multi-module API for FinTech, HealthTech, and Climate Engineering",
    version="1.0.0"
)

# Enable CORS so the frontend can talk to the backend seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "modules": ["medipay", "wattwise", "insurecrop"],
        "docs_url": "/docs"
    }

app.include_router(medipay.router, prefix="/api/v1")
app.include_router(wattwise.router, prefix="/api/v1")
app.include_router(insurecrop.router, prefix="/api/v1")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)