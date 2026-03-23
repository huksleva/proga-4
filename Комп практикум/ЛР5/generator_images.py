from PIL import Image, ImageDraw
import random
from io import BytesIO
from fastapi import FastAPI, Request, Response




def generate_random_image(width=400, height=300):
    # Случайный цвет фона (тёмный)
    bg_color = (random.randint(20, 50), random.randint(20, 50), random.randint(20, 50))
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Рисуем 5-10 случайных фигур
    for _ in range(random.randint(5, 10)):
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        shape = random.choice(['circle', 'rectangle', 'triangle', 'line'])

        x1 = random.randint(0, width - 50)
        y1 = random.randint(0, height - 50)
        x2 = x1 + random.randint(20, 100)
        y2 = y1 + random.randint(20, 100)

        if shape == 'circle':
            draw.ellipse([x1, y1, x2, y2], fill=color, outline=None)
        elif shape == 'rectangle':
            draw.rectangle([x1, y1, x2, y2], fill=color, outline=None)
        elif shape == 'triangle':
            points = [(x1, y2), ((x1 + x2) // 2, y1), (x2, y2)]
            draw.polygon(points, fill=color)
        elif shape == 'line':
            draw.line([x1, y1, x2, y2], fill=color, width=random.randint(2, 5))

    return img





# Генерация и сохранение
if __name__ == '__main__':
    img = generate_random_image()
    img.save('random_shape.png')
    print('✅ Изображение сохранено как random_shape.png')