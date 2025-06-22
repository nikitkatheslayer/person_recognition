from deepface import DeepFace
from translate import Translator

class DeepFaceAnalysis:

    @staticmethod
    def analysis_face(img_path):
        face_info = DeepFace.analyze(img_path = img_path,
        enforce_detection = False,
        actions = ['age', 'gender', 'race', 'emotion']
        )

        return DeepFaceAnalysis.translator(
            face_info[0]["age"],
            face_info[0]["dominant_gender"],
            face_info[0]["dominant_race"],
            face_info[0]["dominant_emotion"]
        )

    @staticmethod
    def translator(age, gender, race, emotion):
        list = [gender, race, emotion]
        list_result = []

        for item in list:
            translator = Translator(from_lang="English", to_lang="Russian")
            translation = translator.translate(item)
            list_result.append(translation)

        list_result.append(age)

        if list_result[1] == "белый":
            list_result[1] = "Европеоидная"
        elif list_result[1] == "чёрный":
            list_result[1] = "Негроидная"
        elif list_result[1] == "азиатский":
            list_result[1] = "Монголоидная"
        return list_result