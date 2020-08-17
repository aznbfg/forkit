# Forkit
Create a web service which will fork it's own Github repo to a user's account.

## Requirements

Python3.7
virtualenv
make
uwsgi

## Create vm

```
make vm_create
```

## Activate vm

```
source vm/bin/activate
```

## Install pip requirements

```
make pip_install
```

## Usage

For testing run:

```
make flask_run
```

For production use uwsgi + sysd + nginx + letsencrypt or something

## Settings

We need to configure settings for github creds like so:

```
github:
  client_id: ...
  client_secret: ...
```

In yaml format.  Pass to app.py with -c or --config
