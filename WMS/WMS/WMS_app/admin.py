from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import (
    Vendor,
    Task,
    DependencyResolution,
    EmailLog,
    TechLog,
    Assignment
)

class TechLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'username', 'change_type')
    list_filter = ('date', 'username')
    search_fields = ('username', 'change_type')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    actions = ['export_as_csv']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'event', 'email_status', 'user_id', 'username', 'phone')
    list_filter = ('event', 'email_status')
    search_fields = ('user_id', 'username', 'phone')
    ordering = ('-created_at',)
    actions = ['export_as_csv']

    def email_status(self, obj):
        return 'Sent' if obj.subject else 'Not Sent'
    email_status.short_description = 'Email Status'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

class TaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'submission_time', 'username', 'task', 'hours', 'status', 'dependency', 'communication_of_change')
    search_fields = ('username', 'task')
    list_filter = ('date', 'username', 'status')
    date_hierarchy = 'date'
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('task_to_work_on', 'date_of_assignment', 'expected_date_of_delivery', 
                   'assigned_by', 'assign_to', 'date_of_delivery_by_assignee', 'mark_as_complete')
    list_filter = ('assigned_by', 'assign_to', 'expected_date_of_delivery', 'mark_as_complete')
    search_fields = ('task_to_work_on', 'assigned_by__username', 'assign_to__username')
    actions = ['export_as_csv']

    fieldsets = (
        ('Assignment Details', {
            'fields': ('task_to_work_on', 'type_of_task', 'date_of_assignment', 'expected_date_of_delivery')
        }),
        ('People Involved', {
            'fields': ('assign_to', 'assigned_by', 'approved_by')
        }),
        ('Completion Status', {
            'fields': ('expected_hours_by_assigner', 'expected_hours_by_assignee',
                      'date_of_delivery_by_assignee', 'mark_as_complete')
        }),
    )

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

class DependencyResolutionAdmin(admin.ModelAdmin):
    list_display = ('task', 'resolved_date', 'dependency', 'resolved_by')
    search_fields = ('task__task', 'resolved_by', 'dependency')
    list_filter = ('resolved_date', 'resolved_by', 'dependency')
    date_hierarchy = 'resolved_date'
    actions = ['export_as_csv']

    def dependency_on(self, obj):
        return obj.task.dependency
    dependency_on.short_description = 'Dependency'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

# Register models
admin.site.register(Vendor)
admin.site.register(Task, TaskAdmin)
admin.site.register(DependencyResolution, DependencyResolutionAdmin)
admin.site.register(TechLog, TechLogAdmin)