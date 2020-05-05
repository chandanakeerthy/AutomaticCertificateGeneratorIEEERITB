from flask import Flask , redirect, render_template, url_for, request, flash, send_file
import cv2
import os
import tempfile
from werkzeug.utils import secure_filename

# to zip the directory
import shutil

app = Flask(__name__)
app.static_folder = 'static'
app.debug = False
app.secret_key = '#$&&*()282987653ngy$$^&*$hkhgf#(*&^098765'




@app.route('/', methods = ['GET','POST'])
@app.route('/certificate', methods = ['GET', 'POST'])
def certificatepage():
    return render_template('home.html')


@app.route('/perform', methods = ['GET','POST'])
def perform():
    temdir = tempfile.gettempdir()
    if request.method == 'POST':
        template_file = request.files['template']
        template_file_name = secure_filename(template_file.filename)
        template_file.save(os.path.join(temdir, template_file_name))

        font_size = request.form['fontsize']

        name_file = request.files['csv']
        name_file_name = secure_filename(name_file.filename)
        name_file.save(os.path.join(temdir, name_file_name))
        print(os.path.abspath(name_file_name))


        font = cv2.FONT_HERSHEY_COMPLEX
        fontScale = int(font_size)                 
        color = (171, 122, 9)               
        thickness = 5
        names = open(f'/tmp/{name_file_name}') # names uploaded 
        for name in names:                    
            text = name.upper()            
            img = cv2.imread(f'/tmp/{template_file_name}')

            cert_len = img.shape[1]
            cert_mid=cert_len//2
            txtsize = cv2.getTextSize(text, font,  fontScale, thickness)
            txt_len=txtsize[0][0]
            if(txt_len%2 == 0):
                mid=txt_len//2
            else:
                mid=(txt_len+1)//2

            org=(cert_mid-mid,450)
            img1 = cv2.putText(img, text, org, font,  fontScale, color, thickness, cv2.LINE_AA)
            path = r"/tmp/"        #path to save the certificates
            cv2.imwrite(os.path.join(path , text+".png"), img1 )
            # compressing to zip to upload
            shutil.make_archive('./static/certificates', 'zip', '/tmp')

        return render_template('home.html', c = 'certificates.zip') # returning cerificates in zip to download
    return render_template('home.html', certificates = '')


if __name__ == "__main__":
    app.run(debug=True)
    