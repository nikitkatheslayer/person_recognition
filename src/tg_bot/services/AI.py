from detection.cv_detect.face import FaceDetector
from detection.cv_detect.person import PersonDetector
from detection.deep.find import DeepFind
from detection.deep.analysis import DeepFaceAnalysis

def recognize_face_photo(image_path):
    detect = FaceDetector()
    count_faces = detect.recognize_photo(image_path)
    return count_faces

def recognize_person_photo(image_path):
    count_person = PersonDetector.recognize_photo(image_path)
    return count_person

def recognize_face_video(video_path):
    detect = FaceDetector()
    time_detected = detect.recognize_video(video_path)
    return time_detected

def recognize_person_video(video_path):
    count_person = PersonDetector.recognize_video(video_path)
    return count_person

def analyze_face_photo(image_path):
    face_info = DeepFaceAnalysis.analysis_face(image_path)
    return face_info

def identify_face_photo(image_path):
    find_result = DeepFind.find_face(image_path)
    return find_result