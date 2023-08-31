from typing import List

from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Query

from config.database import collection_name
from models.sim_model import Sim, UpdateSim
from schemas.sim_schemas import sims_serializer, sim_serializer, update_to_dict

sim_api_router = APIRouter()

@sim_api_router.get("/dashboard")
async def get_sim():
    sims = sims_serializer(collection_name.find({"is_deleted": False}))
    return {"status":"Successfully", "data": sims}

@sim_api_router.get("/{id}")
async def get_sim(id: str):
    try:
        object_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sim with id {id} not found")
    sim = sims_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "Successfully", "data": sim}

@sim_api_router.post("/addproducts/")
async def create_sim(sim: Sim):
    _id = collection_name.insert_one(dict(sim))
    sim = sims_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "Successfully", "data": sim}

@sim_api_router.put("/updateproduct/{id}")
async def update_sim(id: str, update_sim: UpdateSim):
    try:
        sim_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sim with id {id} not found")

    update_sim.update_update_at()
    updated_values = update_sim.dict(exclude_unset=True)

    if not updated_values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    collection_name.find_one_and_update(
        {"_id": sim_id},
        {"$set": updated_values}
    )

    updated_sim = collection_name.find_one({"_id": sim_id})
    updated_sim_dict = update_to_dict(updated_sim)
    return {"status": "Successfully", "data": updated_sim_dict}

@sim_api_router.delete("/product/{id}")
async def delete_sim( id: str):
    try:
        object_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sim with id {id} not found")
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "Successfully"}

@sim_api_router.delete("/destroy/{id}")
async def destroy_sim(id: str):
    try:
        sim_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sim with id {id} not found")

    collection_name.find_one_and_update(
        {"_id": sim_id},
        {"$set": {"is_deleted": True}}
    )
    return {"status": "Successfully"}

@sim_api_router.put("/restore/{id}")
async def restore_sim(id: str):
    try:
        sim_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sim with id {id} not found")

    result = collection_name.find_one_and_update(
        {"_id": sim_id, "is_deleted": True},
        {"$set": {"is_deleted": False}},
        return_document=True
    )

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sim with id {id} not found or is not in trash")

    return {"status": "Successfully restored"}

@sim_api_router.get("/search/")
async def search_sim_by_prefix(prefix: str = Query(..., description="Phone number prefix")):
    query = {"phone_number": {"$regex": f"^{prefix}"},
             "is_deleted": False
             }
    result = collection_name.find(query)

    phone_numbers = [sim_serializer(sim) for sim in result]
    return {"matching_phone_numbers": phone_numbers}

@sim_api_router.get("/trashsim/")
async def get_trash_sims():
    sims = sims_serializer(collection_name.find({"is_deleted": True}))
    return {"status": "Successfully", "data": sims}
