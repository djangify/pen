from django.contrib import admin
from .models import Tag, PromptCategory, WritingPrompt

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PromptCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class WritingPromptAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'category', 'difficulty', 'prompt_type', 'active')
    list_filter = ('category', 'difficulty', 'prompt_type', 'active', 'tags')
    search_fields = ('text',)
    filter_horizontal = ('tags',)
    
    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Prompt'

admin.site.register(Tag, TagAdmin)
admin.site.register(PromptCategory, PromptCategoryAdmin)
admin.site.register(WritingPrompt, WritingPromptAdmin)
