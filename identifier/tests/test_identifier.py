from django.test import TestCase, tag

from ..checkdigit_mixins import LuhnMixin, LuhnOrdMixin
from ..exceptions import IdentifierError
from ..identifier import Identifier
from ..models import IdentifierModel


class WorkResidentPermitIdentifier(Identifier):
    
    
    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'work_resident_permit'  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = 'WR'


class TestIdentifier(TestCase):

    @tag('1')
    def test_valid_checkdigit(self):
        mixin = LuhnMixin()
        checkdigit = mixin.calculate_checkdigit('98765')
        self.assertEqual(checkdigit, '1')
        checkdigit = mixin.calculate_checkdigit('98766')
        self.assertEqual(checkdigit, '9')
        checkdigit = mixin.calculate_checkdigit('98767')
        self.assertEqual(checkdigit, '7')

    def test_luhn_ord_mixin(self):
        mixin = LuhnOrdMixin()
        self.assertEqual('4', mixin.calculate_checkdigit('ABCDE'))
        self.assertEqual('8', mixin.calculate_checkdigit('ABCDEF'))
        self.assertEqual('0', mixin.calculate_checkdigit('ABCDEFG'))

    def test_identifier(self):
        instance = WorkResidentPermitIdentifier(
             address_code='821', dob='07071989', label='wr_permit')
        self.assertEqual('WR8210707198900001-1', instance.identifier)

        instance = WorkResidentPermitIdentifier(
             address_code='821', dob='07071989', label='wr_permit')
        self.assertEqual('WR8210707198900002-9', instance.identifier)

    def test_increments(self):
        """Asserts identifier sequence increments correctly.
        """
        opts = dict(address_code='821', dob='07071989',
                    label='wr_permit')
        for i in range(1, 10):
            identifier = WorkResidentPermitIdentifier(**opts)
            self.assertEqual(
                identifier.identifier[13:18], '0000' + str(i))

    def test_create_missing_args(self):
        """Asserts raises exception for missing identifier_type.
        """
        self.assertRaises(
            IdentifierError,
            Identifier,
            address_code='821',
            dob='07071989',
            label='wr_permit',)

    def test_updates_identifier_model(self):
        """Asserts updates Identifier model with all attributes.
        """
        for _ in range(0, 5):
            WorkResidentPermitIdentifier(
                address_code='821', dob='07071989',
                label='wr_permit', identifier_type='WR')
        self.assertEqual(IdentifierModel.objects.all().count(), 5)
