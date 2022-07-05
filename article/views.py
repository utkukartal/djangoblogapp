from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required

from .forms import ArticleForm
from .models import Article, Comment
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")  # Makaleler sayfasında bir arama işlemi yapıldığında keyword oluşacak ve bu get methoduna bağlı, eğer var ise keyword değişkenine atıyoruz.
    
    if keyword: # Sadece arama işlemi yapıldıysa oluşacak
        articles = Article.objects.filter(title__contains = keyword)  # Burada girilen arama inputuna göre filtreliyoruz
        return render(request, "articles.html", {"articles": articles})
    
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles": articles})

def index(request):  # Request muhabbeti flaskta da bahsettiğimiz istek muhabbetleri GET POST vb.
    # return HttpResponse("<h3>Ana Sayfa</h3>")  # Direk http response dönüyoruz.
    return render(request, "index.html")  # Bu seferde renderladık, flask a benzer fakat küçük değişiklikler var render'ın çalışma mantığından dolayı request'i de gönderdik. direk templates altında değilse belirtmemiz gerekir. Bu kısımda eklediğimiz sözlük context, templatelarla veri gönderme muhabbetleri ile alakalı

def about(request):
    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)  # Loginlenmiş olan user tarafından oluşturulan tüm article'ları verir.
    context = {
        "articles": articles
    }

    return render(request, "dashboard.html", context)

@login_required(login_url = "user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)  # Buradaki request.FILES dosya ekleme muhabbeti için, upload'lanacak dosya bu request'in FILES'ında bulunuyor.
    context = {
        "form": form
        }
    if form.is_valid():
        article = form.save(commit = False)  # Aşırı basit, bizim şu an eldeki form bir ModelForm olduğu için form.save() deyince direkt db'ye kaydediyor. Fakat bir sıkıntısı var, o da author ile alakalı. Hangi user'ın bu article'ı girdiğini bilmiyor. Bundan dolayı ilk olarak commit'lememesi için False diyoruz ardından şu anki login durumunda olan user'ı author olarak veriyoruz.
        article.author = request.user  # Author'u ekliyoruz
        article.save()

        messages.success(request, "Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")
    return render(request, "addarticle.html", context)

def detail(request, id):  # Dinamik url olduğu için id'yi de aldık
    # article = Article.objects.filter(id = id).first()  # Burada first diye spesifik bir şekilde belirtmemiz gerekiyor, zaten tek bir eleman var fakat yine de bir liste içinde getiriyor bu da template'da erişim sıkıntısı oluyor.
    article = get_object_or_404(Article, id = id)  # Yukarıdaki line'ı iptal ettik 224. derste details sayfasında bulunmayan articlelar için hata ekranı oluşturudyorduk. Bu kısım için bu satırı oluşturduk
    comments = article.comment.all()  # Burada üst satırda alınan article'a ait tüm commentleri alıyoruz. Comments modelini oluştururken bu bağlantıyı yapmıştık.
    return render(request, "detail.html", {"article": article, "comments": comments})

@login_required(login_url = "user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)  # instance ile gönderdiğimiz objenin içindeki bilgiler buradaki formların içine yazılacak.
    
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()

        messages.success(request, "Makale başarıyla güncellendi.")
        return redirect("article:dashboard")
    
    return render(request, "update.html", {"form": form})

@login_required(login_url = "user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.success(request, "Makale başarıyla silindi.")
    return redirect("article:dashboard")

def addComment(request, id):
    article = get_object_or_404(Article, id = id)
    
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")  # Request ile girilen bilgileri html'dan aldık.
        comment_content = request.POST.get("comment_content")
        
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)  # Comment modelinde bir obje oluştururken request ile aldığımız bilgileri atıyoruz.
        newComment.article = article  # Article bilgisini id'den almıştık zaten onu da atıyoruz
        newComment.save() # Yaptığımız değişiklikleri kaydediyoruz.
    
    return redirect(reverse("article:detail", kwargs = {"id": id}))  # daha dinamik olması için reverse'ü import ettik ve kullandık. detail dinamik olduğu için id'yi kwargs ile ekledik.
    # return redirect("/articles/article/" + str(id)) redirect işlemini böyle yapabiliriz fakat dinamikliğe ters.