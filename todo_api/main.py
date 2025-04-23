from fastapi import FastAPI, HTTPException
from bson import ObjectId
from db import task_collection
from models import Task

app = FastAPI()

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description", ""),
        "completed": task["completed"]
    }

@app.post("/tasks")
def create_task(task: Task):
    result = task_collection.insert_one(task.dict())
    return {"id": str(result.inserted_id)}

@app.get("/tasks")
def get_tasks():
    return [task_helper(task) for task in task_collection.find()]

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = task_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_helper(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: str, updated: Task):
    result = task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": updated.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"msg": "Updated successfully"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    result = task_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"msg": "Deleted successfully"}