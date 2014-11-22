# project/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@main_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@main_blueprint.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
