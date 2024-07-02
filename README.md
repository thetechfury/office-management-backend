# office-management-backend
## Clone project files from repository
    git clone https://github.com/thetechfury/office-management-backend.git
## Create virtual environment
    python -m venv venv
### Activate the virtual environment
    # for windows   
    .\venv\Scripts\Activate.ps1
    
    # macOS/Linux
    source venv/bin/activate

### Install dependencies
    pip install -r requirements.txt

### Run migrations
    python manage.py migrate

### Run server
    python manage.py runerver

### Packages used
    Django==4.2.13
    djangorestframework==3.15.1    
    used to create APIs in django
    drf-yasg==1.21.7 
    used to automatically generate swagger file of APIs
    Pillow==10.3.0  
    used to support images
    django-filter==24.2 
    used to auomatically filter data  w.r.t to look up field by mentioning it in viewset 
    