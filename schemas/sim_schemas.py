def sim_serializer(sim) -> dict:
    return {
        "id": str(sim["_id"]),
        "network": sim["network"],
        "phone_number": sim["phone_number"],
        "price": sim["price"],
        "category": sim["category"],
        "detail": sim["detail"],
        "created_at": sim["created_at"],
        "updated_at": sim["updated_at"],
        "is_deleted": sim["is_deleted"]
    }

def sims_serializer(sims) -> list:
    return [sim_serializer(sim) for sim in sims]


def update_to_dict(update) -> dict:

    update_dict = {
        "id": str(update["_id"]),
        "network": update["network"],
        "phone_number": update["phone_number"],
        "price": update["price"],
        "category": update["category"],
        "detail": update["detail"],
        "updated_at": update["updated_at"]
    }

    if "created_at" in update:
        update_dict["created_at"] = update["created_at"]

    return update_dict