from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
import io
import base64
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forecast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    future_data = db.Column(db.PickleType, nullable=False)

with app.app_context():
    db.create_all()

def ticker_history(comp, dt):
    ticker = yf.Ticker(comp)
    df = ticker.history(period=dt)
    return df

def scale_fit_transform(train, scaler):
    train = train.reshape(-1, 1)
    train = scaler.fit_transform(train)
    return train

def model_lstm(step, price, unit):
    lstm = Sequential()
    lstm.add(LSTM(units=64, activation='tanh', input_shape=(step, price)))
    lstm.add(Dense(units=unit))
    lstm.compile(optimizer='adam', loss='mse')
    return lstm

def set_forecast(df, back, forecast):
    X, y = [], []
    for i in range(back, len(df) - forecast + 1):
        X.append(df[i - back: i])
        y.append(df[i: i + forecast])
    X = np.array(X)
    y = np.array(y)
    return X, y

def forecast_lstm(df, model, scaler, back):
    X = df[- back:]
    X = X.reshape(1, back, 1)
    y = model.predict(X).reshape(-1, 1)
    y = scaler.inverse_transform(y)
    return X, y

def forecast_df(df, col, y, model, scaler, step, forecast):
    future = pd.DataFrame(columns=['Date', 'Predict'])
    future['Date'] = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast)
    future['Predict'] = y.flatten()
    return future

def is_forecast(stock, price):
    today = datetime.today().strftime('%Y-%m-%d')
    forecast = Forecast.query.filter_by(stock=stock, price=price, date=today).first()
    return forecast

def store_forecast(stock, price, future):
    today = datetime.today().strftime('%Y-%m-%d')
    forecast = Forecast(stock=stock, price=price, date=today, future_data=future)
    db.session.add(forecast)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None
    if request.method == 'POST':
        price = request.form['price']
        stock = request.form['stock']
        dt = '5y'
        step = 100
        forecast = 100
        scaler = MinMaxScaler(feature_range=(0, 1))

        forecast_data = is_forecast(stock, price)
        if forecast_data:
            future = forecast_data.future_data
        else:
            df = ticker_history(stock, dt)
            col = price
            col_data = df[col].values.reshape(-1, 1)
            col_data = scale_fit_transform(col_data, scaler)
            X, y = set_forecast(col_data, step, forecast)
            lstm_model = model_lstm(step, 1, forecast)
            lstm_model.fit(X, y, epochs=10, batch_size=32)
            _, y_pred = forecast_lstm(col_data, lstm_model, scaler, step)
            future = forecast_df(df, col, y_pred, lstm_model, scaler, step, forecast)
            store_forecast(stock, price, future)
        
        plt.figure(figsize=(10, 6))
        plt.plot(future['Date'], future['Predict'])
        plt.title(f'{stock} {price} Stock Price Forecast')
        plt.xlabel('Date')
        plt.ylabel('Price')
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
