from string import Formatter

from .checkdigit_mixins import LuhnOrdMixin
from .models import IdentifierModel
from .exceptions import IdentifierError


class IdentifierMissingTemplateValue(Exception):
    pass


class Identifier:
    
    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = None  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = None  # e.g. 'work_permit', 'visa', 'citizenship', a.k.a identity_type
    padding = 5
    checkdigit = LuhnOrdMixin()
    identifier_model_cls = IdentifierModel
    
    def __init__(self, identifier_type=None, template=None, label=None,
                 address_code=None, dob=None, identifier=None):
        
        self.address_code = address_code
        self.dob = dob
        self.label = label or self.label
        self._identifier = None
        self.identifier_type = identifier_type or self.identifier_type
        if not self.identifier_type:
            raise IdentifierError('Invalid identifier_type. Got None')
        self.template = template or self.template
        if identifier:
            # load an existing identifier
            self.identifier_model = self.identifier_model_cls.objects.get(
                identifier=identifier)
            self._identifier = self.identifier_model.identifier
            self.identifier_type = self.identifier_model.identifier_type
            self.address_code = self.identifier_model.address_code
            self.dob = self.identifier_model.dob
        self.identifier
        


    @property
    def identifier(self):
        """Returns a new and unique identifier and updates
        the IdentifierModel.
        """
        if not self._identifier:
            self.pre_identifier()
            self._identifier = self.template.format(**self.template_opts)
            check_digit = self.checkdigit.calculate_checkdigit(
                ''.join(self._identifier.split('-')))
            self._identifier = f'{self._identifier}-{check_digit}'
            self.identifier_model = self.identifier_model_cls.objects.create(
                name=self.label,
                sequence_number=self.sequence_number,
                identifier=self._identifier,
                dob=self.dob,
                address_code=self.address_code,
                identifier_type=self.identifier_type)
            self.post_identifier()
        return self._identifier

    def pre_identifier(self):
        pass


    def post_identifier(self):
        pass


    @property
    def template_opts(self):
        """Returns the template key/values, if a key from the template
        does not exist raises an exception.
        """
        template_opts = {}
        formatter = Formatter()
        keys = [opt[1] for opt in formatter.parse(
            self.template) if opt[1] not in ['sequence']]
        template_opts.update(
            sequence=str(self.sequence_number).rjust(self.padding, '0'))
        for key in keys:
            try:
                value = getattr(self, key)
            except AttributeError:
                raise IdentifierMissingTemplateValue(
                    f'Required option not provided. Got \'{key}\'.')
            else:
                if value:
                    template_opts.update({key: value})
                else:
                    raise IdentifierMissingTemplateValue(
                        f'Required option cannot be None. Got \'{key}\'.')
        return template_opts


    @property
    def sequence_number(self):
        """Returns the next sequence number to use.
        """
        try:
            identifier_model = IdentifierModel.objects.filter(
                name=self.label).order_by('-sequence_number').first()
            sequence_number = identifier_model.sequence_number + 1
        except AttributeError:
            sequence_number = 1
        return sequence_number