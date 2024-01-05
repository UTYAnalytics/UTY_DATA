import psycopg2
from datetime import datetime, timedelta
import pytz

def check_update_needed():
    # Replace these with your database connection details
    db_host = "db.sxoqzllwkjfluhskqlfl.supabase.co"
    db_name = "postgres"
    db_user = "postgres"
    db_password = "5giE*5Y5Uexi3P2"
  
     # Set the desired timezone (GMT+7 in this case)
    desired_timezone = pytz.timezone("Asia/Bangkok")
  
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Fetch the sys_run_date from the table (replace 'your_table_name' with your actual table name)
    cursor.execute("SELECT sys_run_date FROM best_seller_keepa ORDER BY sys_run_date DESC LIMIT 1;")
    last_run_date = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    if last_run_date:
        # Convert the retrieved date string to a datetime object in UTC
        last_run_datetime_utc = datetime.strptime(last_run_date[0], "%Y-%m-%d").replace(tzinfo=pytz.utc)

        # Convert to the desired timezone (GMT+7)
        last_run_datetime_gmt7 = last_run_datetime_utc.astimezone(desired_timezone)

        # Get today's date in the desired timezone
        today_gmt7 = datetime.now(desired_timezone).date()

        # Check if an update is needed (you can customize this logic based on your requirements)
        update_needed = today_gmt7 > last_run_datetime_gmt7
        return update_needed
    else:
        # If no date is found, consider an update is needed
        return True

# Print '0' if update is needed, '1' otherwise
print('0' if check_update_needed() else '1')
