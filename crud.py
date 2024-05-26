from typing import Any
from aiohttp import web

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from errors import get_http_error
from models import MODEL, MODEL_TYPE, Session


async def select_one(query: Select[Any], session: AsyncSession) -> MODEL:
    item = (await session.execute(query)).first()
    if not item:
        return None
    return item[0]


async def get_item_by_id(model, item_id, session):
    item = await session.get(model, item_id)
    if item is None:
        raise get_http_error(web.HTTPNotFound, f"Data with id {item_id} is not found")
    return item


async def add_item(item: MODEL, session: AsyncSession) -> MODEL:
    try:
        session.add(item)
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, f"item with name {item.name} already exists")
    return item


async def create_item(model: MODEL_TYPE, payload: dict, session: Session) -> MODEL:
    item = model(**payload)
    item = await add_item(item, session)
    return item


async def update_item(item: MODEL, payload: dict, session: AsyncSession) -> MODEL:
    for field, value in payload.items():
        setattr(item, field, value)
    await add_item(item, session)
    return item


async def delete_item(item: MODEL, session: Session):
    await session.delete(item)
    await session.commit()