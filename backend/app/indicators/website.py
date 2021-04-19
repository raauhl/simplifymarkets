from flask import Flask, render_template, request
import sys

app = Flask(__name__)

@app.route('/')
def student():
   return render_template('strategies.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        default_name = '0'
    
        stock = request.form.get('stock', default_name)
        timeframe  =request.form.get('timeframe', default_name)
        indicators1=request.form.get('indicators', default_name)
        comparator =request.form.get('comparator', default_name)
        indicators2=request.form.get('indicators2', default_name)
        print(stock, file=sys.stderr)
        #from backtraderv2 import getInput
        print("backtraderv2.py " + email + " " + email1)
        result = backtraderv2.py.getInput(stock, timeframe, indicators1, comparator, indicators2)
        
        return render_template("result.html",result = result)

'''
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)
'''
if __name__ == '__main__':
   app.run(debug = True)