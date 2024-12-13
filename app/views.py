from flask import request, render_template, current_app

@current_app.route('/')
def main():
    return render_template('base.html')

@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404