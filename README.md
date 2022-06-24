<img height="200" src="C:\Users\Vasily\PycharmProjects\foodate\static\images\fav\android-chrome-512x512.png" alt="FooDate logo"/>

## FooDate web application

### Setup:
1. Clone FooDate repository:
```commandline
git clone https://github.com/vasil1y-777/FooDate Clone FooDate repository
```

2. Open project folder:
```commandline
cd foodate
```
3. Checkout branch if necessary:
```commandline
git checkout develop
```

3. Create .env file in project directory with:
```dotenv
SECRET_KEY = 'random_secret_key'
DEBUG = True
```

4. Install requirements.txt\
```commandline
pip install -r requirements.txt
```

5. Start the server (--insecure for production or DEBUG=False)
```commandline
python manage.py runserver host:port --insecure
```