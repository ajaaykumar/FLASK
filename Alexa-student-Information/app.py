import json
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    Student_id = str(request.form.get('student_id'))
    Student_Name = request.form.get('Name')
    fee = request.form.get('Fee Details')
    Marks = request.form.get('marks')
    Location = request.form.get('location')
    mobile = request.form.get('mobile')

    if request.method == 'POST':
        url = '/studentpost/postdetails'
        Item = ({
            "Student_Id": Student_id,
            "Student_name": Student_Name,
            "Location": Location,
            "Fee_Details": fee,
            "Marks": Marks,
            "Mobile Number": mobile

        })
        data = json.dumps(Item)
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=data, headers=headers)
        print(r)
        return render_template('Index.html', result1="Saved")
    return render_template('Index.html')


@app.route('/details', methods=['GET'])
def home():
    url = '/student/getdetails'
    val = requests.get(url)
    data = val.json()
    return render_template('Details.html', result=data)


@app.route('/attendance', methods=['POST', 'GET'])
def attendance():
    Studentid = str(request.form.get('stdid'))
    print("Studentid", Studentid)

    url = '/student/getdetails'
    val = requests.get(url)
    data = val.json()

    if request.method == 'POST':
        for x in data:
            print("x['Student_Id']", x['Student_Id'])
            if Studentid == x['Student_Id']:
                std = Studentid
                return render_template('AttendancePage.html', result=std)

    return render_template('Details.html', result=data)


name = ''
location1 = ''
Fee1 = ''
mobile = ''
marks = ''
@app.route('/attendanceadd', methods=['GET', 'POST'])
def attendanceadd():
    global name
    global location1
    global Fee1
    global mobile
    global marks
    id1 = request.form.get('id')
    att = request.form.get('attendance')
    date = request.form.get('date')

    urlget = '/student/getdetails'
    url = '/studentpost/postdetails'

    val = requests.get(urlget)
    data = val.json()
    for x in data:
        if id1 == x['Student_Id']:
            name = x['Student_name']
            location1 = x['Location']
            Fee1 = x['Fee_Details']
            marks = x['Marks']
            mobile = x['Mobile Number']

    if att != 'Absent':
        if request.method == 'POST':
            Item = ({
                "Student_Id": id1,
                "Attendance Status": att,
                "Date": date,
                "Student_name": name,
                "Location": location1,
                "Fee_Details": Fee1,
                "Mobile Number": mobile,
                "Marks": marks
                })
            data = json.dumps(Item)
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=data, headers=headers)
            print(r)
            return render_template('AttendancePage.html', result1=date)
        return render_template('AttendancePage.html', result1=date)
    else:
        api =  mobile + '&message=Your son, ' +name+' is absent&route=4'
        response = requests.get(api)
        return render_template('AttendancePage.html', message="Successfully Sent to {}".format(mobile))


if __name__ == '__main__':
    app.run(debug=True)

