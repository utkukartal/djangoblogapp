from django.contrib import admin

from .models import Article, Comment # Bulunduğumz dosyadaki modelsten (o yüzden .models) Article ı alıyor

# Register your models here.

"""admin.site.register(Article)   Bu komut ile registerlıyoruz."""  # Bunu commente aldık, yine kullanıoyruz fakat decoratar olarak kullanacağız 201
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author","created_date"]  # Genel article sayfasında hangi bilgilerin gösterilmesini istiyorsak
    list_display_links = ["title", "created_date"]  # Bununla yukarıda displaylediğimiz hangi verinin link özelliği göreceğini belirliyoruz
    search_fields = ["title"]   # title arayabileceğimiz search field
    list_filter = ["created_date"]  # ekranın sağında süzmek için kullanabileceğimz kısım, zaman yerine title, author vb yapılabilir

    class Meta:  # Bu classın spesifik bir şekilde meta olması gerekiyor.
        model = Article  # Bununla Aritcle ile ArticleAdmin i birleştirmiş oluyoruz.

admin.site.register(Comment)  # Admin paneli için özel bir model oluşturmuyoruz, bastiçe kaydediyoruz.