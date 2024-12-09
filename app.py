import os
import pandas as pd
import psycopg2
from dash import Dash, dcc, html, Input, Output

# Initialize Dash App
app = Dash(__name__)
server = app.server

# Connect to Heroku PostgreSQL
DATABASE_URL = os.getenv("postgres://u3hb629f9996i2:p8c8b6c0c49562570987c5f33c9dfb61383d69f1e391b3ee854018a7d2ed7419d@c3cj4hehegopde.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dbqo6icmfq1om2")

# Fetch Data from PostgreSQL
def fetch_crime_data():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        query = "SELECT * FROM crimes2 ORDER BY arrest_date DESC LIMIT 1000;"
        crime_data = pd.read_sql_query(query, conn)
        conn.close()
        return crime_data
    except Exception as e:
        print(f"Database Error: {e}")
        return pd.DataFrame()

# Initial Data Load
crime_data = fetch_crime_data()

# Define the App Layout
app.layout = html.Div([
    html.H1("NYC Crime Dashboard (PostgreSQL)"),

    # Filter Controls
    html.Label("Filter by Borough:"),
    dcc.Dropdown(
        id='borough-filter',
        options=[
            {'label': borough, 'value': borough}
            for borough in crime_data['borough'].unique()
        ],
        value=None,
        multi=True
    ),

    html.Label("Filter by Date Range:"),
    dcc.DatePickerRange(
        id='date-filter',
        start_date=crime_data['arrest_date'].min(),
        end_date=crime_data['arrest_date'].max(),
        display_format='YYYY-MM-DD'
    ),

    # Display the Map
    dcc.Graph(
        id='crime-map'
    )
])

# Callback for Updating the Map
@app.callback(
    Output('crime-map', 'figure'),
    [
        Input('borough-filter', 'value'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date')
    ]
)
def update_map(selected_boroughs, start_date, end_date):
    filtered_data = fetch_crime_data()

    if selected_boroughs:
        filtered_data = filtered_data[filtered_data['borough'].isin(selected_boroughs)]

    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data['arrest_date'] >= start_date) & 
            (filtered_data['arrest_date'] <= end_date)
        ]

    figure = {
        "data": [
            {
                "x": filtered_data["longitude"],
                "y": filtered_data["latitude"],
                "mode": "markers",
                "marker": {
                    "size": 10,
                    "color": "blue"
                },
                "text": filtered_data["crime_type"]
            }
        ],
        "layout": {
            "title": "Crime Map",
            "xaxis": {"title": "Longitude"},
            "yaxis": {"title": "Latitude"}
        }
    }
    return figure

# Run the App Locally
if __name__ == "__main__":
    app.run_server(debug=True)
