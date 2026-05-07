from fastapi import FastAPI

app = FastAPI(
    title="Whisk Render Service",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Whisk Render Service"
    }

@app.get("/health")
def health_check():
    return {
        "healthy": True
    }