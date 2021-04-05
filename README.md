# IMDB REST Application

### Prerequisite

Install following dependencies<br>
[Python 3](https://www.python.org/downloads/)<br>
[Mysql](https://dev.mysql.com/doc/refman/8.0/en/linux-installation.html)<br>
[Supervisor](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps)<br>

#### Setup 
.env file on server with required value 
```
DB_USER="root"
DB_PASS="as2d2p"
DB_HOST="localhost"
LOGGER_FORMAT="verbose"
DJANGO_SETTINGS_MODULE="imdb.db.settings.env"
PYTHONPATH=$PWD
```

Create virtual environment for python:
```
virtualenv -p python3.6 venv3
```

Source the environment
```
source ~/venv3/bin/activate
```

Install requirements.txt file
```
cd imdb
pip install -r requirements.txt
```

Start the service:
```
supervisord -c supervisord.conf
# python imdb/conf/service_app.py
```

Check the logs
```
tail -f logs/imdb-stderr.log
```


Stop the service:
```
supervisorctl -c supervisord.conf 
> stop app
> shutdown
```

User Credentials
```
username : sunil.saini
password : sunil@123
```

[Click Here for API Documantation](https://warped-crater-1182.postman.co/documentation/5313348-0236f6de-79ce-4e35-8fe3-504dd07a37fc/publish?workspaceId=61a11bb1-75df-4d09-824f-a28c5d053ea9)<br>

Postman Collection Link
```
https://www.getpostman.com/collections/bc0e993e702847208e9b
```