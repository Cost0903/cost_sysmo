from django.contrib import admin
from django.forms import widgets
from .models import Machine, MachineGroup, Policy, Performance
from django.utils.html import format_html, format_html_join
import json
from django.db.models import JSONField
from sysmo.settings import logging
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms import Widget

# Register your models here.

# class PrettyJSONWidget(widgets.Textarea):

#     def format_value(self, value):
#         try:
#             value = json.dumps(json.loads(value), indent=2, sort_keys=True)
#             # these lines will try to adjust size of TextArea to fit to content
#             row_lengths = [len(r) for r in value.split('\n')]
#             self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
#             self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
#             return value
#         except Exception as e:
#             return super(PrettyJSONWidget, self).format_value(value)


class JSONWidget(Widget):

    def __init__(self, html_path, attrs=None):
        self.template_name = html_path
        super(JSONWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        logging.info(f"{name} : {value}")
        """Render the widget as an HTML string."""
        # context = self.get_context(name, value, attrs)
        context = {'value': json.loads(value), 'name': name}
        logging.info(context)
        return mark_safe(render_to_string(self.template_name, context))


class MachineAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'owner', 'group')
    list_filter = ('owner', 'group')
    readonly_fields = ('ruuid')
    search_fields = ('hostname', 'owner__username', 'group__name')
    fieldsets = (
        ('主機資訊', {
            'fields': ('hostname', 'description', 'ruuid')
        }),
        ('群組資訊', {
            'fields': ('group', 'owner')
        }),
        ('硬體資訊', {
            'fields': ('disk_info', 'network_info')
        }),
        # ('硬碟資訊', {
        #     'fields': ('disk_info')
        # }),
    )

    formfield_overrides = {
        JSONField: {
            'widget': JSONWidget("json_widget.html")
        }
    }

    def network_json(self, obj):
        trans_json = eval(str(obj.network_info))
        return format_html_join(
            "\n", """
            <div>Interface : {}</div>
            <div>ipv4 : {}</div>
            <div>mac : {}</div>
            """, ((interface, obj.network_info[interface].get("ipv4"),
                   obj.network_info[interface].get("mac"))
                  for interface in obj.network_info.keys()))

    network_json.short_description = '網卡資訊'


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'cpu_usage', 'mem_usage', 'swap_usage',
                    'disk_usage', 'datetime')
    # readonly_fields = ('datetime')
    # list_filter = ('machine', 'datetime')
    search_fields = ('machine__hostname', 'machine__owner__username',
                     'machine__group__name')


admin.site.register(Machine, MachineAdmin)
admin.site.register(MachineGroup)
admin.site.register(Policy)
admin.site.register(Performance, PerformanceAdmin)
