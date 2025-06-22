from deepface import DeepFace
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
PROJECT_ROOT = os.getenv('PROJECT_ROOT')

class DeepFind:
    @staticmethod
    def find_face(img_path):
        find_info = DeepFace.find(
            img_path = img_path,
            db_path = f"{PROJECT_ROOT}/storage/users",
            enforce_detection=False,
            silent=True,
        )

        best_match = None
        min_distance = float('inf')
        for df in find_info:
            if not df.empty:
                current_best = df.loc[df['distance'].idxmin()]
                if current_best['distance'] < min_distance:
                    min_distance = current_best['distance']
                    best_match = current_best

        if best_match is not None:
            image_path = best_match['identity']
            filename = Path(image_path).name

            return filename
        else:
            return None

# if __name__ == '__main__':
#     analyzer = DeepFind()
#     result = analyzer.find_face(f"{PROJECT_ROOT}/storage/image/face_id_1.jpg")
#     print(result)
