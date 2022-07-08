"# Django Blog App" 

Clone
```
https://github.com/utkukartal/djangoblogapp.git
```

Install Dependecies
```
  pip install -r requirements.txt
```

Setting Database
```
  python manage.py makemigrations
  python manage.py migrate
```

Creating Superuser
```
  pythun manage.py createsuperuser
```

You will need to change certain things to your preference such as messages and raise errors, and at blog/settings.py you need to add your own domain to ALLOWED_HOSTS.

I used Python 3.8, other versions might work but I'm not certain about it.
