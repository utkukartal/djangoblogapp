from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = "Yazar")  # Biz burada ForeignKey ile başka bir tablodaki objeye erişiyoruz ve db içinde hazır bulunan auth.User tablosuna erişiyoruz. on_delete ile
    # bu objenin yani userin silinmesi durumunda ne olacağını belirliyoruz, models.CASCADE ile bu user silinirse bu user tarafından yazılmış Articlelar da silinsin diyoruz. 
    title = models.CharField(max_length = 50, verbose_name = "Başlık")
    # content = models.TextField(verbose_name = "İçerik")  # models den gerekli fieldlar ile oluşturuyoruz.
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Oluşturulma Tarihi")  # Dbye veri eklendiği anda o anki tarihi created_date e atayacak 
    # verbose_name = "" ile admin panelinde bunların nasıl görüneceğini belirliyoruz.
    # Aşağıdaki method ile de articles içinde değilde genel penceredeki görünüşünü değiştirmek için gerçekleştiriyoruz.
    article_image = models.FileField(blank = True, null = True, verbose_name = "Makaleye Fotoğraf Ekleyin")  # Blank ve null'u true yaptık, dolmasına gerek olmadığı için.
    def __str__(self):  # Buna gerek kalmadı, admin modeli ile admin.py de genel olarak ekledik zaten.
        return self.title 
    
    class Meta:  # Article ve aşağıdaki Comment modellerine eklediğimiz bu class'ın amacı aşağıdaki satırdan anlaşılabileceği gibi order'ı yani sıralamayı değiştirmek. Normalde ilk eklenen ilk gözüküyor created_date'e göre yani başına eksi koyunca tersi oluyor.
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name = "Makale", related_name = "comment")
    comment_author = models.CharField(max_length = 50, verbose_name = "İsim")
    comment_content = models.CharField(max_length = 200, verbose_name = "Yorum")
    comment_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.comment_content
    
    class Meta:
        ordering = ['-comment_date']
