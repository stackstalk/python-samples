from fastapi import FastAPI 

import uvicorn

app = FastAPI() 

@app.get("/hello") 
async def root(): 
     return {"message": "Hello, World!"} 

@app.get("/health") 
async def root(): 
     return "ok" 

if __name__ == '__main__':
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=9089,
                reload=True)
