from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
        
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():  # biz bu methodu kullandığımız zaman, forms.py altındaki clean çağrılıyor.  
        username = form.cleaned_data.get("username")  # forms.py içinde values'a hangi key ile kaydettiysek o key'i kullanmamız gerekiyor.
        password = form.cleaned_data.get("password")
            
        newUser = User(username = username)
        newUser.set_password(password)  # Django Shell ile db'ye kaydetme methodları
        newUser.save()

        # login(request, newUser)  # bir nevi session başlatmak, fakat register olunca direk login olmasınalr istiyorum.
        messages.success(request, "Başarıyla kayıt olundu, lütfen giriş yapınız.")
        return redirect("user:login")  # Kayıt olunduktan sonra direkt loginlemek ve anasayfaya yönlendirmek saçma login ekranına gitmeli

    context = {
        "form": form
    }
    return render(request, "register.html", context) # Context tipi sözlük olmak zorunda olduğu için yukardakini yaptık.
    
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():  # biz bu methodu kullandığımız zaman, forms.py altındaki clean çağrılıyor.  
            username = form.cleaned_data.get("username")  # forms.py içinde values'a hangi key ile kaydettiysek o key'i kullanmamız gerekiyor.
            password = form.cleaned_data.get("password")
            
            newUser = User(username = username)
            newUser.set_password(password)  # Django Shell ile db'ye kaydetme methodları
            newUser.save()

            login(request, newUser)  # bir nevi session başlatmak

            return redirect("index")
        else:
            context = {
                "form": form
            }
            return render(request, "register.html", context)

    else:
        form = RegisterForm()
        context = {
            "form": form
        }
        return render(request, "register.html", context)"""  

def loginUser(request):
    form = LoginForm(request.POST or None)
    context= {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")  # Burada kafalar karışabilir bir miktar çünkü LoginForm'da cleaned_data belirtmedik. Clean methoduda yok zaten. Bu sıkıntı oluşturmuyor çünkü clean methodu
        password = form.cleaned_data.get("password")  # biz belirtmesekte formlarda tanımlanıyor ve biz burada cleaned_data.get yaparak direkt veriyi alabiliyoruz.

        user = authenticate(username = username, password = password)  # User'ın db'de olup olmadığını kontrol edip user'a atıyor

        if user is None: # Yukarıdaki kontrolde kullanıcı bulunmazsa None döner
            messages.info(request, "Kullanıcı adı veya parola hatalı.")
            return render(request, "login.html", context)
        
        messages.success(request, "Başarıyla giriş yapıldı.")
        login(request, user)
        return redirect("index")
    
    return render(request, "login.html", context)

@login_required(login_url = "user:login")            
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yapıldı.")
    return redirect("index")
    