import sqlite3
import hashlib
import os
from datetime import datetime

class UserDB:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            admin_hash = self.hash_password('admin123')
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password_hash, is_admin) 
                VALUES (?, ?, ?)
            ''', ('admin', admin_hash, True))
            
            conn.commit()
    
    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def add_user(self, username, password, is_admin=False):
        """Add a new user to the database"""
        password_hash = self.hash_password(password)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, is_admin)
                    VALUES (?, ?, ?)
                ''', (username, password_hash, is_admin))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, password_hash, is_admin FROM users 
                WHERE username = ?
            ''', (username,))
            result = cursor.fetchone()
            
            if result and self.verify_password(result[1], password):
                return {'username': result[0], 'is_admin': result[2]}
            return None
    
    def get_all_users(self):
        """Get all users (admin only)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, is_admin, created_at 
                FROM users ORDER BY created_at DESC
            ''')
            return cursor.fetchall()
    
    def update_user(self, user_id, username=None, password=None, is_admin=None):
        """Update user information"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if username:
                cursor.execute('''
                    UPDATE users SET username = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (username, user_id))
            
            if password:
                password_hash = self.hash_password(password)
                cursor.execute('''
                    UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (password_hash, user_id))
            
            if is_admin is not None:
                cursor.execute('''
                    UPDATE users SET is_admin = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (is_admin, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_user(self, user_id):
        """Delete a user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_user(self, user_id):
        """Get user by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, is_admin, created_at 
                FROM users WHERE id = ?
            ''', (user_id,))
            return cursor.fetchone()
