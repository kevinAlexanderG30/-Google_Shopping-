import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .forms import SearchForm

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            google_shopping_url = f"https://www.google.com/search?tbm=shop&q={query}&hl=es&gl=es"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Accept-Language": "es-ES,es;q=0.9",
            }
            response = requests.get(google_shopping_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraer todos los enlaces de los resultados
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if "lacasadelelectrodomestico.com" in href:
                    links.append(href)
            
            # Debugging: Print captured links
            print("Captured Links:")
            for link in links:
                print(link)

            # Filtrar y procesar los enlaces
            filtered_links = []
            for link in links:
                if '/Articulo~' in link:
                    product_id = link.split('IDArticulo~')[1].split('~')[0]
                    filtered_links.append({'url': link, 'product_id': product_id})

            return render(request, 'results.html', {
                'google_shopping_url': google_shopping_url,
                'filtered_links': filtered_links,
            })
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})
