from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def main_page():
    return FileResponse("templates/index.html")


@app.post("/createObject")
def create_object():
    pass



@app.delete("/deleteObject")
def delete_object():
    pass

@app.delete("/deleteAllObject")
def delete_all_object():
    pass







if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5001, reload=True)