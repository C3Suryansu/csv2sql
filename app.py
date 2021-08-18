from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import pandas as pd
config = pd.read_json('config.json', typ = 'series')


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods = ['GET', 'POST'])
def data():
    if request.method == 'POST':
        if request.files:
            data = request.files['csvfile']
            df = pd.read_csv(data)
            conn = mysql.connector.connect(host=config.host,
                               database=config.database,
                               user=config.user,
                               password=config.password)
            if conn.is_connected():
                cursor = conn.cursor()
                for i in range(len(df)):
                    row = df.iloc[i]
                    cursor.execute("INSERT INTO `content`(`name`, `videoLink`, `subdomain`, `createdAt`, `lastUpdatedOn`) VALUES (%s,%s,%s,%s,%s)", (row.name, row.videoLink, row.subdomain, row.createdAt, row.lastUpdatedOn))
                    print("row inserted at ", i)
                conn.commit()
                cursor.close()
                conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)

