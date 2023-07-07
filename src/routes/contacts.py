from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.chemas import ContactResponse, ContactModel
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.conf import messages

router = APIRouter(prefix="/contacts", tags=['contacts'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get),
                                                                     Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)): # Перевірка на токен, потребує авторизації
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_get)])
async def get_contacts(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_fullname(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_create)])
async def create_contacts(body: ContactModel, db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_lastname(body.contact_id, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.EMAIL_IS_EXIST)

    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_update)])
async def update_contacts(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)

    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_remove)])
async def remove_contacts(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact
