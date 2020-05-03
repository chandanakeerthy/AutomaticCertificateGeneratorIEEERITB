from flask import Flask , redirect, render_template, url_for, request
import cv2
import os

app = Flask(__name__)
app.static_folder = 'static'
app.debug = True
app.secret_key = '#$&&*()282987653ngy$$^&*$hkhgf#(*&^098765'




@app.route('/', methods = ['GET','POST'])
@app.route('/certificate', methods = ['GET', 'POST'])
def certificatepage():
    return render_template('home.html')


@app.route('/perform', methods = ['GET','POST'])
def perform():
    if request.method == 'POST':
        template = request.files['template']
        template.save(f'./downloadFolder/{template.filename}')
        template_file = template.filename

        font_size = request.form['fontsize']

        name_file = request.files['csv']
        name_file.save(f'./downloadFolder/{name_file.filename}')
        name_file = name_file.filename

        font = cv2.FONT_HERSHEY_COMPLEX
        fontScale = int(font_size)                 
        color = (171, 122, 9)               
        thickness = 5
        names = open(f'./downloadFolder/{name_file}') # names uploaded 
        for name in names:                    
            text = name.upper()            
            img = cv2.imread(f'./downloadFolder/{template_file}')

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
            path = r"./certificates/"        #path to save the certificates
            cv2.imwrite(os.path.join(path , text+".jpg"), img1 )

    return render_template('home.html')


if __name__ == "__main__":
    app.run()
    