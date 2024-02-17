from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import get_db, News, Base, engine

import users

app = FastAPI(
    title='News API',
    docs_url='/',
    version='1.0'
)

app.include_router(users.router)

Base.metadata.create_all(engine)


class CreateNewSchema(BaseModel):
    title: str
    content: str


class ResponseNewsSchema(BaseModel):
    title: str
    content: str


@app.post('/new/', response_model=ResponseNewsSchema, tags=['News'])
async def add_new(news: CreateNewSchema, db: Session = Depends(get_db)):
    new = News(title=news.title, content=news.content)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get('/new/', tags=['News'])
async def list_news(db: Session = Depends(get_db)):
    news = db.query(News).all()
    return {'news': news}


@app.get('/new/{new_id}', tags=['News'])
async def detail_new(new_id: int, db: Session = Depends(get_db)):
    new = db.query(News).get(new_id)
    return new


@app.patch('/new/{new_id}', tags=['News'])
async def detail_new(new_id: int, data_new: CreateNewSchema, db: Session = Depends(get_db)):
    new = db.query(News).get(new_id)
    if new:
        new.title = data_new.title
        new.content = data_new.content
        db.commit()
        db.refresh(new)
        return new
    raise HTTPException(status_code=404, detail='News not found')


@app.delete('/new/{new_id}', tags=['News'])
async def delete_new(new_id: int, db: Session = Depends(get_db)):
    new = db.query(News).get(new_id)
    if new:
        db.delete(new)
        db.commit()
        return {"message": "News deleted successfully"}
    raise HTTPException(status_code=404, detail='News not found')
