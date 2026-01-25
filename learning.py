import os
import csv
import io
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask,request,jsonify,render_template_string,send_file
import base64

app=Flask(__name__)

ADMIN_DEFAULT=os.getenv("ADMIN_PASSWORD","iteme2026")

DATABASE_URL="postgresql://postgres:aime@localhost:5432/iteme_pay"

def get_db_connection():
    conn=psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute(
        '''
       CREATE TABLE learning(
       id SERIAL PRIMARY KEY,
       name TEXT NOT NULL,
       date DATE NOT NULL,
       amount DECIMAL(10,2) NOT NULL,
       receiver TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );
      '''
    )
    conn.commit()
    cur.close()
    conn.close()

try:
    init_db()
except Exception as error:
    print(f"Database init failed here is the error {error}")

@app.route('/api/submit',methods=['POST'])
def submit_data():
    data=request.json
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute(
            "INSERT INTO learning (name,date,amount,receiver) VALUES (%s,%s,%s,%s)"
            (data['name'],data['date'],data['amount'],data['receiver'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status":"success","message":"201 [ok] data sent successful "}),201
    except Exception as error:
        return jsonify({"status":"error","message":str(error)}),500
    
@app.route('/api/admin/date',methods=['GET'])
def get_data():
    pwd=request.args.get('pwd')
    if pwd:
        try:
            pwd=base64.b64decode(pwd).decode('utf-8')
        except:
            pass
    if not pwd or pwd != ADMIN_DEFAULT:
        return jsonify({"status":"error","message":"Unauthorized"}),401
    
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("SELECT * FROM learning")
        rows=cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as error:
        return jsonify({"status":"error","message":str(error)}),500
@app.route('/api/admin/download', methods=['GET'])
def download_csv():
    pwd=request.args.get('pwd')
    format_type=request.args.get('format','csv').lower()

    if pwd:
        try:
            pwd=base64.b64decode(pwd).decode('utf-8')
        except:
            pass
    if not pwd or pwd !=ADMIN_DEFAULT:
        return jsonify({"status":"error","message":"Unathorized"}),401
    
    try:
        conn=get_db_connection()
        cur=conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM learning")
        rows=cur.fetchall()
        cur.close()
        conn.close()

        if format_type=='csv':
            output=io.StringIO()
            if rows:
                fieldnames=list(rows[0].keys())
                writer=csv.