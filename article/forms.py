from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):  # Bu sefer Forms almıyoruz ModelForm alıyoruz, bunun farkı ne peki? Bizim oluşturduğumuz Model (importladığımız Article) ile django'nun formunu
    class Meta:                      # bağlayarak bir model oluşturuyoruz.
        model = Article
        fields = ["title", "content", "article_image"]  # Sadece title ve content için field oluşturduk, çünkü diğer veriler author ve date olabilir ve biz bunları zaten hazır alıyoruz.
 