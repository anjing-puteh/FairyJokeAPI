from datetime import date
from typing import List
from fastapi.responses import FileResponse

from app import db, Schema
from . import router, DATA_PATH
from .models import Difficulties, Difficulty, Music


class DifficultySchema(Schema):
    name: Difficulties
    level: int
    illustrator: str
    effector: str

    class Config:
        orm_mode = True


class MusicSchema(Schema):
    title: str
    artist: str
    ascii: str
    bpm: str
    release_date: date
    genres: List[str]
    difficulties: List[DifficultySchema]

    class Config:
        orm_mode = True


@router.get('/musics')
async def get_musics():
    return {
        x.id: MusicSchema.from_orm(x)
        for x in db.session.query(Music)
    }


@router.get('/musics/{music_id}')
async def get_music(music_id: int):
    music = db.session.get(Music, music_id)
    return music


@router.get('/musics/{music_id}/{difficulty}.png')
async def get_jacket(music_id: int, difficulty: Difficulties):
    diff = db.session.get(Difficulty, (music_id, difficulty))
    path = DATA_PATH / 'music' / diff.music.folder / diff.filename
    return FileResponse(path)
