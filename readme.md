# Flask Paywall

Setup a paywall with Flask and Stripe to offer paid access to your premium content.

## Workflow

1. User registers and pays
3. User obtains access to premium content

## QuickStart

### Set Environment Variables

Rename *config_sample.py* to *config.py*, update the config settings, and then run:

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
```

### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
```

### Run

```sh
$ python manage.py runserver
```

### Test

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

## Todo

1. forgot password
1. change/update password
1. logging
1. admin charts