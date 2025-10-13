from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import database
import functools

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production!
db = database.UserDB()

# Decorators
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or not session.get('is_admin'):
            return redirect(url_for('access_denied'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return redirect(url_for('user_login'))

# User Login Interface
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.verify_user(username, password)
        if user:
            session['user'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Login successful!', 'success')
            
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return f"Welcome {user['username']}! Regular user dashboard would go here."
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('user_login.html')

# Admin Login Interface
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.verify_user(username, password)
        if user and user['is_admin']:
            session['user'] = user['username']
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    users = db.get_all_users()
    return render_template('admin_dashboard.html', users=users)

# User Management
@app.route('/admin/users/add', methods=['POST'])
@admin_required
def add_user():
    username = request.form['username']
    password = request.form['password']
    is_admin = 'is_admin' in request.form
    
    if db.add_user(username, password, is_admin):
        flash('User added successfully!', 'success')
    else:
        flash('Username already exists!', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/edit/<int:user_id>', methods=['POST'])
@admin_required
def edit_user(user_id):
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = 'is_admin' in request.form
    
    if db.update_user(user_id, username, password, is_admin):
        flash('User updated successfully!', 'success')
    else:
        flash('Error updating user', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/delete/<int:user_id>')
@admin_required
def delete_user(user_id):
    if db.delete_user(user_id):
        flash('User deleted successfully!', 'success')
    else:
        flash('Error deleting user', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/get/<int:user_id>')
@admin_required
def get_user(user_id):
    user = db.get_user(user_id)
    if user:
        return jsonify({
            'id': user[0],
            'username': user[1],
            'is_admin': bool(user[2])
        })
    return jsonify({'error': 'User not found'}), 404

# Access Denied
@app.route('/access-denied')
def access_denied():
    return render_template('access_denied.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('user_login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)