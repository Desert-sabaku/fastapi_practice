from fastapi import FastAPI, HTTPException

from app.model.grocery import ItemPayload

app = FastAPI()

grocery_list: dict[int, ItemPayload] = {}


@app.post("/items/{item_name}/{quantity}")
def add_item(name: str, quantity: int) -> dict[str, ItemPayload]:
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    items_ids = {
        item.name: item.id if item.id is not None else 0 for item in grocery_list.values()
    }

    if name in items_ids.keys():
        item_id = items_ids[name]
        grocery_list[item_id] = ItemPayload(
            id=item_id,
            name=name,
            quantity=quantity
        )
    else:
        item_id = max(grocery_list.keys()) + 1 if grocery_list else 1
        grocery_list[item_id] = ItemPayload(
            id=item_id,
            name=name,
            quantity=quantity
        )

    return {"item": grocery_list[item_id]}
