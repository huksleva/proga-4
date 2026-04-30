# 1. Импортируем необходимые библиотеки
import os

from PIL import Image
from huggingface_hub import InferenceClient

# 2. Создаём переменную для хранения токена доступа
HF_TOKEN = os.getenv("HF_TOKEN")  # Замените на ваш реальный токен с Hugging Face

# 3. Создаём экземпляр клиента, передавая ему токен
client = InferenceClient(token=HF_TOKEN)

# 4. Вызываем метод генерации изображения, указывая модель и промпт
prompt = "A majestic cyberpunk lion standing in a neon-lit rainy city, cinematic lighting, highly detailed, 4k resolution"
image = client.text_to_image(prompt=prompt, model="black-forest-labs/FLUX.1-schnell")

# 5. Сохраняем сгенерированное изображение в файл
image.save("generated_image.png")

# 6. Выводим сообщение об успешном сохранении
print("Изображение успешно сохранено как 'generated_image.png'")
