from django.contrib import admin
from autoimgApp.models import ContactMessage, WorkingDB
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class WorkingDBV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID','selectFile')
admin.site.register(WorkingDB, WorkingDBV)


class ContactMessageV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','subject','message','dateee')
admin.site.register(ContactMessage,ContactMessageV)
