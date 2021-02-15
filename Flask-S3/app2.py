from flask import Flask
from flask_wtf import Form
from flask_wtf.file import FileField
from sss3 import s3_upload
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import requests
import json
 
app = Flask(__name__)
app.secret_key = "super secret key"
app.config.from_object('config')

class UploadForm(Form):
    example = FileField('Example File')
 
# @app.route('/')
# def home():
#     session['logged_in'] = False 
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return "Ok"
 
# @app.route('/login', methods=['POST'])
# def do_admin_login():
#     if request.form['password'] == 'password' and request.form['username'] == 'admin':
#         session['logged_in'] = True
#         return render_template('home.html')
         
#     else:
#         flash('wrong password!')
#         return render_template('login.html')
   
# @app.route('/')
# def logout():
# # remove the username from the session if it is there
#     session.pop('username')
#     return redirect(url_for('login')) 

@app.route('/show')
def show(): 
    #if not session.get('logged_in'):
        #return render_template('login.html')

    r = requests.get('')
    d=r.text
    #print d
    decode = json.loads(d)
    print(decode)

    data_list = []
    for item in decode:
        data_details = {"nam":"", "id":""}
        data_details['nam'] = item['nam']
        data_details['id'] = item['id']
        data_list.append(data_details)
    de=data_list
    flash(de)
    return render_template('show.html')

'''@app.route('/upload')
def upload():
    if  session.get('logged_in'):
        return render_template('home.html')'''
@app.route('/', methods=['POST', 'GET'])
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        output = s3_upload(form.example)
        flash('{src} uploaded to S3 as {dst}'.format(src=form.example.data.filename, dst=output))
        return render_template('example.html', form=form)

        if request.method == 'POST':
            result = request.form
            #result1 = result.append('img',output)
            #print(result1)
            url = ''
            data1 = {'result':result,'photo':output}
            data = json.dumps(data1)
            print(data)
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=data, headers=headers)
            print(r.status_code)
          #return data
    return render_template('example.html', form=form)
if __name__ == "__main__":
    app.run(debug = True)
