from proj.handlers.main import bp_main


def init_app(app):
    app.register_blueprint(bp_main)
