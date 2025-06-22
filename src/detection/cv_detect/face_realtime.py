import asyncio
import cv2
import cvlib as cv
from typing import Optional, Tuple, Union

from sqlalchemy.dialects.postgresql import array

from detection.deep.find import DeepFind
from db.orm import AsyncORM
import os
from dotenv import load_dotenv

load_dotenv()


async def process_ident(frame) -> Tuple[str, Optional[str]]:
    """
    Обрабатывает кадр и возвращает (идентификатор, путь к фото пользователя).
    """
    try:
        ident_result = DeepFind.find_face(frame)
        if not ident_result:
            return "Unknown", None

        user_info = await AsyncORM.get_user_photo(ident_result)
        if user_info:
            photo_path = f"{os.getenv('PROJECT_ROOT')}/storage/users/{user_info[0].photo}"
            return user_info[0].service_number, photo_path  # <--- photo = путь к файлу
    except Exception as e:
        print(f"[Ошибка] Определение личности: {e}")

    return "Unknown", None


def draw_faces(frame, faces, confidences, ident: str):
    """
    Рисует прямоугольники вокруг лиц и отображает ID в правом верхнем углу.
    """
    for idx, (startX, startY, endX, endY) in enumerate(faces):
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
        text = f"{confidences[idx] * 100:.2f}%"
        y_position = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.putText(frame, text, (startX, y_position), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)

    frame_height, frame_width = frame.shape[:2]
    corner_text = f"ID: {ident}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2
    (text_width, text_height), _ = cv2.getTextSize(corner_text, font, font_scale, thickness)
    x = frame_width - text_width - 10
    y = text_height + 10
    cv2.putText(frame, corner_text, (x, y), font, font_scale, (0, 255, 255), thickness)


async def run_face_recognition(poll_interval: int = 30):
    """
    Основной цикл распознавания лиц с отображением изображения пользователя справа.
    """
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("[Ошибка] Камера не доступна.")
        return

    cv2.namedWindow("Real-time Face Detection", cv2.WINDOW_NORMAL)

    frame_count = 0
    last_ident = 'Unknown'
    last_photo_path = None

    try:
        while True:
            status, frame = webcam.read()
            if not status:
                print("[Ошибка] Не удалось прочитать кадр.")
                break

            faces, confidences = cv.detect_face(frame)
            if frame_count % poll_interval == 0:
                if faces:
                    last_ident, last_photo_path = await process_ident(frame)
                else:
                    last_ident, last_photo_path = 'Unknown', None
            frame_count += 1
            draw_faces(frame, faces, confidences, last_ident)
            # Загружаем изображение пользователя, если путь валиден
            if last_photo_path and os.path.isfile(last_photo_path):
                user_img = cv2.imread(last_photo_path)

                if user_img is not None:
                    # Подгонка размера
                    frame_height = frame.shape[0]
                    scale = frame_height / user_img.shape[0]
                    new_width = int(user_img.shape[1] * scale)
                    user_img = cv2.resize(user_img, (new_width, frame_height))

                    # Объединение
                    combined = cv2.hconcat([frame, user_img])
                else:
                    combined = frame
            else:
                combined = frame

            cv2.imshow("Real-time Face Detection", combined)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        webcam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(run_face_recognition())
