# identifier
Identifier module

[![Coverage Status](https://coveralls.io/repos/github/Work-Res/identifier/badge.svg?branch=develop)](https://coveralls.io/github/Work-Res/identifier?branch=develop)

## Overview

The Application Identifier Management Module is designed to create and manage unique identifiers for applications within the system.
It ensures the accurate identification of applications and facilitates efficient management of their identifiers.

Add an applicant and application identifiers and other useful identifiers to your project

## Installation

Add to settings:

    INSTALLED_APPS = [
        ...
        'identifier.apps.AppConfig',
        ...
    ]

    
## Features

1. Identifier Generation: Automatically generates unique identifiers for new applications added to the system.
2. Identifier Management: Provides functionalities to manage and update identifiers for existing applications.
3. Validation: Ensures that identifiers adhere to specified formats and standards, maintaining consistency and accuracy.


## Identifier Format

* **Identifier type** refers to identifier type based on the application, whether it’s a work permit, resident, or visa etc.

* **Address code** refers to the resident's location, where administrative divisions (including cities, banners, and districts) have their own specific codes. (For example, the code for Serowe in central district in Botswana maybe 110102.) Change of address does not modify this code, however, which means that the code therefore reflects one's birthplace or the location of one's first-time card issuance.

* **Date of Birth** in the form YYYY-MM-DD.

* **Order code** is the code used to disambiguate people with the same date of birth and address code. Men are assigned to odd numbers, women assigned to even numbers.

* **The Checksum** is the final digit, which confirms the validity of the ID number from the first 17 digits, utilizing ISO 7064:1983, MOD 11-2.

	
### Identifiers

For example:

	from identifier.identifier import Identifier
	
	
	class WorkResidentPermitIdentifier(Identifier):
	    
	    template = '{identifier_type}{address_code}{dob}{sequence}'
	    label = 'work_resident_permit'  # e.g. work_permit_identifier, visa_identifier, etc
	    identifier_type = 'WR'
    
    work_resident_identifier = WorkResidentPermitIdentifier(
        subject_type_nameaddress_code='821', dob='07071989', label='wr_permit')
    >>> work_resident_identifier.identifier
    'WR8210707198900001-1'
    
    
 ### Short Identifiers

Creates a small identifier that is almost unique, for example, across 25 Edc devices in a community. We use these as sample requisition identifiers that are transcribed manually onto a tube from the Edc screen in a household. Once the sample is received at the local lab it is allocated a laboratory-wide unique specimen identifier.

    from identifier import ShortIdentifier
    
    >>> ShortIdentifier()
    ShortIdentifier('46ZZ2')

Add a static prefix -- prefix(2) + identifier(5):

	from identifier import ShortIdentifier
	
	class MyIdentifier(ShortIdentifier):
    	prefix_pattern = r'^[0-9]{2}$'
 	
    >>> options = {'prefix': 22}
    >>> id = MyIdentifier(options=options)
	>>> id
	MyIdentifier('22UYMBT')
	>>> next(id)
	'22KM84G'

Add a checkdigit -- prefix(2) + identifier(5) + checkdigit(1):

	from identifier import ShortIdentifier
	
	class MyIdentifier(ShortIdentifier):
    	prefix_pattern = r'^[0-9]{2}$'
    	checkdigit_pattern = r'^[0-9]{1}$'

    >>> options = {'prefix': 22}
    >>> id = MyIdentifier(options=options)
	>>> id
	MyIdentifier('223GF8A3')
	>>> next(id)
	'22DXVW23'

	
Add more to the prefix, such as address_ code and some other code.

	from identifier.short_identifier import ShortIdentifier	
	
	class SomeIdentifier(ShortIdentifier):
	    
		identifier_type = 'some_identifier'
		prefix_pattern = r'^[0-9]{4}$'
		template = '{address_code}{some_id}{random_string}'

		@property
		def options(self):
			if 'prefix' not in self._options:
				self._options.update(
					{'prefix': str(self._options.get('address_code')) + str(self._options.get('some_id'))})
			return self._options

    >>> options = {'address_code': 22, 'some_id': '12'}
    >>> id = SomeIdentifier(options=options)
	>>> id
	SomeIdentifier('22126MZXD')
	>>> next(id)
	'2212Y899C'

