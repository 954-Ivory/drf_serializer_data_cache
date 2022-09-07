"""
Settings for drf-serializer-data-cache are all namespaced in the
DRF_SERIALIZER_DATA_CACHE setting. For example your project's `settings.py` file
might look like this:

DRF_SERIALIZER_DATA_CACHE = {
    'SERIALIZER_CACHE_TIMEOUT': 86400
}

This module provides the `api_setting` object, that is used to access
drf-serializer-data-cache settings, checking for user settings first, then falling
back to the defaults.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.test.signals import setting_changed

DEFAULTS = {
    'SERIALIZER_CACHE_BACKEND': 'default',
    'SERIALIZER_CACHE_TIMEOUT': 86400,
    'AUTO_DELETE_RELATED_CACHES': True,
}


class APISettings(object):
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:

        from drf_serializer_data_cache.settings import api_settings
        print(api_settings.SERIALIZER_CACHE_TIMEOUT)

    """

    def __init__(self, defaults=None):
        self.defaults = defaults
        self.settings = getattr(settings, 'DRF_SERIALIZER_DATA_CACHE', {})

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        return val


cache_settings = APISettings(DEFAULTS)


def reload_api_settings(*args, **kwargs):
    global cache_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'DRF_SERIALIZER_DATA_CACHE':
        cache_settings = APISettings(DEFAULTS)


setting_changed.connect(reload_api_settings)
