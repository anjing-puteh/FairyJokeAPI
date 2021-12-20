from datetime import date
from typing import List
from fastapi.responses import FileResponse, RedirectResponse

from app import db, Schema
from . import router, DATA_PATH
from .models import Apeca, Difficulties, Music, Genres


class DifficultySchema(Schema):
    diff: Difficulties
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
    # genres: List[Genres]
    difficulties: List[DifficultySchema]

    class Config:
        orm_mode = True


@router.get('/musics')
async def sdvx_get_musics():
    return {
        x.id: MusicSchema.from_orm(x)
        for x in db.session.query(Music)
    }


@router.get('/musics/{music_id}')
async def sdvx_get_music(music_id: int):
    music = db.session.get(Music, music_id)
    return MusicSchema.from_orm(music)


@router.get('/musics/{music_id}/{difficulty}.png')
async def sdvx_get_jacket(music_id: int, difficulty: Difficulties):
    music = await sdvx_get_music(music_id)
    diff = next(filter(lambda x: x.diff == difficulty, music.difficulties))
    if diff.external_jacket:
        return RedirectResponse(diff.external_jacket)
    path = DATA_PATH / 'music' / diff.music.folder / diff.filename
    return FileResponse(path)


@router.get('/apecas/{apeca_id}.png')
async def sdvx_get_apeca(apeca_id: int):
    apeca = db.session.get(Apeca, apeca_id)
    path = DATA_PATH / 'graphics' / 'ap_card' / f'{apeca.texture}.png'
    return FileResponse(path)
