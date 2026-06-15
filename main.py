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

app.include_router(medipay.router)
app.include_router(wattwise.router)
app.include_router(insurecrop.router)

