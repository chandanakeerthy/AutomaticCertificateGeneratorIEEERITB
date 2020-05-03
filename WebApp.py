from flask import Flask , redirect, render_template, url_for, request

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
        template = request.form['template']
        font_size = request.form['fontsize']
        csv_file = request.form['csv']
        

    return render_template('home.html', content = values)


if __name__ == "__main__":
    app.run()
    