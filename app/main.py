from fastapi import FastAPI
import uvicorn
from routers import posts,users,votes

app = FastAPI()

@app.get("/",status_code=200)
def hello():
    return {
        "msg": "Hello World"
    }

app.include_router(router=posts.posts_router)
app.include_router(router=users.users_router)
app.include_router(router=votes.votes_router)
#start main app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True,log_level="trace")
