from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '65a20c3bfab9b36b413a0ec718b51b0af63dd753702be106b597addf619e6c4a'

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    params = {
        "q": query,
        "hl": "en",
        "gl": "es",
        "tbm": "shop",
        "tbs": "p_ord:rv",
        "num": 10,
        "location": "Madrid, Spain",
        "api_key": API_KEY
    }
    response = requests.get('https://serpapi.com/search.json', params=params)
    results = response.json().get('shopping_results', [])

    filtered_results = []
    alternative_results = []

    for result in results:
        result_data = {
            'title': result['title'],
            'link': result['link'].split('?')[0],
            'thumbnail': result.get('thumbnail'),
        }

        if result.get('source') == 'La Casa del Electrodoméstico':
            product_id = result['link'].split('IDArticulo~')[-1].split('~')[0]
            result_data['product_id'] = product_id
            filtered_results.append(result_data)
        else:
            result_data['source'] = result['source']
            alternative_results.append(result_data)
    
    found_in_casa = bool(filtered_results)
    if not found_in_casa and len(alternative_results) > 0:
        filtered_results = alternative_results[:5]

    return render_template('results.html', results=filtered_results, found_in_casa=found_in_casa)

if __name__ == '__main__':
    app.run(debug=True)
