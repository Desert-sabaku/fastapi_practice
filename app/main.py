from fastapi import FastAPI, HTTPException

from app.model.grocery import ItemPayload

app = FastAPI()

grocery_list: dict[int, ItemPayload] = {}


@app.post("/items/{name}/{quantity}")
def add_item(name: str, quantity: int) -> dict[str, ItemPayload]:
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # if item already exists, we'll just add the quantity.
    # get all item names
    items_ids = {
        item.name: item.id if item.id is not None else 0
        for item in grocery_list.values()
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


@app.get("/items")
def list_items(id: int) -> dict[str, ItemPayload]:
    return {"items": grocery_list[id]}


@app.delete("/items/{id}")
def delete_item(id: int):
    if id not in grocery_list:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    del grocery_list[id]
    return {"message": "Item deleted successfully"}


@app.delete("/items/{id}/{quantity}")
def remove_quantity(id: int, quantity: int):
    if id not in grocery_list:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    if grocery_list[id].quantity <= quantity:
        raise HTTPException(
            status_code=400,
            detail="Quantity to remove is greater than the available quantity"
        )
    else:
        grocery_list[id].quantity -= quantity

    return {"message": "Quantity removed successfully"}
