from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello everyone. This is Shashank! How are you doing? I'm good. Thank you for asking."
   ekajfnaskdjnf

@app.get("/health")
def health():
    return {"status": "ok"}
