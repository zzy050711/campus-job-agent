from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "欢迎来到 Campus Job Agent！"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }