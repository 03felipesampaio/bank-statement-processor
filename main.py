from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def get_main_page() -> str:
    return "Hello World!"