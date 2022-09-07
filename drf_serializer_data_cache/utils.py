from django.db.models import Model
from django.db.models.base import ModelBase


def get_module_name(obj):
    name = getattr(obj, '__name__', obj.__class__.__name__)
    module = getattr(obj, '__module__', obj.__class__.__module__)
    return f'{module}.{name}'


def get_cache_key(instance, serializer):
    if isinstance(instance, Model):
        format_dict = {
            'pk': instance.pk,
            'instance': get_module_name(instance),
            'serializer': get_module_name(serializer),
        }
        format_str = '{instance}:{serializer}:{pk}'
        return format_str.format(**format_dict)


def get_dispatch_uid(model):
    if isinstance(model, ModelBase):
        format_dict = {
            'model': get_module_name(model),
        }
        format_str = '{model}'
        return format_str.format(**format_dict)


def get_serializer_model_base(serializer):
    child = getattr(serializer, 'child', None)
    serializer = child or serializer
    meta = getattr(serializer, 'Meta', None) or getattr(serializer, 'queryset', None)
    model = getattr(meta, 'model', None)
    return model, serializer


def get_relation_fields(model):
    res = []
    fields = model._meta._get_fields(reverse=True)
    for field in fields:
        if field.is_relation:
            lookups_key = field.name
            related_model = field.related_model
            if lookups_key and related_model:
                res.append([related_model, lookups_key])
    return res
