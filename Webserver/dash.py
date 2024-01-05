from flask import Flask, render_template
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Create a simple DataFrame for testing
    data = {'X': [1, 2, 3, 4, 5], 'Y': [10, 14, 18, 24, 30]}
    df = pd.DataFrame(data)

    # Create a Plotly figure using the DataFrame
    fig = px.line(df, x='X', y='Y', title='Simple Plotly Plot')

    # Convert the Plotly figure to JSON
    plot_json = fig.to_json()

    # Convert the DataFrame to HTML for rendering in the template
    table_html = df.to_html(classes='table table-striped', index=False)

    return render_template('index.html', plot_json=plot_json, table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
