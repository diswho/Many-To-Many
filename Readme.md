# Many-To-Many Relationships In FastAPI
In this tutorial, I cover multiple strategies for handling `many-to-many` relationships using `FastAPI` with `SQLAlchemy` and `pydantic`. I assume you already know of what these things are and how to use them in a basic sense.
 
[URL](https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/#intro)

[Github](https://github.com/ben519/fastapi-many-to-many/)



## Setting up EVN

```sh
python -m venv venv
```

```sh
venv\Scripts\activate
```

```sh
pip install SQLAlchemy
```
```sh
pip install pipreqs
```
```sh
pipreqs C:\Users\vieng\Documents\Workspaces\Python\Many-To-Many --force
```
```sh
pip install -r requirements.txt
```

## Run App

```sh
uvicorn main:app --reload
```