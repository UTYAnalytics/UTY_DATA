import tempfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd
import psycopg2
import glob
from supabase import create_client, Client
from datetime import date
import re
import unicodedata
from selenium.common.exceptions import TimeoutException
import imaplib
import email
import re
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timezone
import productrequest
from pyvirtualdisplay import Display
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

SUPABASE_URL = "https://sxoqzllwkjfluhskqlfl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN4b3F6bGx3a2pmbHVoc2txbGZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIyODE1MTcsImV4cCI6MjAxNzg1NzUxN30.FInynnvuqN8JeonrHa9pTXuQXMp9tE4LO0g5gj0adYE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Replace these with your Keepa username and password
username = "utycorp@"
password = "H@h@!1234"

keepa_api_key_product = productrequest.KeepaAPI(
    "4ghd75c7ivb6tuoifdl793k6kvurslo049b40gkvtqbdkgttq3t34btb7och58rb"
)

# Gmail App Password
server = "imap.gmail.com"
email_address = "uty.tra@thebargainvillage.com"
email_password = "kwuh xdki tstu vyct"
subject_filter = "Keepa.com Account Security Alert and One-Time Login Code"

display = Display(visible=0, size=(800, 800))
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists

# Create a temporary directory for downloads
with tempfile.TemporaryDirectory() as download_dir:
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options = [
        # Define window size here
        "--window-size=1200,1200",
        "--ignore-certificate-errors"
        # "--headless",
        # "--disable-gpu",
        # "--window-size=1920,1200",
        # "--ignore-certificate-errors",
        # "--disable-extensions",
        # "--no-sandbox",
        # "--disable-dev-shm-usage",
        #'--remote-debugging-port=9222'
    ]
    chrome_options.add_experimental_option("prefs", prefs)
    for option in options:
        chrome_options.add_argument(option)


def get_otp_from_email(server, email_address, email_password, subject_filter):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_address, email_password)
    mail.select("inbox")

    status, data = mail.search(None, '(SUBJECT "{}")'.format(subject_filter))
    mail_ids = data[0].split()

    latest_email_id = mail_ids[-1]
    status, data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = data[0][1].decode("utf-8")
    email_message = email.message_from_bytes(data[0][1])

    otp_pattern = re.compile(r"\b\d{6}\b")

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if "text/plain" in content_type or "text/html" in content_type:
                email_content = part.get_payload(decode=True).decode()
                match = otp_pattern.search(email_content)
                if match:
                    return match.group(0)
    else:
        email_content = email_message.get_payload(decode=True).decode()
        match = otp_pattern.search(email_content)
        if match:
            return match.group(0)

    return None

data_result=[]
def best_seller_Data():

    # Login process
    try:
        # Initialize the Chrome driver with the options
        driver = webdriver.Chrome(options=chrome_options)

        # Open Keepa
        driver.get("https://keepa.com/#!")

        wait = WebDriverWait(driver, 20)
        # Login process
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="panelUserRegisterLogin"]'))
        )
        login_button.click()

        username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username_field.send_keys(username)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(10)
        try:
            otp = get_otp_from_email(server, email_address, email_password, subject_filter)
            otp_field = driver.find_element(By.ID, "otp")
            otp_field.send_keys(otp)
            otp_field.send_keys(Keys.RETURN)
            time.sleep(5)
        except NoSuchElementException:
            print("OTP field not found. Check the HTML or the timing.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    except:
        print(f"An unexpected error occurred: {e}")

    # Navigate to the top seller list
    try:
        data_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="topMenu"]/li[4]/a/span'))
        )
        data_button.click()
        time.sleep(5)

        top_seller_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="subPanel"]/ul[3]/li[4]/a'))
        )
        top_seller_button.click()
        time.sleep(5)

        showrow_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="grid-tools-topseller"]/div/span[1]/span/span')
            )
        )
        showrow_button.click()

        allrow_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tool-row-menu"]/ul/li[8]'))
        )
        allrow_button.click()
        time.sleep(30)
        # Download process
        download_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="grid-tools-topseller"]/div/span[2]/span')
            )
        )
        download_button.click()
        time.sleep(5)
        csv_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="formatRadio"]/div[2]/div'))
        )
        csv_button.click()
        time.sleep(5)
        final_download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="exportSubmit"]'))
        )
        final_download_button.click()
        time.sleep(8)
    except Exception as e:
        print("Error during navigation/download:", e)

    # Close the browser
    driver.quit()


    def get_newest_file(directory):
        files = glob.glob(os.path.join(directory, "*"))
        if not files:  # Check if the files list is empty
            return None
        newest_file = max(files, key=os.path.getmtime)
        return newest_file


    file_path = download_dir

    newest_file_path = get_newest_file(file_path)

    if newest_file_path:
        data = pd.read_csv(newest_file_path)
        # Proceed with the database insertion
    else:
        print("No files found in the specified directory.")


    # Database connection parameters
    db_host = "db.sxoqzllwkjfluhskqlfl.supabase.co"
    db_name = "postgres"
    db_user = "postgres"
    db_password = "5giE*5Y5Uexi3P2"


    # Add the new columns to the table
    # data = productrequest.add_columns_to_table(data, keepa_api_key_product)

    # Drop the first column
    data.drop(data.columns[0], axis=1, inplace=True)
    data["sys_run_date"] = str(date.today())

    # Connect to your database
    conn = psycopg2.connect(
        host=db_host, database=db_name, user=db_user, password=db_password
    )
    cursor = conn.cursor()

    # Create table if not exists (use the SQL command provided earlier)
    create_table_query = """CREATE TABLE IF NOT EXISTS best_seller_keepa (
        name TEXT,
        review_count_lifetime_percentage INT,
        review_count_30d_percentage INT,
        review_count_90d_percentage INT,
        review_count_365d_percentage INT,
        review_count_lifetime INT,
        review_count_30d INT,
        review_count_90d INT,
        review_count_365d INT,
        uses_fba BOOLEAN,
        verified_listings INT,
        primary_category TEXT,
        primary_brand TEXT,
        seller_id TEXT,
        country TEXT,
        sys_run_date DATE,
        totalStorefrontAsins INT,
        ratingCount INT
    );"""  # replace ... with your table structure
    cursor.execute(create_table_query)
    conn.commit()

    # Insert data into the table
    insert_query = """
    truncate table best_seller_keepa;
    """  # replace ... with your column names and %s placeholders
    # Set the timeout value (in seconds), for example, 300 seconds (5 minutes)
    timeout_seconds = 600
    cursor.execute(insert_query, timeout=timeout_seconds)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    headers = [
        "name",
        "review_count_lifetime_percentage",
        "review_count_30d_percentage",
        "review_count_90d_percentage",
        "review_count_365d_percentage",
        "review_count_lifetime",
        "review_count_30d",
        "review_count_90d",
        "review_count_365d",
        "uses_fba",
        "verified_listings",
        "primary_category",
        "primary_brand",
        "seller_id",
        "country",
        "sys_run_date",
    ]
    # Define the table name
    table_name = "best_seller_keepa"
    data.columns = headers
    # Insert data
    for index, row in data.iterrows():
        insert_data = row.to_dict()
        response = supabase.table(table_name).insert(insert_data).execute()
        if hasattr(response, "error") and response.error is not None:
            raise Exception(f"Error inserting row: {response.error}")
        print(f"Row inserted at index {index}")
    data_result.append(data)

with ThreadPoolExecutor() as executor:
        # Submit each row for processing
        futures = [executor.submit(best_seller_Data(), data_result)]
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
