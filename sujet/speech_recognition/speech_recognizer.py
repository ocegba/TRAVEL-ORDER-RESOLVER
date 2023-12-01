import speech_recognition as sr

class SpeechRecognizer:
   def __init__(self):
       self.recognizer = sr.Recognizer()

   def record_audio(self, filename='record.wav'):
       with sr.Microphone() as source:
           print("Réglage du bruit ambiant... Patientez...")
           self.recognizer.adjust_for_ambient_noise(source)
           print("Vous pouvez parler...")
           recorded_audio = self.recognizer.listen(source)
           print("Enregistrement terminé !")
           with open(filename, 'wb') as f:
               f.write(recorded_audio.get_wav_data())

   def recognize_audio(self, audio_file):
       try:
           with sr.AudioFile(audio_file) as source:
               # self.recognizer.adjust_for_ambient_noise(source)  # Ajustement du bruit ambiant - peut supprimer des parties si on parle trop doucement
               audio_data = self.recognizer.listen(source)  # Enregistrement audio
               print("Reconnaissance du texte...")
               text = self.recognizer.recognize_google(audio_data, language="fr-FR")
               with open("text_enregistrement.txt", "w") as text_record:
                   text_record.write(text)
        
               print("Vous avez dit : {}".format(text))
       except Exception as ex:
           print(ex)

if __name__ == "__main__":
   recognizer = SpeechRecognizer()
   recognizer.record_audio('record.wav')
   recognizer.recognize_audio('record.wav')