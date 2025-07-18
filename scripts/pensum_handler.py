import mysql.connector
import logging
from datetime import datetime


logging.basicConfig(
    filename="PensumHanlder.log",
    level=logging.INFO
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logging.getLogger().addHandler(console_handler)



class PensumHandler:
    def __init__(self):
        self.conn = mysql.connector.connect(
        host="localhost",
        user="oa",  
        password="",
        database="pensum_db"
        )

        self.cursor = self.conn.cursor()
    
    def show_tables(self):
        self.cursor.execute("SHOW TABLES;")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]
    
    def describe_table(self, table):
        self.cursor.execute(f"DESCRIBE {table};")
        description = self.cursor.fetchall()
        return [x[0] for x in description]
    
    def display_table(self, table):
        self.cursor.execute(f"SELECT * FROM {table};")
        result = self.cursor.fetchall()
        return result
    
    def get_avg(self):
        self.cursor.execute(f"SELECT AVG(score) FROM courses;")
        result = self.cursor.fetchall()
        logging.info(f" Average : {result[0]}")
        return result
    
    def add_month(self, code, month):      
        try:
            query = "UPDATE courses SET month = %s WHERE code = %s"
            self.cursor.execute(query, (month, code))  # pass values as tuple
            self.conn.commit()
            logging.info(f"{month} has been added into subject : {code}")

        except Exception as e:
            logging.error(f"Error : {e}")
    
    def get_code(self, course: str):
        try:
            query = "SELECT code FROM courses WHERE name LIKE %s"
            param = f"%{course}%"
            self.cursor.execute(query, (param,))
            result = self.cursor.fetchall()

            if result:
                logging.info(f"Results found for '{course}': {result}")
            else:
                logging.warning(f"No course found matching: {course}")

            return result

        except Exception as e:
            logging.error(f"Error in get_code: {e}")
            return None

    def mark_completed(self, code, month : str , score : int):      
        try:
            self.add_month(code , month)
            self.add_score(code, score)
            query = "UPDATE courses SET completed = 1 WHERE code = %s"
            self.cursor.execute(query, (code,))  # pass values as tuple
            self.conn.commit()
            logging.info(f"{code} has been completed!!")

        except Exception as e:
            logging.error(f"Error : {e}")

    def add_score(self, code, score):      
        try:
            query = "UPDATE courses SET score = %s WHERE code = %s"
            self.cursor.execute(query, (score, code))  # pass values as tuple
            self.conn.commit()
            logging.info(f"{score} has been added into subject : {code}")

        except Exception as e:
            logging.error(f"Error : {e}")

    def completed_summary(self):

        today = datetime.today()
        target_date_str = "2028-03-04"
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
        difference = target_date - today
        difference = difference.days
        years = difference // 365.25
        rem_dy = difference % 365.25
        months = rem_dy // 30.44
        rem_d = rem_dy % 30.44
        rem_d = round(rem_d)

        self.cursor.execute(
            """
            SELECT 
                COUNT(*) AS total,
                SUM(completed = 1) AS completed,
                SUM(completed = 0) AS missing,
                AVG(score) AS average
            FROM courses;
            """
        )
        result = self.cursor.fetchone()
        summary = {
            "total": int(result[0]),
            "completed": int(result[1]),
            "missing": int(result[2]),
            "avg" : float(result[3]),
            "remaining" : f"📅Uni Remaining days : {round(years)} Year(s), {round(months)} Month(s) & {rem_d} day(s)"
        }

        # Average
        self.cursor.execute("SELECT AVG(score) FROM courses;")
        avg_result = self.cursor.fetchone()
        average = float(avg_result[0]) if avg_result[0] is not None else 0.0

        # Log in a more human-readable way
        today = datetime.today()
        target_date_str = "2028-03-04"
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
        difference = target_date - today
        difference = difference.days
        years = difference // 365.25
        rem_dy = difference % 365.25
        months = rem_dy // 30.44
        rem_d = rem_dy % 30.44
        rem_d = round(rem_d) 
        logging.info(f"📘 Pensum Summary ({today}):\n"
                    f"──────────────────────────────\n"
                    f"🟢 Total Subjects: {summary['total']}\n"
                    f"✅ Completed: {summary['completed']}\n"
                    f"❌ Missing: {summary['missing']}\n"
                    f"📊 Average Score: {average:.2f}\n"
                    f"📅Uni Remaining days : {round(years)} Year(s), {round(months)} Month(s) & {rem_d} day(s)")
        
        return summary


    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Error closing connection: {e}")

if __name__ == "__main__":
    pass


    
    

    



    
