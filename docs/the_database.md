# The Database

For this tutorial we will be using a SQLite database containing customers and orders.  
You should copy /databases/grid_tutorial.db from this repo and copy to your application /databases folder.

Once that is done we need to make a couple of changes to settings.py

Find 

```python
DB_URI = "sqlite://storage.db"
``` 

and change it to 

```python
DB_URI = "sqlite://grid_tutorial.db"
```

Next, find 

```python
DB_FAKE_MIGRATE = False
``` 

and change it to 

```python
DB_FAKE_MIGRATE = True
```

We'll add the different model definitions to models.py as we go along.


[Back to Index](../README.md)