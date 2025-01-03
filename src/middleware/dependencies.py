from fastapi import Request, HTTPException

async def get_active_project_id(request: Request):
    if not hasattr(request.state, "active_project") or not request.state.active_project:
        raise HTTPException(status_code=400, detail="No active project set")
    return request.state.active_project