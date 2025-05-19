from flask import Flask, request, jsonify, render_template
import mysql.connector
from llm import convert_natural_language_to_sql

app = Flask(__name__)

#  Update DB credentials (if needed)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'elementary',
    'database': 'student_db'
}

#  Database connection
def get_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query')
    
    try:
        #  Convert NL to SQL using LLaMA
        sql_query = convert_natural_language_to_sql(user_query)
        print(f"Generated SQL: {sql_query}")  #  Debug log

        #  Execute SQL query
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify({'status': 'success', 'data': result})
    
    except mysql.connector.Error as e:
        return jsonify({'status': 'error', 'message': f"MySQL Error: {str(e)}"})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    