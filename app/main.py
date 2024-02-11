from fastapi import FastAPI
import uvicorn
from routers import posts,users,votes

app = FastAPI()

app.include_router(router=posts.posts_router)
app.include_router(router=users.users_router)
app.include_router(router=votes.votes_router)
#start main app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True,log_level="info")
