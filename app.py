from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# DB CONFIG (FIX)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "skillrr_db"
}

# Global connection
db = mysql.connector.connect(**db_config)
cursor = db.cursor(dictionary=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/jobs')
def get_jobs():
    cursor.execute("""
    SELECT job_id,title,base_price,job_status
    FROM Job
    """)
    jobs = cursor.fetchall()
    return jsonify(jobs)


@app.route('/bids', methods=['POST'])
def place_bid():
    data = request.json
    try:
        query = """
        INSERT INTO Bid(job_id,freelancer_id,price)
        VALUES(%s,%s,%s)
        """
        cursor.execute(query, (data['job_id'], data['freelancer_id'], data['price']))
        db.commit()
        return jsonify({"message": "Bid placed successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400


@app.route('/contracts', methods=['POST'])
def create_contract():
    data = request.json
    try:
        query = """
        INSERT INTO Contract(job_id,freelancer_id,start_date,final_price)
        VALUES(%s,%s,%s,%s)
        """
        cursor.execute(query, (data['job_id'], data['freelancer_id'], data['start_date'], data['price']))
        db.commit()
        return jsonify({"message": "Contract created"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400


@app.route('/payment', methods=['POST'])
def make_payment():
    data = request.json
    try:
        query = """
        INSERT INTO Transaction(contract_id,amount,payment_type,payment_status)
        VALUES(%s,%s,%s,%s)
        """
        cursor.execute(query, (data['contract_id'], data['amount'], data['type'], data['status']))
        db.commit()
        return jsonify({"message": "Payment recorded"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400


@app.route('/review', methods=['POST'])
def submit_review():
    data = request.json
    try:
        query = """
        INSERT INTO Review(contract_id,reviewer_id,reviewee_id,rating,comment)
        VALUES(%s,%s,%s,%s,%s)
        """
        cursor.execute(query, (data['contract_id'], data['reviewer'], data['reviewee'], data['rating'], data['comment']))
        db.commit()
        return jsonify({"message": "Review submitted"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400


# =========================
# TRANSACTION APIs
# =========================

@app.route('/tx_read', methods=['POST'])
def tx_read():
    conn = mysql.connector.connect(**db_config)
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        cursor.execute("START TRANSACTION")
        cursor.execute("SELECT COUNT(*) FROM Job")
        result = cursor.fetchone()
        conn.commit()
        return {"message": f"Read success, total jobs = {result[0]}"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()


@app.route('/tx_update_safe', methods=['POST'])
def tx_update_safe():
    conn = mysql.connector.connect(**db_config)
    conn.autocommit = False
    cursor = conn.cursor()

    job_id = request.json['job_id']

    try:
        cursor.execute("START TRANSACTION")
        cursor.execute("UPDATE Job SET base_price = base_price + 1000 WHERE job_id=%s", (job_id,))
        conn.commit()
        return {"message": f"Safe update on job {job_id}"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()


@app.route('/tx_conflict', methods=['POST'])
def tx_conflict():
    conn = mysql.connector.connect(**db_config)
    conn.autocommit = False
    cursor = conn.cursor()

    job_id = request.json['job_id']
    delay = int(request.json['delay'])

    try:
        cursor.execute("START TRANSACTION")
        cursor.execute("SET innodb_lock_wait_timeout = 2")
        cursor.execute("UPDATE Job SET base_price = base_price + 500 WHERE job_id=%s", (job_id,))

        import time
        time.sleep(delay)

        conn.commit()
        return {"message": "Transaction committed"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()


@app.route('/tx_deadlock', methods=['POST'])
def tx_deadlock():
    conn = mysql.connector.connect(**db_config)
    conn.autocommit = False
    cursor = conn.cursor()

    job1 = request.json['job1']
    job2 = request.json['job2']
    delay = int(request.json['delay'])

    try:
        cursor.execute("START TRANSACTION")

        cursor.execute("SELECT * FROM Job WHERE job_id=%s FOR UPDATE", (job1,))
        cursor.fetchall()
        import time
        time.sleep(delay)

        cursor.execute("SELECT * FROM Job WHERE job_id=%s FOR UPDATE", (job2,))
        cursor.fetchall()
        conn.commit()
        return {"message": "Done"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()


@app.route('/tx_dirty', methods=['POST'])
def tx_dirty():
    conn = mysql.connector.connect(**db_config)
    conn.autocommit = False
    cursor = conn.cursor()

    job_id = request.json['job_id']

    try:
        cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        cursor.execute("START TRANSACTION")

        cursor.execute("SELECT base_price FROM Job WHERE job_id=%s", (job_id,))
        val = cursor.fetchone()

        conn.commit()
        return {"message": f"Read value: {val[0]}"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.route('/tx_dirty_write', methods=['POST'])
def tx_dirty_write():
    conn = mysql.connector.connect(**db_config)
    conn.autocommit = False
    cursor = conn.cursor()

    job_id = request.json['job_id']

    try:
        cursor.execute("START TRANSACTION")

        cursor.execute("UPDATE Job SET base_price = base_price + 999 WHERE job_id=%s", (job_id,))

        import time
        time.sleep(10) 

        conn.rollback() 

        return {"message": "Rolled back"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
