from rest_framework.serializers import SerializerMetaclass
from drf_serializer_data_cache.cache import cache
from drf_serializer_data_cache.settings import cache_settings
from drf_serializer_data_cache.signals import connect_cache_clear_signals
from drf_serializer_data_cache.utils import get_cache_key, get_serializer_model_base
from collections import OrderedDict


def model_bound_discover(serializer, res=None):
    if not res:
        res = set()
    model, serializer = get_serializer_model_base(serializer)
    if model:
        res.add(model)
    declared_fields = getattr(serializer, '_declared_fields', OrderedDict())
    for model_name in declared_fields:
        model_bound_discover(declared_fields[model_name], res)
    return res


class CacheClearSerializerMetaclass(SerializerMetaclass):
    def __new__(mcs, name, bases, attrs):
        serializer = super(CacheClearSerializerMetaclass, mcs).__new__(mcs, name, bases, attrs)
        if cache_settings.AUTO_DELETE_RELATED_CACHES:
            models = model_bound_discover(serializer)
            if models:
                connect_cache_clear_signals(models, serializer)
        return serializer


class ToRepresentationCacheMixin:
    def to_representation(self, instance):
        key = get_cache_key(instance, self)
        cached = cache.get(key)
        if cached:
            return cached
        super_to_representation = getattr(super(ToRepresentationCacheMixin, self), 'to_representation')
        assert super_to_representation and callable(
            super_to_representation), 'The `Serializer` has not `to_representation`'
        result = super_to_representation(instance)
        cache.set(key, result, cache_settings.SERIALIZER_CACHE_TIMEOUT)
        return result


class SerializerCacheMixin(ToRepresentationCacheMixin, metaclass=CacheClearSerializerMetaclass):
    pass
