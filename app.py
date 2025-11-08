from flask import Flask, render_template_string, request
import google.generativeai as genai
import base64
import random

# 🔑 Add your free Gemini API key from Google AI Studio
genai.configure(api_key="AIzaSyD0Mk2wL9pxo3X0EJz_c_pD9WN9iFSDpb0")

app = Flask(__name__)

FOOD_IMAGES = [
    "https://images.unsplash.com/photo-1604152135912-04a38a8a3a2c",
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
    "https://images.unsplash.com/photo-1551218808-94e220e084d2",
    "https://images.unsplash.com/photo-1523983300740-508e2f48d11a",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chef.AI 🍳</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: url('{{ bg_image }}') center/cover no-repeat fixed;
            backdrop-filter: blur(6px);
            color: #fff;
            text-align: center;
            padding: 40px;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.6);
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
        }
        form {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 15px;
            display: inline-block;
        }
        input, button {
            padding: 10px; margin: 10px;
            border: none; border-radius: 8px;
        }
        input[type=text] {
            width: 250px; color: #222;
        }
        button {
            background: linear-gradient(45deg, #ff512f, #f09819);
            color: white; font-weight: bold;
        }
        .recipe {
            margin-top: 40px;
            background: rgba(0,0,0,0.7);
            padding: 20px; border-radius: 15px;
            width: 70%; margin: auto;
        }
        img {
            width: 220px; border-radius: 12px; margin-top: 10px;
        }
        pre {
            text-align: left;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
<div class="overlay"></div>
<h1>Chef.AI 🍜</h1>
<p>Type a dish name or upload a photo — I’ll cook up the recipe!</p>

<form method="POST" enctype="multipart/form-data">
    <input type="text" name="dish_name" placeholder="Enter dish name (e.g. Sushi)" />
    <br>OR<br>
    <input type="file" name="dish_photo" accept="image/*" />
    <br>
    <button type="submit">Generate Recipe</button>
</form>

{% if recipe %}
<div class="recipe">
    <h2>🍽️ Recipe for {{ dish_name }}</h2>
    {% if image_data %}
        <img src="data:image/png;base64,{{ image_data }}">
    {% endif %}
    <pre>{{ recipe }}</pre>
</div>
{% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    recipe = None
    image_data = None
    dish_name = None
    bg_image = random.choice(FOOD_IMAGES)

    if request.method == 'POST':
        dish_name = request.form.get('dish_name')

        if 'dish_photo' in request.files and request.files['dish_photo'].filename:
            file = request.files['dish_photo']
            image_data = base64.b64encode(file.read()).decode('utf-8')

            model = genai.GenerativeModel("gemini-2.5-pro")


            prompt = "Generate a full recipe with ingredients and steps for this dish image."
            recipe = model.generate_content([prompt, {"mime_type": "image/png", "data": base64.b64decode(image_data)}]).text

        elif dish_name:
            model = genai.GenerativeModel("gemini-2.5-pro")

            prompt = f"Write a delicious recipe for {dish_name} including cuisine type, ingredients, and instructions."
            recipe = model.generate_content(prompt).text

    return render_template_string(HTML, recipe=recipe, dish_name=dish_name, image_data=image_data, bg_image=bg_image)

if __name__ == '__main__':
    app.run(port=5050, debug=True)
