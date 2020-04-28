from django.db.models.fields import FloatField, IntegerField, DecimalField, CharField, DateField, DateTimeField
from rest_framework import viewsets, serializers, routers
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters
#from rest_framework.permissions import IsAdminUser
from django.apps import apps


DEFAULT_MODELS = ["ContentType", "Group", "LogEntry", "Permission", "Session", "User"]


class RouterFactory(object):
    """
        need to realise
        ViewSet
        Serialiser
    
    """

    def _get_router(self,
                    viewset_cls=None, serialiser_cls=None,
                    permissions=None, pagination_cls=None,
                    models=None):
        
        autogen_router = routers.DefaultRouter()

        viewset_cls     = viewset_cls or viewsets.ModelViewSet
        serialiser_cls  = serialiser_cls or serializers.ModelSerializer
        
        pagination_cls  = LimitOffsetPagination
        #permissions     = permissions or (IsAdminUser,)
        models          = models or apps.get_models()
        
        models = [m for m in models if m.__name__ not in DEFAULT_MODELS]
        models = sorted(models, key=lambda m: m.__name__)
        
        
        for model in models:
            resource_name = model.__name__

            cls_props = {
                'queryset': model.objects.all(),
                'pagination_class': pagination_cls,
                #'permission_classes': permissions,
                'serializer_class': type('{0}Serialiser'.format(resource_name), (serialiser_cls,), {
                    'Meta': type('Meta', (object,), {
                        'model': model,
                        'fields': '__all__'
                    })
                })
            }

            fields_defs = self._build_filters_for_model(model)
            cls_props['filterset_class'] = type('{0}Filter'.format(resource_name), (filters.FilterSet,), {
                'Meta': type('Meta', (object,), {
                    'model': model,
                    'fields': fields_defs
                })
            })
            
            cls_config = type('{0}ViewSet'.format(resource_name), (viewset_cls,), cls_props)

            print('registering_resource', resource_name, cls_config)
            autogen_router.register(resource_name, cls_config)

        return autogen_router
    
    
    def _build_filters_for_model(self, model):

        fields_defs = {}

        all_fields = model._meta.get_fields()
              
        core_fields = [
            f for f in all_fields if (f.concrete)
                                     and not (f.one_to_many or f.one_to_one or f.many_to_many)
        ]
        numeric_fields = [
            f for f in core_fields if isinstance(f, (FloatField, IntegerField, DecimalField))
        ]
        txt_fields = [
            f for f in core_fields if isinstance(f, (CharField,))
        ]
        date_fields = [
            f for f in core_fields if isinstance(f, (DateField, DateTimeField,))
        ]
        related_fields = [
            f for f in all_fields if (f.concrete) and (f.one_to_many or f.one_to_one)
        ]
        related_operators = ['exact', 'in', 'gt', 'gte', 'lt', 'lte', 'isnull']
        txt_operators = ['exact', 'in', 'contains', 'regex', 'isnull']
        num_operators = ['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull']
        date_operators = ['exact', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull']

        for f in all_fields:
            if f in numeric_fields:
                operators = num_operators
            elif f in txt_fields:
                operators = txt_operators
            elif f in date_fields:
                operators = date_operators
            elif f in related_fields:
                operators = related_operators
            else:
                operators = []

            fields_defs[f.name] = operators

        return fields_defs


    def get_default_router(self):
        '''
        Gets a default router pre-configured for all models
        :return: The default router pre-configured for all models
        '''
        return self._get_router()
