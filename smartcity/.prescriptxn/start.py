from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
import pymysql
import requests
import json
import openai
from module import dbModule

app = Flask(__name__, static_folder='static', template_folder='templates')

API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

db_config = {
    'host': 'localhost',
    'user': 'SETUser',
    'password': 'Conestoga1',
    'database': 'prescriptxn'
}

# Connect to MySQL
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

#route
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        address = request.form.get('address')
        city = request.form.get('city')
        province = request.form.get('province')
        postal_code = request.form.get('postalCode')
        email = request.form.get('email')

        # Insert data into users table
        db = pymysql.connect(**db_config)
        cursor = db.cursor()
        sql = "INSERT INTO users (firstName, lastName, gender, birthday, address, city, province, postalCode, email) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (first_name, last_name, gender, birthday, address, city, province, postal_code, email)
        cursor.execute(sql, values)
        db.commit()

        # Close database connection
        cursor.close()
        db.close()
        return redirect(url_for('medlist', name=first_name)) + url_for('qrcode', firstName=first_name, lastName=last_name, email=email, birthday=birthday)
    else:
        return render_template("register.html")


@app.route('/qrcode')
def qrcode():
 
    db = pymysql.connect(**db_config)
    mycursor = db.cursor()

    mycursor.execute("SELECT * FROM users")
    
    results = mycursor.fetchall()
    userID = results[0][0]
    firstName = results[0][1]
    lastName = results[0][2]
    birthday = results[0][4]
    email = results[0][9]
    
    # Close database connection
    mycursor.close()
    db.close()

    if results:
        return render_template("qrcode.html", userID=userID, firstName=firstName, lastName=lastName,birthday=birthday , email=email)
    else:
        return render_template("home.html")



@app.route('/medlist')
def medlist():
    name = request.args.get('name')
    return render_template("medlist.html", name=name)


@app.route('/medadd', methods=['GET', 'POST'])
def medadd(): 
    if request.method == 'POST':
        medlist = json.loads(request.form.get('medicationList'))
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        for medication in medlist:
            api_url = f'https://api.fda.gov/drug/label.json?search=openfda.generic_name:"{medication}"&limit=1'
            response = requests.get(api_url)

            if response.status_code == 200:
                # Extract relevant information from the API response
                result = response.json()
                drug_name = result['results'][0]['openfda']['generic_name'][0]

                ai_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"provide effectiveness of {drug_name} in 2 sentences with easy words"},
                    ]
                )
                print(ai_response)
                print(f"Medication: {drug_name}")
            else:
                print("no response from fda api")

            sql = "insert into medications (medication_name) values (%s)"
            values = medication
            cursor.execute(sql, values)
            db.commit()    
        cursor.close()
        db.close()
    else:
        return render_template("medadd.html")

    name = request.args.get('name')
    return render_template("medadd.html", name=name)



@app.route('/medinfo', methods=['GET', 'POST'])
def medinfo():
    # connect
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    # get data
    cursor.execute("SELECT * FROM medications")
    medications = cursor.fetchall()

    print(medications)

    #close
    cursor.close()
    db.close()

    name = request.args.get('name')
    return render_template("medinfo.html", name=name)


@app.route('/portal')
def portal():
    name = request.args.get('name')
    return render_template("portal.html", name=name)

@app.route('/appointment')
def appointment():
    name = request.args.get('name')
    return render_template("appointment.html", name=name)

@app.route('/about')
def about():
    name = request.args.get('name')
    return render_template("about.html", name=name)


def main():
    app.run(host='127.0.0.1', debug=True, port=8000)

if __name__ == '__main__':
    main()