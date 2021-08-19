# CS39AB - Cloud Computing - Summer 2021
# Instructor: Thyago Mota
# Description: Lab3
# Alejandro Rojas
# http://lab03-1301595104.us-west-1.elb.amazonaws.com/

from re import sub
from decimal import Decimal
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import os

EXCHANGE_RATE_URL = ' https://www.coindesk.com/price/ethereum'

if __name__ == "__main__":

    # delete the following lines once you are satisfied with the db connection and before creating the docker image
    os.environ['DB_HOST']     = 'lab03.c8yzzsnmodry.us-west-1.rds.amazonaws.com'
    os.environ['DB_NAME']     = 'ethereum'
    os.environ['DB_USER']     = 'ethereum'
    os.environ['DB_PASSWORD'] = '135791'    
    
    
    # attempt to connect to MySQL
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    cursor = db.cursor()

    # get quote and update db
    req = requests.get(EXCHANGE_RATE_URL)
    soup = BeautifulSoup(req.content, 'html.parser')
    el = soup.find('div',class_='price-large')
    #print(el.text)
    exch_rate = Decimal(sub(r'[^\d\-\.]', '',  el.text))
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    #print(time)
    sql = f"INSERT INTO quotes VALUES ('{today}', {exch_rate})"
    cursor.execute(sql)
    db.commit()
    db.close()

