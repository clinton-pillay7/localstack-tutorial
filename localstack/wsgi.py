import boto3
from flask import Flask
from flask import request, render_template, request, redirect, send_file, url_for
import os
import botocore

#ENDPOINT_URL_ = 'http://192.168.8.108:4566'


app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('frontend.html')



@app.route('/upload', methods = ["POST"])
def upload_file():
	f = request.files["file"]
	f.save(f.filename)
	ENDPOINT_URL_ = 'http://localstack:4566'
	s3client = boto3.client("s3", region_name="us-east-1", endpoint_url = ENDPOINT_URL_,aws_access_key_id="test",aws_secret_access_key="test")
	file_filename = str(f.filename)
	s3client.upload_file(file_filename, "terrabucket", file_filename)
	return "uploaded" 


@app.route('/view')
def view():
        ENDPOINT_URL_ = 'http://localhost:4566'
        dclient = boto3.client("dynamodb", region_name="us-east-1", endpoint_url = ENDPOINT_URL_,aws_access_key_id="test",aws_secret_access_key="test")
        jresponsearray = dclient.scan(TableName="terratable")
        itemlist = jresponsearray["Items"]
        jsonlist = []
        for i in range(len(itemlist)):
                jsonlist_ = itemlist[i]["filename"]["S"]
                jsonlist.append(jsonlist_)
        return render_template("view.html", jsonlist=jsonlist)


if __name__ == "__main__":
	app.run(debug=True)

