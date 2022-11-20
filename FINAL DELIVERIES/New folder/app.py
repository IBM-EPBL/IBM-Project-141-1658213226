from flask import Flask,redirect,url_for,render_template,request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID="CrPBkKCDOmp031DxUhvsBVccZMGtVxSi5b9jLdl1mA-c"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/d94940f9ab2f457b81380796fc475d45:4cee5363-1117-4f3d-bc8a-1be19de8fe7a:bucket:ibm-assisment3"
COS_BUCKET_LOCATION="jp-tok-standard"


# Create resource https://s3.ap.cloud-object-storage.appdomain.cloud
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app=Flask(__name__)



def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()

        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))


def delete_item(bucket_name, object_name):
    try:
        cos.delete_object(Bucket=bucket_name, Key=object_name)
        print("Item: {0} deleted!\n".format(object_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete object: {0}".format(e))



def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))

  
@app.route('/')
def index():
    bucket="ibm-assisment3"
    files = get_bucket_contents(bucket)
    return render_template('index.html', files = files,bucket=bucket)
@app.route('/')
def home():
   
    return render_template('home.html')

@app.route('/')
def jobsearch():
    return render_template('jobsearch.html')

@app.route('/')
def jobrecommandation():
    return render_template('jobrecommandtion.html')


@app.route('/deletefile', methods = ['GET', 'POST'])
def deletefile():
   if request.method == 'POST':
       bucket=request.form['bucket']
       name_file=request.form['filename']
       
       delete_item(bucket,name_file)
       return 'file deleted successfully'
    
   if request.method == 'GET':
       return render_template('delete.html')
        
	
@app.route('/sign', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
       fname=request.form['fname']
       lname_file=request.form['lname']
       email = request.files['email']
       phone=request.form['phone']
       password=request.form['pass']
       confirmpasswork=request.form['cd']
       multi_part_upload(fname,lname_file,email,phone,password,confirmpasswork)
       return 'file uploaded successfully <a href="/">GO to Home</a>'
       
    
   if request.method == 'GET':
       return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
       email = request.files['email']
       password=request.form['pass']
       multi_part_upload(email,password)
       return 'file uploaded successfully <a href="/">GO to Home</a>'

@app.route('/resume', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
       fullname=request.form['fullname']
       address=request.form['address']
       email = request.files['email']
       
       confirmpasswork=request.form['cd']
       multi_part_upload(fname,lname_file,email,phone,password,confirmpasswork)
       return 'file uploaded successfully <a href="/">GO to Home</a>'
       
    
   if request.method == 'GET':
       return render_template('signup.html')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)

        