"""Uber call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.exceptions import ResponseError
from ubersmith.calls import BaseCall, FileCall
from ubersmith.utils import prepend_base

__all__ = [
    'ApiExportCall',
    'CheckLoginCall',
    'ClientWelcomeStatsCall',
    'MethodGetCall',
    'DocumentationCall',
]

_ = prepend_base(__name__.split('.')[-1])


class ApiExportCall(BaseCall):
    method = _('api_export')
    required_fields = ['table']


class CheckLoginCall(BaseCall):
    method = _('check_login')
    timestamp_fields = [
        'last_login',
        'password_changed',
    ]

    def process_request(self):
        # if login invalid just have the call return false
        try:
            super(CheckLoginCall, self).process_request()
        except ResponseError, e:
            if e.error_code == 3 and \
               e.error_message == 'Invalid login or password.':
                self.response_data = False
            else:
                raise  # re-raises the last exception

    def clean(self):
        # don't clean if response was False
        if self.response_data:
            super(CheckLoginCall, self).clean()
        else:
            self.cleaned = False


class ClientWelcomeStatsCall(BaseCall):
    method = _('client_welcome_stats')
    required_fields = ['client_id']
    timestamp_fields = ['client_activity']
    date_fields = ['next_inv']
    int_fields = [
        'client_activity_type',
        'closed_count',
        'inv_count',
        'pack_count',
        'ticket',
        'type',
    ]


class MethodGetCall(BaseCall):
    method = _('method_get')


class DocumentationCall(FileCall):
    method = _('documentation')
