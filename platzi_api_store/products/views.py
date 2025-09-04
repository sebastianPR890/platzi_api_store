from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import json

def product_list(request):
    return render(request, 'product_list.html')

def show_product(request):
    if request.method == "GET":
        try:
            url = "https://api.escuelajs.co/api/v1/products"
            response = requests.get(url)
            
            if response.status_code == 200:
                product_data = response.json()
                data = [
                    {
                        'success': True,
                        'product': {
                            'id': product['id'],
                            'name': product['title'],
                            'price': product['price'],
                            'description': product['description'],
                            'image': product['images'][0] if product['images'] else ''
                        }
                    }
                    for product in product_data # Limitar a los primeros 20 productos
                ]
                
                return JsonResponse({'success': True, 'products': data}, safe=False)
            
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error en la API: {response.status_code}. Detalles: {response.text[:200]}'
                })
                
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'La solicitud ha tardado demasiado tiempo en responder.'
            })
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'success': False,
                'error': 'Error de conexión. Por favor, verifica tu conexión a Internet.'
            })
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la solicitud: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido.'
    })

def add_product_page(request):
    return render(request, 'add_product.html')

@csrf_exempt

def add_product(request):
    if request.method == "POST":
        try:
            url = "https://api.escuelajs.co/api/v1/products"
            data = json.loads(request.body)
            
            payload = {
                'title': data.get('title'),
                'price': int(data.get('price')),
                'description': data.get('description'),
                'categoryId': int(data.get('categoryId')),
                'images': [data.get('image')]
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 201:
                return JsonResponse({'success': True, 'product': payload})
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error al crear el producto: {response.status_code}. Detalles: {response.text}'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la solicitud: {str(e)}'
            })
    return JsonResponse({'success': False, 'error': 'Error al procesar la solicitud.'}, status=405)