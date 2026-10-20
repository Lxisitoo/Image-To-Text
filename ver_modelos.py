import google.generativeai as genai

# Reemplaza con tu clave real que empieza con AIza
genai.configure(api_key="AQ.Ab8RN6IwGQThsA_uGlzjHPMlnw68cgRku8z7HayxWwSpLi0QfA") 

print("Modelos compatibles disponibles para tu clave:")
for modelo in genai.list_models():
    if 'generateContent' in modelo.supported_generation_methods:
        print(modelo.name)