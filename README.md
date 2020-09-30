# DjangoWebPortal => Portal for students (eDeanOffice)

I've created application for students to sign up for classes. Plans are created automatically 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to run the software is postgresql database and pg_config. You can edit parameters to database in mainproject/settings.py
You also need python3 and pip.

### Installing

Build virtual environment with this command:
```
python3 -m venv ./venv
```
You have to activate it with command:
```
. venv/bin/activate
```
and then install all requirements:
```
pip install -r requirements.txt
```
and then (last, I swear) run command:
```
python manage.py migrate
```

I suggest to add example data before you will start destroying my lovely application. Run python from shell:

```
python manage.py shell
```

and put this commands:

```python
from accounts.add_data import add_data
from entities.add_data import add_entities
add_data()
add_entities()
quit()
```

Now you can run it using:

```
python manage.py runserver
```

end now you can go to localhost:8000 and you will see welcome page.

## Running the tests

To run all tests put:

```
python manage.py test
```

To run tests from one module (or file) put (for example):
```
python manage.py test entities.tests.file
```

## Authors

* **Adam S** it was me

## License

It would be an honor for me if it can help you or it would be useful for you.
Don't pay, get for free.

## The END

* Hat tip to anyone whose code was used: many websites
* Inspiration: I've hated plans for laboratory's groups at my university. Now I know that it is hard to be good for everyone :-(
