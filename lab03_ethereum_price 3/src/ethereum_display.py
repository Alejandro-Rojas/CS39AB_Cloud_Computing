# CS39AB - Cloud Computing - Summer 2021
# Instructor: Thyago Mota
# Description: Lab3
# Alejandro Rojas
# http://lab03-1301595104.us-west-1.elb.amazonaws.com/

from string import Template
import mysql.connector
import os


HTML_TEMPLATE = \
'''
    <!DOCTYPE html>
        <html>
            <head>
                <title>Ethereum</title>
                <style>
                    body {
                        font:18px/1.4 Verdana,Arial; 
                        background: #fff; 
                        height:100%; 
                        margin:25px 0; 
                        padding:0;
                        text-align: center
                    }
                    p {
                        margin-top:0
                    }
                    table { 
                        border: 1px solid black; 
                        margin: 0 auto; 
                        border-collapse: separate;
                        box-sizing: border-box;
                        table-layout: fixed;
                        width: 900px;
                    }
                    th, td { 
                        border: 1px solid black;
                        text-align: center; 
                    }
                    thead { 
                        background: #008CBA; 
                        color: #fff; 
                    }
                    tbody { 
                        background: #fff; 
                        color: #000; 
                    }
                </style>
            </head> 
                <body>
                <table class="table table-striped table-bordered table-sm">  
                    <thead class="thead-dark">  
                        <tr>  
                            <th>Date</th>  
                            <th>Time</th>  
                            <th>Price</th>  
                        </tr>  
                    </thead>  
                    <tbody class="tbody-light">
                    
'''
def lambda_handler(event, context):
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    cursor = db.cursor()
    sql = "SELECT `datetime`, quote FROM quotes ORDER BY `datetime` DESC"
    cursor = db.cursor(buffered = True)
    cursor.execute(sql) 
    html = HTML_TEMPLATE
    for date_time, quote in cursor:
        date = date_time.date()
        time = date_time.time()
        html += f"<tr><td>{date}</td><td>{time}</td><td>{quote}</td></tr>"
        #html = Template(HTML_TEMPLATE).safe_substitute(date=date,time=time,qutoe=quote)
        #html = Template(HTML_TEMPLATE).safe_substitute("<tr><td>{date[date=date]}'<tr><td>time=time<tr><td>quote=quote")
    html += "</table></html/>"
    return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': html
        }
