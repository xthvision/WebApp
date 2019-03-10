# sihFinalWebapp
the final webapp

## Functions 

### to read a doc file and extract important information from it. The test cases and the range of values
### Now load multiple pdf file and verify if the results are in given range or not.


This is the complete web app the api can be modeled over it 


### dependencies 
#### postgresql 
#### opencv, numpy, djngolatest, python3, pip3, psypog, pillow 
#### pandas, torch, camelot
#### etc check it out during installation

The steps to understand this app is below


gnbm
create virtual env
virtualenv xthvision

> source oreancv/bin/activate (to go into virtual env)
> django-admin startproject nameOfProject
> cd to project directory
> install django in virtualenv
> pip install django
>> add .gitignore file in root directory
>> in settings.py add these lines to change db to postgresql
	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'producthuntdb',
        'USER': 'postgres',
	'PASSWORD': '2437@orean',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

>> also create db in postgres admin 
	sudo su postgres
	psql
	CREATE DATBASE databasenme;
>> pip install psycopg2
> python manage.py migrate
>>> Products app
>>> accounts app (to manage user and signup)
>>> python manage.py startapp accounts
>>> python manage.py startapp products


 
> add path of app in settings
	in this manner 'products.apps.ProductsConfig'
	where ProductsConfig is the class name in app



> Create url for home page
	in urls.py add path to home page, the home lives in products
	so import views from products and creare path and create function in views 		to handle request

	from products import views #import views from prodcuts
	path('', views.home, name='home'), # create path
	
	def home(request):
    		return render(request, 'products/home.html')	
	
	create templates/projects/home.html and html code



> 	if you want to add basic template create a templates folder in root 		dir(which is inside the first and conatins urls.py) and add base.html to it
	add path to base templates in settings.py
	'DIRS': ['producthunt/templates'], (if templates is in producthunt folder)

	use this to extend the template
		{% extends 'base.html' %}
		{% block content %}
		{% endblock %}
	the base.html will be like
		<header>
		{% block content %}
		{% endblock %}
		<footer>

>	add static files such as site logo in static folder in root
	add static url and path to static in settings.py of root
		STATICFILES_DIRS = [
		    os.path.join(BASE_DIR, 'producthunt/static')
		]	
		STATIC_ROOT = os.path.join(BASE_DIR, 'static')
		STATIC_URL = '/static/'

	run python manage.py collectstatic
	this will create a static file in main root dir

// Now handling the signup and login

	>> add path to accounts app in urls.py rest follow as above
	>> this time we are redirecting tu urls present in accounts
		   from django.urls import path, include

		   path('accounts', include('accounts.urls'),
		
	>> create urls.py in accounts
		from django.urls import path, include
		from . import views

		urlpatterns = [
		    path('signup/', views.signup, name = 'signup'),
		    path('login/', views.login, name = 'login'),
		    path('logout/', views.logout, name = 'logout'),
		]
	>> Now add these functions in views of accounts

	>> add the necessary hml code 
	>>> make the form post to {% url 'signup' %} to make a post request to 		    view.py signup method 

		def signup(request):
		    if request.method == "POST":
		        return "do this"
    		    else:
        		return render(request, 'accounts/signup.html')
	   after this you gotta bring in two modules
		from django.contrib.auth.models import User
		from django.contrib import auth

	   now in views.py write the function to check entries, if entries are fine
	   in a try catch block check for existing user if does not exists create an
	   account.

		
		 try:
	                user = User.objects.get(username=request.POST['username'])
	                return render(request, 'accounts/signup.html', 				{'error':"User already exists"}) 
            	except User.DoesNotExists:
                	user = User.objects.create_user(request.POST['username'], 				password=request.POST['password)
                	auth.login(request, user)
                	return redirect('home')


	>> now once the user is created you can login a post method form with 
	   csrf token inclued.

	>> handling post request in views.py

		if request.method == 'POST':
		        #do something
        		user = auth.authenticate(username=request.POST['username'], 				password=request.POST['password'])
        		if user is not None:
            			auth.login(request, user)
            			return redirect('home')
        		else:
            			return render(request, 'accounts/login.html', 					{'error': 'User name or password is inccorect'})
    		else:
        		return render(request, 'accounts/login.html')   
	>> aut.autenticate is used to authenticate 

	>> you can check on pages if its a logined user or not using
		{% if user.is_authenticated %}

	>> create a super user also so that you can acess users from console


// This part involves creating models for database.

	>> in the product models.py create a class Product 
	   add all the neceary fileds
	>> to add image filed you will have to install 
	   pillow

	>> import user to create foregin key bindings
	   from django.contrib.auth.models import User


	>> run migrate
	>> add product to admin.py of products
		from django.contrib import admin
		from . models import Product

		# Register your models here.
		admin.site.register(Product)

	>> to add products which only logined people can add
	   add the paths and reach the function
	   in thhe before fucntion just add 
		
		@login_required
		def create(request):
    			return render(request, 'products/create.html')
	   
	   which can be only used when you import
		from django.contrib.auth.decorators import login_required
	>> fetch the data in the function which is handling the post request sent 	     from the form

	>> createa the model object also import it from models
	>> save it 
	>> to use timezone function from django.utils import timezone

		def create(request):
    			if request.method == 'POST':
        			if request.POST['title'] and request.POST['body'] 					and request.POST['url'] and request.FILES['image'] 					and request.FILES['icon']:
            				product = Product()
            				product.title = request.POST['title']
            				product.body = request.POST['body']
            				if request.POST['url'].startswith('http://') 						orrequest.POST['url'].startswith
					('https://'): 
                				product.url = request.POST['url']
            				else:
                				product.url = 							'http://'+request.POST['url']
            
            				product.icon = request.FILES['icon']
            				product.image = request.FILES['image'] # for 						files its not post
            				product.pub_date = timezone.datetime.now()
            				product.hunter = request.user #current user
            				product.save() #upload value to db
            				return redirect('home')

        			else:
            				return render(request, 						'products/create.html', {'error:' 'Please 						fill all the fields'})
    			else:
        			return render(request, 'products/create.html')


	>> now you can upload data

// acessing media 

	>> to acess media you will have to add static path after the path in urls.p of main also import settings and static models
		from django.conf.urls.static import static 
		from django.conf import settings		

		static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
	>> now you need to add paths in settings.py of main file
	>> adding media root to settings of main project

		
		MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
		MEDIA_URL = '/media/' 


// now rendering the cdetails of product once user creates a product

	>> you will have to add dynamic url path to roducts urls.py file
		path('<int: product_id>', views.detail, name='detail'),
	>> the int value can be replaced by any int value now add a function to 
	   handle such url in views.py
	>> to get an sepcific object you will have to import
		from django.shortcuts import render, redirect, get_object_or_404
		
		def detail(request, product_id): #product id can be used to rerurn 			specific page
		product = get_object_or_404(Product, pk=product_id)
    		return render(request, 'products/detail.html', {'product': product})
	404 method used to gey product from db and passed to template
	
	>> from the prouct id redirect to 'products/productID'
	































	
	





























