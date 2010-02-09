from models import *
from django.contrib import admin

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1

class PositionAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]

admin.site.register(Election)
admin.site.register(Vote)
admin.site.register(Position, PositionAdmin)

