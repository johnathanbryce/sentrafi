from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def init_app():
    print("Hello world.")
    return {"status": "ok", "service": "sentrafi-backend"}
