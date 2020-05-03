from flask import Flask , redirect, render_template, url_for, request

app = Flask(__name__)
app.static_folder = 'static'
app.debug = True
app.secret_key = '#$&&*()282987653ngy$$^&*$hkhgf#(*&^098765'



@app.route('/', methods = ['GET','POST'])
@app.route('/certificate', methods = ['GET', 'POST'])
def certificatepage();
    return render_template('home.html')


if __name__ == "__main__":
    app.run()
    