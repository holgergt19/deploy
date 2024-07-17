import os
import cv2
import dlib
from PIL import Image, ImageDraw
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .models import ImageUpload
import requests

# Ruta al predictor de puntos clave faciales de dlib
predictor_path = os.path.join('C:\\django\\deploy', 'shape_predictor_68_face_landmarks.dat')
#predictor_path = os.path.join(os.getcwd(), 'shape_predictor_68_face_landmarks.dat')


# Cargar los modelos dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def detect_face_and_smile(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Cannot load image from {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        
        # Obtener los landmarks de la boca (puntos 48 a 67)
        mouth_landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(48, 68)]
        
        return mouth_landmarks

    return None

def generate_mask(image_path, mouth_landmarks, output_mask_path):
    with Image.open(image_path).convert("RGBA") as img:
        mask = Image.new("RGBA", img.size)

        draw = ImageDraw.Draw(mask, "RGBA")

        if mouth_landmarks and isinstance(mouth_landmarks, list) and len(mouth_landmarks) == 20:
            # Extraer los límites de la región de la boca para definir el rectángulo
            x_coords = [point[0] for point in mouth_landmarks]
            y_coords = [point[1] for point in mouth_landmarks]
            
            x_min = min(x_coords)
            x_max = max(x_coords)
            y_min = min(y_coords)
            y_max = max(y_coords)

            # Ajustar los límites para asegurarnos de cubrir los dientes
            y_min = y_min - 5  # Subir un poco por encima de la boca
            y_max = y_max + 5  # Bajar un poco por debajo de la boca
            
            # Dibujar el rectángulo en blanco opaco
            draw.rectangle([x_min, y_min, x_max, y_max], outline=None, fill=(255, 255, 255, 255))

            # Crear una imagen combinada con la máscara aplicada sobre la imagen original
            combined = img.copy()
            draw_combined = ImageDraw.Draw(combined, "RGBA")
            draw_combined.rectangle([x_min, y_min, x_max, y_max], outline=None, fill=(0, 0, 0, 0))  # Hacer transparente la región segmentada

            combined.save(output_mask_path, format='PNG')
        else:
            raise ValueError("No se pudieron obtener landmarks válidos de la boca.")
    
    return output_mask_path

def resize_image(image_path, output_path, size=(1024, 1024)):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path, format='PNG')
    return output_path

def apply_braces_effect(image_path, mask_path):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/images/edits"

    with open(image_path, 'rb') as image_file, open(mask_path, 'rb') as mask_file:
        response = requests.post(
            url,
            headers={'Authorization': f'Bearer {api_key}'},
            files={'image': image_file, 'mask': mask_file},
            data={
                'prompt': 'Create what the result of an orthodontic treatment would be like, which is the application of braces, which are attachments that are placed on the teeth.',
                'size': '1024x1024',
                'n': 5,  # Solicitar 5 imágenes
                'model': 'dall-e-2'
            }
        )

    response_data = response.json()
    if 'data' in response_data:
        edited_image_urls = [item['url'] for item in response_data['data']]
        return edited_image_urls
    else:
        raise ValueError(f"Error en la respuesta de la API: {response_data.get('error', 'Respuesta desconocida')}")


@login_required
def upload_image(request):
    odontologo = request.user.odontologo
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.idOdontologo = odontologo
            image_instance.save()

            original_image_path = image_instance.image.path

            try:
                # Detectar landmarks de la boca y generar la máscara
                mouth_landmarks = detect_face_and_smile(original_image_path)
                if mouth_landmarks:
                    mask_path = original_image_path.replace('uploads', 'masks').replace('.jpeg', '_mask.png')
                    generate_mask(original_image_path, mouth_landmarks, mask_path)

                    # Redimensionar la imagen original y la máscara
                    resized_image_path = original_image_path.replace('uploads', 'resized').replace('.jpeg', '_resized.png')
                    resize_image(original_image_path, resized_image_path)
                    resized_mask_path = mask_path.replace('masks', 'resized_masks')
                    resize_image(mask_path, resized_mask_path)

                    image_instance.resized_image = resized_image_path
                    image_instance.mask = resized_mask_path
                    image_instance.save()

                    try:
                        # Aplicar el efecto de brackets utilizando la API de OpenAI
                        edited_image_urls = apply_braces_effect(resized_image_path, resized_mask_path)
                        image_instance.edited_images = edited_image_urls
                        image_instance.save()
                    except ValueError as e:
                        return render(request, 'facecam/upload.html', {
                            'form': form,
                            'error': str(e),
                            'image': image_instance,
                            'mask_url': image_instance.mask.url if image_instance.mask else None
                        })
                else:
                    return render(request, 'facecam/upload.html', {
                        'form': form,
                        'error': 'No se detectó la sonrisa en la imagen.',
                        'image': image_instance
                    })
            except FileNotFoundError as e:
                return render(request, 'facecam/upload.html', {
                    'form': form,
                    'error': str(e),
                    'image': image_instance
                })
            except Exception as e:
                return render(request, 'facecam/upload.html', {
                    'form': form,
                    'error': f"Error desconocido: {str(e)}",
                    'image': image_instance
                })

            # Renderizar la página con la imagen, máscara y URLs de las imágenes editadas
            return render(request, 'facecam/upload.html', {
                'form': form,
                'image': image_instance,
                'mask_url': image_instance.mask.url if image_instance.mask else None,
                'edited_image_urls': edited_image_urls  # Pasar la lista de URLs a la plantilla
            })
    else:
        form = ImageUploadForm()
    return render(request, 'facecam/upload.html', {'form': form})

