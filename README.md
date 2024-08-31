# Command to execute project

#*Using Liveserver*

Make sure you are in root directory of your project folder
 ```python manage.py runserver```
 
Output will be available on **http://127.0.0.1:8000/letterCreation/form**

**For editing html pages**

Pages are avilable on letterGenerate/templates_ folder

#*Using Docker*

***Create a .env file and add below contents***
```
POSTGRES_HOST=db
POSTGRES_USER=DFSL_users
POSTGRES_PASSWORD=admin
POSTGRES_DB=LetterGeneration
SECRET_KEY='django-insecure-7u3s$1#@1e$%gpj4x!co8=3m65b=qr_5x^_0*knn49-&gcuymg'
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
DJANGO_SUPERUSER_USERNAME=DFSL_users
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin
```
***To build the docker image***
```
docker-compose up -d --build
```

