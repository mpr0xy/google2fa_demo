install dependence
==================
```
pip install flask

cd python-googauth
python setup.py install

```

init database
=============
```
from google2fa.py import init_db
init_db()
```

start 
=====
```
python google2fa
```


use
===
`/add/usernmae`

Use Google Authenticator get the QR code 


`/verify/username/code`

Show the verify of the code from Google Authenticator







