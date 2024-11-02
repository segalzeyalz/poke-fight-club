from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g

# Initialize SQLAlchemy
db = SQLAlchemy()


def get_db():
    """Get or create database connection"""
    if 'db' not in g:
        g.db = db

    return g.db


def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)

    if db is not None:
        db.session.remove()


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)

    # Register close_db function to be called when app context ends
    app.teardown_appcontext(close_db)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()


def reset_db():
    """Reset database - useful for testing"""
    if not current_app.config['TESTING']:
        raise RuntimeError('This function can only be called in testing mode')

    db.drop_all()
    db.create_all()