# Cargar los modelos dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
        
def detect_face_and_smile(image_path):
    # Verificar el formato de la imagen usando PIL
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Convertir a RGB si no lo está
            img.save(image_path)  # Guardar de nuevo en el mismo lugar
    except Exception as e:
        raise ValueError(f"Error al leer la imagen con Pillow: {str(e)}")

    # Leer la imagen con OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Cannot load image from {image_path}")

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        
        # Obtener los landmarks de la boca (puntos 48 a 67)
        mouth_landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(48, 68)]
        
        return mouth_landmarks

    return None


def generate_mask(image_path, mouth_landmarks, output_mask_path):
    with Image.open(image_path).convert("RGBA") as img:
        mask = Image.new("RGBA", img.size)

        draw = ImageDraw.Draw(mask, "RGBA")

        if mouth_landmarks and isinstance(mouth_landmarks, list) and len(mouth_landmarks) == 20:
            # Extraer los límites de la región de la boca para definir el rectángulo
            x_coords = [point[0] for point in mouth_landmarks]
            y_coords = [point[1] for point in mouth_landmarks]
            
            x_min = min(x_coords)
            x_max = max(x_coords)
            y_min = min(y_coords)
            y_max = max(y_coords)

            # Ajustar los límites para asegurarnos de cubrir los dientes
            y_min = y_min - 5  # Subir un poco por encima de la boca
            y_max = y_max + 5  # Bajar un poco por debajo de la boca
            
            # Dibujar el rectángulo en blanco opaco
            draw.rectangle([x_min, y_min, x_max, y_max], outline=None, fill=(255, 255, 255, 255))

            # Crear una imagen combinada con la máscara aplicada sobre la imagen original
            combined = img.copy()
            draw_combined = ImageDraw.Draw(combined, "RGBA")
            draw_combined.rectangle([x_min, y_min, x_max, y_max], outline=None, fill=(0, 0, 0, 0))  # Hacer transparente la región segmentada

            combined.save(output_mask_path, format='PNG')
        else:
            raise ValueError("No se pudieron obtener landmarks válidos de la boca.")
    
    return output_mask_path

def resize_image(image_path, output_path, size=(1024, 1024)):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path, format='PNG')
    return output_path

def apply_braces_effect(image_path, mask_path):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/images/edits"

    with open(image_path, 'rb') as image_file, open(mask_path, 'rb') as mask_file:
        response = requests.post(
            url,
            headers={'Authorization': f'Bearer {api_key}'},
            files={'image': image_file, 'mask': mask_file},
            data={
                'prompt': 'Create what the result of an orthodontic treatment would be like, which is the application of braces, which are attachments that are placed on the teeth.',
                'size': '1024x1024',
                'n': 5,  # Solicitar 5 imágenes
                'model': 'dall-e-2'
            }
        )

    response_data = response.json()
    if 'data' in response_data:
        edited_image_urls = [item['url'] for item in response_data['data']]
        return edited_image_urls
    else:
        raise ValueError(f"Error en la respuesta de la API: {response_data.get('error', 'Respuesta desconocida')}")


@login_required
def upload_image(request):
    odontologo = request.user.odontologo
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.idOdontologo = odontologo
            image_instance.save()

            original_image_path = image_instance.image.path

            try:
                # Detectar landmarks de la boca y generar la máscara
                mouth_landmarks = detect_face_and_smile(original_image_path)
                if mouth_landmarks:
                    mask_path = original_image_path.replace('uploads', 'masks').replace('.jpeg', '_mask.png')
                    generate_mask(original_image_path, mouth_landmarks, mask_path)

                    # Redimensionar la imagen original y la máscara
                    resized_image_path = original_image_path.replace('uploads', 'resized').replace('.jpeg', '_resized.png')
                    resize_image(original_image_path, resized_image_path)
                    resized_mask_path = mask_path.replace('masks', 'resized_masks')
                    resize_image(mask_path, resized_mask_path)

                    image_instance.resized_image = resized_image_path
                    image_instance.mask = resized_mask_path
                    image_instance.save()

                    try:
                        # Aplicar el efecto de brackets utilizando la API de OpenAI
                        edited_image_urls = apply_braces_effect(resized_image_path, resized_mask_path)
                        image_instance.edited_images = edited_image_urls
                        image_instance.save()
                    except ValueError as e:
                        return render(request, 'facecam/upload.html', {
                            'form': form,
                            'error': str(e),
                            'image': image_instance,
                            'mask_url': image_instance.mask.url if image_instance.mask else None
                        })
                else:
                    return render(request, 'facecam/upload.html', {
                        'form': form,
                        'error': 'No se detectó la sonrisa en la imagen.',
                        'image': image_instance
                    })
            except FileNotFoundError as e:
                return render(request, 'facecam/upload.html', {
                    'form': form,
                    'error': str(e),
                    'image': image_instance
                })
            except Exception as e:
                return render(request, 'facecam/upload.html', {
                    'form': form,
                    'error': f"Error desconocido: {str(e)}",
                    'image': image_instance
                })

            # Renderizar la página con la imagen, máscara y URLs de las imágenes editadas
            return render(request, 'facecam/upload.html', {
                'form': form,
                'image': image_instance,
                'mask_url': image_instance.mask.url if image_instance.mask else None,
                'edited_image_urls': edited_image_urls  # Pasar la lista de URLs a la plantilla
            })
    else:
        form = ImageUploadForm()
    return render(request, 'facecam/upload.html', {'form': form})
