import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Iltimos, tizimga kiring"
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Create uploads folder
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.config.get('UPLOAD_FOLDER', 'uploads'), 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config.get('UPLOAD_FOLDER', 'uploads'), 'submissions'), exist_ok=True)
    os.makedirs(os.path.join(app.config.get('UPLOAD_FOLDER', 'uploads'), 'lesson_files'), exist_ok=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Context processor for translations
    @app.context_processor
    def inject_translations():
        from flask import session
        from app.utils.translations import get_translation, TRANSLATIONS
        lang = session.get('language', 'uz')
        return {
            't': lambda key: get_translation(key, lang),
            'current_lang': lang,
            'languages': {
                'uz': {'code': 'uz', 'name': 'O\'zbek', 'flag': '🇺🇿'},
                'ru': {'code': 'ru', 'name': 'Русский', 'flag': '🇷🇺'},
                'en': {'code': 'en', 'name': 'English', 'flag': '🇺🇸'}
            }
        }
    
    from app.routes import main, auth, admin, dean, courses, api, accounting
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(dean.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(accounting.bp)
    
    # Error handler qo'shish
    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        import sys
        print(f"Internal Server Error: {error}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        from flask import render_template
        return render_template('error.html', error=str(error)), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('error.html', error="Sahifa topilmadi"), 404
    
    with app.app_context():
        db.create_all()
        try:
            from app.models import create_demo_data, GradeScale
            create_demo_data()
            GradeScale.init_default_grades()
        except Exception as e:
            # Xatolarni log qilish (production'da)
            import sys
            import traceback
            print(f"Warning: Error initializing demo data: {e}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            # Xatoga qaramay ilova ishga tushishi kerak
            pass
    
    return app
