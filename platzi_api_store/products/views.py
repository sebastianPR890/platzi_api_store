from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import json

def product_list(request):
    return render(request, 'product_list.html')

def product_detail(request, product_id):
    return render(request, 'product_detail.html', {'product_id': product_id})

def product_update(request, product_id):
    return render(request, 'product_update.html', {'product_id': product_id})

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

def get_product_detail(request, product_id):
    if request.method == "GET":
        try:
            url = f"https://api.escuelajs.co/api/v1/products/{product_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                product = response.json()
                data = {
                    'success': True,
                    'product': {
                        'id': product.get('id'),
                        'name': product.get('title'),
                        'price': product.get('price'),
                        'description': product.get('description'),
                        'image': product.get('images')[0] if product.get('images') else '',
                        'categoryId': product.get('category', {}).get('id')
                    }
                }
                return JsonResponse(data)
            elif response.status_code == 404:
                return JsonResponse({'success': False, 'error': 'Producto no encontrado.'}, status=404)
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error en la API: {response.status_code}. Detalles: {response.text[:200]}'
                }, status=response.status_code)
                
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la solicitud: {str(e)}'
            }, status=500)
            
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)


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
                return JsonResponse({'success': True, 'product': response.json()})
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error al crear el producto: {response.status_code}. Detalles: {response.text}'
                }, status=response.status_code)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la solicitud: {str(e)}'
            }, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

@csrf_exempt
def update_product(request, product_id):
    if request.method == "PUT":
        try:
            url = f"https://api.escuelajs.co/api/v1/products/{product_id}"
            data = json.loads(request.body)
            
            payload = {
                'title': data.get('title'),
                'price': int(data.get('price')),
                'description': data.get('description'),
                'categoryId': int(data.get('categoryId')),
                'images': [data.get('image')]
            }
            
            response = requests.put(url, json=payload)
            
            if response.status_code == 200:
                return JsonResponse({'success': True, 'product': response.json()})
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error al actualizar el producto: {response.status_code}. Detalles: {response.text}'
                }, status=response.status_code)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la solicitud: {str(e)}'
            }, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido. Se esperaba PUT.'}, status=405)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            url = f"https://api.escuelajs.co/api/v1/products/{product_id}"
            response = requests.delete(url, timeout=10)

            if response.status_code == 200 and response.json() is True:
                return JsonResponse({'success': True, 'message': 'Producto eliminado con éxito.'})
            else:
                error_detail = response.text
                try:
                    error_detail = response.json().get('message', response.text)
                except json.JSONDecodeError:
                    pass
                return JsonResponse({
                    'success': False,
                    'error': f'Error de la API al eliminar: {response.status_code}. Detalles: {error_detail}'
                }, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'error': f'Error de red: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido. Se esperaba DELETE.'}, status=405)