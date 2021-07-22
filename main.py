from flask import Flask
from flask import *

from firebase import *
from linkUpdater import *






app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getPlayLists')
def getpls():
    pass



@app.route('/mp3LinkUpdater')
def mp3LinkUpdater():
    fun()
    return("bello")

    


app.run(debug = True)
