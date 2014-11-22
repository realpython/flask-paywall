# Flask Paywall

Setup a paywall with Flask and Stripe to offer paid access to your premium content.

## Workflow

1. User registers an account
2. User obtains access to member page
3. User pays via Stripe
3. User obtains access to premium content

> The act of registering is seperate from paying, since we want to capture an email address in case there is a problem with paying or if the user decides not to pay at all. In those situations, we can reach out to the user.

## QuickStart

### Rename *config_sample.py* as *config.py*

### Set Environment Variables

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
```

### Update Settings in Production

1. `SECRET_KEY`
1. `SQLALCHEMY_DATABASE_URI`
1. `STRIPE_SECRET_KEY`
1. `STRIPE_PUBLISHABLE_KEY`

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

### Testing

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
1. error handlers
1. logging
1. admin charts
