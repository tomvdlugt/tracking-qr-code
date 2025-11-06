import logging
import traceback
from flask import current_app, jsonify, request

def register_error_handlers(app):

  #400 handler
  @app.errorhandler(400)
  def bad_request(error):
    app.logger.warning(f"400 at {request.path}: {error}")
    return jsonify({
        "error": "Bad Request",
        "path": request.path
  }), 400

  #404 handler
  @app.errorhandler(404)
  def not_found(error):
    current_app.logger.info(f"404 at: {request.path}")
    return jsonify({"error": "not found", "path": request.path}), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    current_app.logger.info(f"405 at {request.path}: method not allowed")
    return jsonify({
        "error": "Method Not Allowed",
        "allowed_methods": list(error.valid_methods) if hasattr(error, "valid_methods") else None
    }), 405


  #500 handler
  @app.errorhandler(500)
  def internal_server_error(error):
    current_app.logger.exception("500 internal server error")
    return jsonify({"error": "internal server error"}), 500
