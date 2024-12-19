import datetime
from uuid import UUID

from fastapi import APIRouter, Query
from injection import inject

from src.di import UsersDAO

router = APIRouter(prefix="")


@router.get("/offset-example")
@inject
async def offset_endpoint(
        users_dao: UsersDAO,
        offset: int = Query(0),
        page_size: int = Query(5)
):
    items = users_dao.get_offset_items(
        offset=offset,
        page_size=page_size,
    )

    return {
        "items_count": len(items),
        "page_size": page_size,
        "offset": offset,
        "items": items
    }


@router.get("/keyset-example")
@inject
async def keyset_endpoint(
        users_dao: UsersDAO,
        page_size: int = Query(5),
        # last_item_id: UUID = Query(None),
        last_item_sorting_value: datetime.datetime = Query(None),
):
    items = users_dao.get_keyset_items(
        page_size=page_size,
        last_item_sorting_value=last_item_sorting_value,
    )
    return {"items": items}
