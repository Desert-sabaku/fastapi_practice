import redis
from fastapi import FastAPI, HTTPException

from app.models.grocery import ItemPayload

app = FastAPI()

redis_client = redis.StrictRedis(
    host="0.0.0.0", port=6379, db=0, decode_responses=True
)

@app.post("/items/{name}/{quantity}")
def add_item(name: str, quantity: int) -> dict[str, ItemPayload]:
    """Route to add an item to the inventory.

    Args:
        name (str): item name
        quantity (int): item quantity

    Raises:
        HTTPException: If quantity is less than or equal to 0

    Returns:
        dict[str, ItemPayload]: item payload
    """
    if quantity <= 0:
        raise HTTPException(
            status_code=400, detail="Quantity must be greater than 0.")

    # Check if item already exists
    item_id_str = redis_client.hget("item_name_to_id", name)

    if item_id_str is not None:
        id = int(item_id_str)
        redis_client.hincrby(f"item_id:{id}", "quantity", quantity)
    else:
        # Generate an ID for the item
        id = redis_client.incr("item_ids")
        redis_client.hset(
            f"item_id:{id}",
            mapping={
                "item_id": id,
                "item_name": name,
                "quantity": quantity,
            },
        )
        # Create a set so we can search by name too
        redis_client.hset("item_name_to_id", name, id)

    return {
        "item": ItemPayload(id=id, name=name, quantity=quantity)
    }


@app.get("/items/{id}")
def list_item(id: int) -> dict[str, dict[str, str]]:
    """Route to list a specific item by ID but using Redis.

    Args:
        id (int): item ID

    Raises:
        HTTPException: If item not found

    Returns:
        dict[str, dict[str, str]]: item payload
    """
    if not redis_client.hexists(f"item_id:{id}", "item_id"):
        raise HTTPException(status_code=404, detail="Item not found.")
    else:
        return {"item": redis_client.hgetall(f"item_id:{id}")}


@app.get("/items")
def list_items() -> dict[str, list[ItemPayload]]:
    items: list[ItemPayload] = []
    stored_items: dict[str, str] = redis_client.hgetall("item_name_to_id")

    for _, id_str in stored_items.items():
        id = int(id_str)

        name = redis_client.hget(f"item_id:{id}", "item_name")
        if name is not None:
            name = name
        else:
            continue  # skip this item if it has no name

        quantity = redis_client.hget(
            f"item_id:{id}", "quantity"
        )
        if quantity is not None:
            quantity = int(quantity)
        else:
            quantity = 0

        items.append(
            ItemPayload(id=id, name=name,
                        quantity=quantity)
        )

    return {"items": items}


@app.delete("/items/{id}")
def delete_item(id: int) -> dict[str, str]:
    """Route to delete a specific item by ID but using Redis.

    Args:
        id (int): item ID

    Raises:
        HTTPException: If item not found

    Returns:
        dict[str, str]: result message
    """
    if not redis_client.hexists(f"item_id:{id}", "item_id"):
        raise HTTPException(status_code=404, detail="Item not found.")
    else:
        name = redis_client.hget(
            f"item_id:{id}", "item_name")
        redis_client.hdel("item_name_to_id", f"{name}")
        redis_client.delete(f"item_id:{id}")
        return {"result": "Item deleted."}


@app.delete("/items/{id}/{quantity}")
def remove_quantity(id: int, quantity: int) -> dict[str, str]:
    """Route to remove some quantity of a specific item by ID but using Redis.

    Args:
        id (int): item ID
        quantity (int): quantity to remove

    Raises:
        HTTPException: If item not found

    Returns:
        dict[str, str]: result message
    """
    if not redis_client.hexists(f"item_id:{id}", "item_id"):
        raise HTTPException(status_code=404, detail="Item not found.")

    item_quantity = redis_client.hget(
        f"item_id:{id}", "quantity")

    # if quantity to be removed is higher or equal to item's quantity, delete the item
    if item_quantity is None:
        existing_quantity = 0
    else:
        existing_quantity = int(item_quantity)

    if existing_quantity <= quantity:
        name = redis_client.hget(
            f"item_id:{id}", "item_name")
        redis_client.hdel("item_name_to_id", f"{name}")
        redis_client.delete(f"item_id:{id}")
        return {"result": "Item deleted."}
    else:
        redis_client.hincrby(f"item_id:{id}", "quantity", -quantity)
        return {"result": f"{quantity} items removed."}
