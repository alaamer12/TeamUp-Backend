from typing import List

from beanie.odm.enums import SortDirection
from fastapi import APIRouter, HTTPException, Body, status

from app.models.team_request import TeamRequest

router = APIRouter()


@router.get("/", response_model=List[TeamRequest])
async def get_requests() -> List[TeamRequest]:
    """
    Retrieve all team requests sorted by creation date (newest first).
    
    Returns:
        List[TeamRequest]: A list of team request documents
    """
    requests = await TeamRequest.find_all().sort([("created_at", SortDirection.ASCENDING)]).to_list()
    return requests


@router.post("/", response_model=TeamRequest, status_code=status.HTTP_201_CREATED)
async def create_request(request: TeamRequest) -> TeamRequest:
    """
    Create a new team request.
    
    Args:
        request: The team request data
    
    Returns:
        TeamRequest: The created team request
    """
    await request.save()
    return request


@router.delete("/{request_id}")
async def delete_request(
        request_id: str,
        owner_fingerprint: str = Body(..., embed=True)
) -> dict:
    """
    Delete a team request.
    
    Args:
        request_id: The ID of the request to delete
        owner_fingerprint: The fingerprint of the request owner for verification
    
    Returns:
        dict: A message confirming the deletion
    
    Raises:
        HTTPException: If the request is not found or user is not authorized
    """
    # Find the request
    request = await TeamRequest.get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Check ownership
    if request.owner_fingerprint != owner_fingerprint:
        raise HTTPException(status_code=403, detail="Not authorized to delete this request")

    # Delete the request
    await request.delete()

    return {"message": "Request deleted successfully"}


@router.put("/{request_id}", response_model=TeamRequest)
async def update_request(
        request_id: str,
        request_data: TeamRequest
) -> TeamRequest:
    """
    Update a team request.
    
    Args:
        request_id: The ID of the request to update
        request_data: The updated team request data
    
    Returns:
        TeamRequest: The updated team request
    
    Raises:
        HTTPException: If the request is not found or user is not authorized
    """
    # Find the request
    request = await TeamRequest.get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Check ownership
    if request.owner_fingerprint != request_data.owner_fingerprint:
        raise HTTPException(status_code=403, detail="Not authorized to update this request")

    # Update the request (excluding id field)
    for field, value in request_data.model_dump(exclude={"id"}).items():
        setattr(request, field, value)

    await request.save()
    return request
