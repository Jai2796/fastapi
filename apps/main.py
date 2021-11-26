from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# from .schemas import Poster

# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='bala1234', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('Database connnection failed')
#         print('Error : ', error)
#         time.sleep(3)

# my_posts = [{"title": "title of post 1", "content":"content of post 1", "id":1}, {"title":"Favorite foods", "content":"its an awesome food", "id":2},]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World !!!"}

# @app.get("/sqlalchemy")
# def test_posts(db : Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return {'status': post}







