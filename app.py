"""
TravelGo Application Entrypoint
AWS Cloud Practitioner Project
"""

import os
from flask import Flask, render_template, session
from config import Config
from routes.auth import auth_bp
from routes.travel import travel_bp
from routes.booking import booking_bp
from routes.dashboard import dashboard_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Route Blueprints
    app.register_blueprint(travel_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(dashboard_bp)

    # Global context processor for templates
    @app.context_processor
    def inject_user():
        return {
            "current_user": session.get("user_name"),
            "current_email": session.get("user_email"),
            "is_authenticated": "user_email" in session
        }

    # Health check route for AWS EC2 / ALB target groups
    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "TravelGo", "version": "1.0.0"}, 200

    # Custom Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("base.html", custom_error="404 — Page Not Found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("base.html", custom_error="500 — Internal Server Error"), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))
