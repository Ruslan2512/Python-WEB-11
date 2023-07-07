import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.chemas import ContactModel
from src.repository.contacts import get_contacts, get_contact_by_fullname, get_contact_by_lastname, create, update, remove


class TestContactsRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.contact = Contact(fullname='test_name', lastname='test_lastname', email='test@test.com', phone_number='+01234567', birthday='01.01.1970')

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).limit().offset().all().return_value = contacts
        result = await get_contacts(10, 0, self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(
            fullname='test_name',
            lastname='test_lastname',
            email='test@test.com',
            phone_number='+01234567',
            birthday='01.01.1970'
        )
        result = await create(body, self.session)
        self.assertEqual(result.fullname, body.fullname)
