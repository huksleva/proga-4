from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def main_page():
    return FileResponse("templates/index.html")


@app.get("/")




@app.post("/a")
def request():

    return {"123": 123}







if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5001, reload=True)