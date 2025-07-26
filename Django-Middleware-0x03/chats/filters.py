import django_filters
from .models import Message


class Messagefilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='sender_id__username',
                                     lookup_expr='icontains')
    start_time = django_filters.DateTimeFilter(field_name='timestamp',
                                               lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='timestamp',
                                             lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'start_time', 'end_time']
