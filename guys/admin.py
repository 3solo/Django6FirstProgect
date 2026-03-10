from django.contrib import admin

from guys.models import FloodMessages, Category, News, Topic, TopicMessages


@admin.register(FloodMessages)
class FloodMessagesAdmin(admin.ModelAdmin):
    list_display = ('user','message', 'time_drop')
    list_filter = ('user', 'time_drop')
    search_fields = ('message',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_drop')
    list_filter = ('time_drop',)
    search_fields = ('title', 'content',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_time',)
    list_filter = ('category', 'created_time',)
    search_fields = ('title',)


@admin.register(TopicMessages)
class TopicMessagesAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_time',)
    list_filter = ('topic', 'author', 'created_time',)
    search_fields = ('content',)



