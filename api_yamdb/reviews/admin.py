from django.contrib import admin

from reviews.models import Category, Genre, Title, User, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


class GenreAdmin(CategoryAdmin):
    pass


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "year", "description")
    search_fields = ("name", "year")
    list_filter = ("category",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "role", "bio")
    search_fields = ("username",)
    list_filter = ("role",)
    list_editable = ("username", "email", "role", "bio")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "score")
    search_fields = ("title",)
    list_filter = ("score",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text")
    search_fields = ("review",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
