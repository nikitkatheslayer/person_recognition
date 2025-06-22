from cvlib.object_detection import draw_bbox
import cvlib as cv
import cv2
import json
from dotenv import load_dotenv
from sort_tracker import Sort
import numpy as np
import os

load_dotenv()

class PersonDetector:

    @staticmethod
    def recognize_photo(image_path):
        try:
            image = cv2.imread(image_path)
            if image is None:
                return ValueError('Failed to read image: {}'.format(image_path))

            bbox, label, conf = cv.detect_common_objects(image)

            bbox_person = []
            label_person = []
            conf_person = []

            for b, l, c in zip(bbox, label, conf):
                if l == 'person':
                    bbox_person.append(b)
                    label_person.append(l)
                    conf_person.append(c)
            output_image = draw_bbox(image, bbox_person, label_person, conf_person, colors=[(0, 255, 0)])

            save_path = os.path.splitext(image_path)[0] + '_detected.jpg'
            cv2.imwrite(save_path, output_image)

            return len(bbox_person)

        except Exception as e:
            raise ValueError(f'Error while recognizing person: {e}')

    @staticmethod
    def recognize_video(video_path):
        try:
            video = cv2.VideoCapture(video_path)
            if not video.isOpened():
                return ValueError('Failed to open video: {}'.format(video_path))

            video_split_path, file_ext = os.path.splitext(video_path)
            save_path = f"{video_split_path}_detected{file_ext}"

            frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(video.get(cv2.CAP_PROP_FPS))
            fourcc = int(video.get(cv2.CAP_PROP_FOURCC))

            out = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))

            tracker = Sort()
            unique_ids = set()
            seen_ids = set()
            count_frame = 0
            result_time_detected = []

            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break
                count_frame += 1
                bbox, label, conf = cv.detect_common_objects(frame)
                person_detections = []
                for b, l, c in zip(bbox, label, conf):
                    if l == 'person' and c > 0.9:
                        x1, y1, x2, y2 = b
                        person_detections.append([x1, y1, x2, y2, c])
                if person_detections:
                    tracks = tracker.update(np.array(person_detections))
                    for d in tracks:
                        x1, y1, x2, y2, score, track_id = d
                        unique_ids.add(int(track_id))
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, f'ID: {int(track_id)}, CONF: {float(round(score, 2))}', (int(x1), int(y1) - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        if track_id not in seen_ids:
                            time_detection = round(count_frame / fps, 2)
                            result_time_detected.append({
                                "id": track_id,
                                "time_detected": time_detection,
                                "object_accuracy": score,
                            })
                            seen_ids.add(track_id)
                out.write(frame)
            video.release()
            out.release()

            video_dir = os.path.dirname(video_path)
            result_path = os.path.join(video_dir, "result.json")

            with open(result_path, "w") as file:
                json.dump(result_time_detected, file, indent=4, ensure_ascii=False)

            return len(unique_ids), frame_width, frame_height

        except Exception as e:
            raise ValueError(f'Error while recognizing person: {e}')