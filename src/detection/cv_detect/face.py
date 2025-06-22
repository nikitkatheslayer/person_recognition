import os
import cv2
import cvlib as cv
import numpy as np
from sort_tracker import Sort
from dotenv import load_dotenv

load_dotenv()

class FaceDetector:
    def __init__(self):
        self.tracker = Sort(max_age=15, min_hits=3)

    @staticmethod
    def detect(frame):
        faces, confidences = cv.detect_face(frame)
        return faces, confidences

    @staticmethod
    def draw_rectangles(img, faces):
        for (startX, startY, endX, endY) in faces:
            cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)

    def face_tracker_update(self, faces, confidences):
        detections = np.empty((0, 5))
        if len(faces) > 0:
            for (box, conf) in zip(faces, confidences):
                x1, y1, x2, y2 = box
                detection = np.array([[x1, y1, x2, y2, conf]])
                detections = np.vstack([detections, detection])
        tracks = self.tracker.update(detections)

        return tracks

    def face_tracker(self, tracks, frame, faces, max_scores, seen_ids, count_frame, fps, result_time_detected):
        for track in tracks:
            x1, y1, x2, y2, score, track_id = track

            face = frame[int(y1):int(y2), int(x1):int(x2)]
            num_bright_pixels = np.sum(face >= 240)
            total_pixels = face.size
            if total_pixels == 0:
                continue
            ratio = num_bright_pixels / total_pixels
            if ratio < 0.5:
                if track_id not in max_scores or score > max_scores[track_id]["score"]:
                    max_scores[track_id] = {
                        "score": score,
                        "frame": frame.copy(),
                        "box": (x1, y1, x2, y2)
                    }
            if track_id not in seen_ids:
                time_detection = round(count_frame / fps, 2)
                result_time_detected.append({
                    "id": track_id,
                    "time_detected": time_detection,
                    "object_accuracy": score,
                })
                seen_ids.add(track_id)
            self.draw_rectangles(frame, faces)
            cv2.putText(frame, f'ID: {int(track_id)}, CONF: {float(round(score, 2))}', (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        return max_scores, result_time_detected


    def recognize_photo(self, image_path):
        try:
            img = cv2.imread(image_path)
            if img is None:
                return ValueError('Failed to read image: {}'.format(image_path))

            faces, confidences = self.detect(img)
            self.draw_rectangles(img, faces)

            image_path, file_ext = os.path.splitext(image_path)
            save_path = f"{image_path}_detected{file_ext}"
            cv2.imwrite(save_path, img)

            return len(faces)

        except Exception as e:
            raise ValueError(f'Error while recognizing face: {e}')

    def recognize_video(self, video_path):
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

            count_frame = 0
            max_scores = {}
            seen_ids = set()
            result_time_detected = []
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                count_frame = count_frame + 1
                faces, confidences = self.detect(frame)
                tracks = self.face_tracker_update(faces, confidences)
                max_scores, result_time_detected = self.face_tracker(tracks, frame, faces, max_scores,
                                                                     seen_ids, count_frame, fps, result_time_detected)
                out.write(frame)
            save_dir = video_split_path
            os.makedirs(save_dir, exist_ok=True)
            for track_id, data in max_scores.items():
                frame = data["frame"]
                if "box" in data:
                    x1, y1, x2, y2 = map(int, data["box"])
                    face_crop = frame[y1-50:y2+50, x1-50:x2+50]
                else:
                    face_crop = frame
                filename = f"face_id_{int(track_id)}.jpg"
                image_save_path = os.path.join(save_dir, filename)
                cv2.imwrite(image_save_path, face_crop)
            video.release()
            out.release()

            return result_time_detected, video_split_path, frame_width, frame_height

        except Exception as e:
            raise ValueError(f'Error while recognizing face: {e}')

# file = 'asd.mp4'
# save_path = f"{os.getenv('PROJECT_ROOT')}/storage/video/{file}"
# detector = FaceDetector()
# detection_info = detector.recognize_video(save_path)
#
# print(detection_info)