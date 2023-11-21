from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_fuel_prices():
    try:
        # Open the website
        response = requests.get('https://m.fuelo.net/m/gasstation/122?lang=bg')
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract fuel types and prices
        fuel_prices = []

        # Find all rows in the table body
        rows = soup.select('.table tbody tr')

        for row in rows:
            # Find the second and third td elements (fuel type and price)
            td_elements = row.find_all('td')

            if len(td_elements) >= 3:
                fuel_type = td_elements[1].text.strip()
                price_text = td_elements[2].text.strip().replace('лв./л', '').replace(',', '.')
                price = float(price_text)
                fuel_prices.append((fuel_type, price))
        print(fuel_prices)
        return fuel_prices

    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/')
def index():
    fuel_prices = get_fuel_prices()
    return render_template('index.html', fuel_prices=fuel_prices)

@app.route('/', methods=['POST'])
def calculate_cost():
    try:
        kilometers = float(request.form['kilometers'])
        liters_per_km = float(request.form['litersPerKm'])
        fuel_price = float(request.form['fuelPrice'])
        num_people = float(request.form['numPeople'])

        total_cost = ((liters_per_km * kilometers) / 100) * fuel_price / num_people

        return jsonify({'total_cost': round(total_cost, 2)})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error calculating total cost'})

if __name__ == '__main__':
    app.run(debug=True)
