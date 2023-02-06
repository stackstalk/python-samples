from fastapi import FastAPI, Request
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

import uvicorn
import os

description = """
Sample app to demonstrate file upload with FastAPI
"""
app = FastAPI(title="FileUploadApp",
              description=description,
              version="0.1")


@app.get("/download")
async def download(name: str):
    file_path = "/app/filecache/" + name + ".zip"
    if os.path.exists(file_path):
       return FileResponse(path=file_path, filename=file_path, media_type='application/zip')
    
    return {"message": "File not found"}
      

@app.post("/upload")
async def upload(name: str, file: UploadFile = File(...)):
    try:
        filename = "/app/filecache/" + name + ".zip" 
        with open(filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        print(e)
        return {"message": "Error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

if __name__ == '__main__':
    uvicorn.run('app:app',
                host='0.0.0.0',
                port=8091,
                reload=True)
