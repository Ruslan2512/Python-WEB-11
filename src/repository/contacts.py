from sqlalchemy.orm import Session

from src.database.models import Contact
from src.chemas import ContactModel
from src.services.auth import auth_service


async def get_contacts(limit: int, offset: int, db: Session):
    """
    The get_contacts function returns a list of contacts from the database.

    :param limit: int: Limit the number of results returned
    :param offset: int: Specify the number of items to skip before returning results
    :param db: Session: Pass the database session to the function
    :return: Alist of cat objects
    """
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_fullname(contact_id, db: Session):
    contact = db.query(Contact).filter_by(fullname=contact_id).first()
    return contact


async def get_contact_by_lastname(lastname: str, db: Session):
    contact = db.query(Contact).filter_by(lastname=lastname).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_fullname(contact_id, db)
    if contact:
        contact.email = body.email
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_fullname(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
