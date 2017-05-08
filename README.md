### Libr

The purpose of Libr is to create a web application that can be used to
present files, especially PDF files, in a way that makes them easy to
browse and explore.


#### Running Libr
Libr can be ran using gunicorn (or similar WSGI servers).
Ex. `gunicorn -w 1 --log-level debug libr:app`.
