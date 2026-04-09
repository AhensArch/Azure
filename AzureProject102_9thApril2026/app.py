import os
import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS allows your Frontend App Service to talk to your Backend App Service
CORS(app)

# Helper function to connect to Azure SQL
def get_db_connection():
    # 'AZURE_SQL_CONNECTIONSTRING' must match the name in your App Service Environment Variables
    conn_str = os.getenv('AZURE_SQL_CONNECTIONSTRING')
    return pyodbc.connect(conn_str)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TaskName, Status FROM Tasks")
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def add_task():
    try:
        new_task = request.json.get('task_name')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tasks (TaskName) VALUES (?)", (new_task,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Task added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()