from fastapi import FastAPI
from routes import user_routes, course_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(course_routes)
@app.get("/")
def home():
    return {"message": "API rodando"}
