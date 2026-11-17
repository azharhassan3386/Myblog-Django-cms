# MyBlog (Django CMS)

## Chalane ka tarika (Windows)
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py makemigrations blog
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Mac/Linux: `source venv/bin/activate`

## Important URLs
- http://127.0.0.1:8000/            blog home
- http://127.0.0.1:8000/admin/      admin panel (categories, comments approve, visits)
- http://127.0.0.1:8000/post/new/   nayi post (login zaroori)
- http://127.0.0.1:8000/feed/rss/   RSS
- http://127.0.0.1:8000/sitemap.xml sitemap

## Subscribers ko email
    python manage.py notify_subscribers
(Development mein email terminal mein nazar aati hai.)
