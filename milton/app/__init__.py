import os

from flask import Flask, session
from app.i18n import TRANSLATIONS

def create_app():
    app = Flask(__name__)
    # საჭიროა session-ისთვის (ენის არჩევანი); production-ზე SECRET_KEY env-ცვლადით
    app.secret_key = os.environ.get('SECRET_KEY', 'milton-studio-tbilisi-dev-key')

    from .main import main_bp
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_i18n():
        lang = session.get('lang', 'ka')
        return {
            't': TRANSLATIONS[lang],
            'lang': lang,
            'other_lang': 'en' if lang == 'ka' else 'ka',
        }

    return app
