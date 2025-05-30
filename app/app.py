from flask import Flask, jsonify, request, render_template_string
import os
import datetime
import json
import logging
from logging.handlers import RotatingFileHandler

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

# Setup logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask application startup')

# Sample data for demonstration
sample_users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "admin"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "user"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "role": "user"}
]

# HTML templates
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Docker App Updated from other system</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .api-list { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .endpoint { margin: 10px 0; padding: 10px; background: white; border-left: 4px solid #007bff; }
        .method { color: #007bff; font-weight: bold; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳  Flask Docker </h1>
        
        <div class="status">
            <strong>✅ Application Status:</strong> Running successfully in Docker!<br>
            <strong>🕐 Server Time:</strong> {{ current_time }}<br>
            <strong>🔄 Version:</strong> {{ version }}<br>
            <strong>🌍 Environment:</strong> {{ environment }}
        </div>

        <div class="api-list">
            <h3>📋 Available API Endpoints:</h3>
            
            <div class="endpoint">
                <span class="method">GET</span> <a href="/health">/health</a> - Health check endpoint
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <a href="/api/users">/api/users</a> - Get all users
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <a href="/api/users/1">/api/users/&lt;id&gt;</a> - Get user by ID
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> /api/users - Create new user (JSON required)
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <a href="/api/stats">/api/stats</a> - Application statistics
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <a href="/test">/test</a> - Test page with forms
            </div>
        </div>

        <div class="footer">
            <p>🚀 Auto-deployment enabled - Push to GitHub to update automatically!</p>
            <p>Built with Flask + Docker + Auto-deployment</p>
        </div>
    </div>
</body>
</html>
"""

TEST_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Page - Flask Docker App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { background: #007bff; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .result { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        a { color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Page</h1>
        
        <form id="userForm">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="role">Role:</label>
                <input type="text" id="role" name="role" value="user">
            </div>
            
            <button type="submit">Create User</button>
        </form>
        
        <div id="result" class="result" style="display: none;"></div>
        
        <p><a href="/">← Back to Home</a></p>
    </div>

    <script>
        document.getElementById('userForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const userData = {
                name: formData.get('name'),
                email: formData.get('email'),
                role: formData.get('role')
            };
            
            try {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('result');
                
                if (response.ok) {
                    resultDiv.innerHTML = `<strong>✅ Success!</strong><br>User created: ${JSON.stringify(result, null, 2)}`;
                    resultDiv.style.backgroundColor = '#d4edda';
                    resultDiv.style.color = '#155724';
                } else {
                    resultDiv.innerHTML = `<strong>❌ Error!</strong><br>${result.error || 'Unknown error'}`;
                    resultDiv.style.backgroundColor = '#f8d7da';
                    resultDiv.style.color = '#721c24';
                }
                
                resultDiv.style.display = 'block';
                this.reset();
            } catch (error) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<strong>❌ Network Error!</strong><br>${error.message}`;
                resultDiv.style.backgroundColor = '#f8d7da';
                resultDiv.style.color = '#721c24';
                resultDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    """Home page with application info and API documentation"""
    return render_template_string(HOME_TEMPLATE, 
                                current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                version="1.4.0",
                                environment=os.environ.get('FLASK_ENV', 'production'))

@app.route('/health')
def health():
    """Health check endpoint for Docker and load balancers"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.1.0",
        "environment": os.environ.get('FLASK_ENV', 'production'),
        "uptime": "running"
    })

@app.route('/test')
def test_page():
    """Test page with interactive forms"""
    return render_template_string(TEST_TEMPLATE)

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    app.logger.info('GET /api/users - Fetching all users')
    return jsonify({
        "users": sample_users,
        "total": len(sample_users),
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    app.logger.info(f'GET /api/users/{user_id} - Fetching user')
    user = next((u for u in sample_users if u['id'] == user_id), None)
    
    if user:
        return jsonify({
            "user": user,
            "timestamp": datetime.datetime.now().isoformat()
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new user
        new_user = {
            "id": max([u['id'] for u in sample_users]) + 1 if sample_users else 1,
            "name": data['name'],
            "email": data['email'],
            "role": data.get('role', 'user')
        }
        
        sample_users.append(new_user)
        app.logger.info(f'POST /api/users - Created user: {new_user["name"]}')
        
        return jsonify({
            "message": "User created successfully",
            "user": new_user,
            "timestamp": datetime.datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        app.logger.error(f'Error creating user: {str(e)}')
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    return jsonify({
        "total_users": len(sample_users),
        "server_time": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.environ.get('FLASK_ENV', 'production'),
        "endpoints": {
            "GET /": "Home page",
            "GET /health": "Health check",
            "GET /api/users": "List all users",
            "GET /api/users/<id>": "Get user by ID",
            "POST /api/users": "Create new user",
            "GET /api/stats": "Application statistics",
            "GET /test": "Test page"
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested resource was not found",
        "available_endpoints": [
            "GET /",
            "GET /health",
            "GET /api/users",
            "GET /api/users/<id>",
            "POST /api/users",
            "GET /api/stats",
            "GET /test"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f'Internal server error: {str(error)}')
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on the server"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.logger.info(f'Starting Flask application on port {port}')
    app.run(host='0.0.0.0', port=port, debug=debug)