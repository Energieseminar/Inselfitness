from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def display_dataframe():
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 22],
            'City': ['New York', 'San Francisco', 'Los Angeles']}
    
    df = pd.DataFrame(data)
    
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
