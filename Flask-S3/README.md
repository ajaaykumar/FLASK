# Flask-S3
## upload file using flask to amazon s3
To run this program, you'll need
- Python 3.6
- Flask (I used pip install flask to get the latest version)
- Boto (A Python interface to Amazon Web Services)
- An AWS account

### Some tips:
- Be sure to set S3 bucket permissions and IAM user permissions, or the upload will fail
- Don't forget to include enctype="multipart/form-data" in your HTML form tag.
- Don't forget to include the attribute multiple in your HTML input tag.
