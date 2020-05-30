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
    if os.path.exists('./static/certificates.zip'):
        os.remove('./static/certificates.zip')
    return render_template('home.html', con = 'none')


@app.route('/perform', methods = ['GET','POST'])
def perform():
    if request.method == 'POST':
        try:
            temdir = tempfile.gettempdir()
            template_file = request.files['template']
            template_file_name = secure_filename(template_file.filename)
            template_file.save(os.path.join(temdir, template_file_name))

            font_size = request.form['fontsize']

            name_file = request.files['csv']
            name_file_name = secure_filename(name_file.filename)
            name_file.save(os.path.join(temdir, name_file_name))
            
            # font color conversion to rgb format
            color_code_hex = request.form['fontcolor']
            value = color_code_hex.lstrip('#')
            lv = len(value)
            color_code_rgb = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

            # converion from rgb to bgr for cv2 processing
            color_code_bgr = color_code_rgb[::-1]

            font = cv2.FONT_HERSHEY_COMPLEX
            fontScale = int(font_size)                 
            color = color_code_bgr            
            thickness = 5

            # form namesList on file type of names file
            fileFormat = name_file_name.split('.')[-1] # get the .format
            if fileFormat == 'txt':
                names = open(f'/tmp/{name_file_name}') # names uploaded
                namesList = [name[:-1] for name in names]
            elif fileFormat == 'csv':
                import pandas as pd 
                df = pd.read_csv(name_file_name)
                namesList = df['Name'] # set the default value for name column in csv file
            else:
                raise Exception(f'Names file format not supported: {fileFormat}')

            for name in namesList:                    
                text = name. upper()            
                img = cv2.imread(f'/tmp/{template_file_name}')

                cert_len = img.shape[1]
                cert_mid = cert_len//2
                txtsize = cv2.getTextSize(text, font,  fontScale, thickness)
                txt_len = txtsize[0][0]
                if(txt_len%2 == 0):
                    mid=txt_len//2
                else:
                    mid=(txt_len//2)+1

                org=(cert_mid - mid,640)

                img1 = cv2.putText(img, text, org, font,  fontScale, color, thickness, cv2.LINE_AA)
                path = r"/tmp/"        #path to save the certificates
                cv2.imwrite(os.path.join(path , text+".png"), img1 )
                # compressing to zip to upload
                shutil.make_archive('./static/certificates', 'zip', '/tmp')
            return render_template('home.html', c = 'certificates.zip', con = 'block') # returning cerificates in zip to download
        except Exception as e:
            print(e)
    return render_template('home.html', certificates = '', con = 'none')


#############################################################################################
# Invalid urls routings handled
@app.errorhandler(404)
def page_not_found(error):
    # future developemt to render custom 404 error page
    return 'This Page Does Not Exists',404

#############################################################################################

if __name__ == "__main__":
    app.run(debug=True)
    