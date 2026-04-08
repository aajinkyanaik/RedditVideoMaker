import gtts #google translate TTS
import os.path
import requests
import random
import base64
import pathlib
import pyttsx3 #TODO add functions for pyTTS
import itertools
import sys
import moviepy.editor

class TTS:
    def __init__(self, text:str) -> None:
        """Assumes text is ready to be voiced."""
        self.FileDir:str = os.path.dirname(__file__)
        self.text:str = text
        self.TiktokTTSLink:str = "https://tiktok-tts.weilnet.workers.dev/"
        self.TiktokGenerate:str = "api/generation"
        self.TiktokStatus:str = "api/status"
        self.TiktokTTSVoice = "Tiktok TTS hasnt been used yet!"
        self.PyTTSengine = pyttsx3.init()
    
    def GoogleTranslateTTS(self, File:str="gtts.mp3", Repeat:int=1):
        if not os.path.exists(f"{self.FileDir}\\GoogleTranslate\\"):
            print(f"Creating {self.FileDir}\\GoogleTranslate\\")
            os.mkdir(f"{self.FileDir}\\GoogleTranslate\\")
        gtts.gTTS(self.text).save(f"{self.FileDir}\\GoogleTranslate\\{File}")
        with open(str(pathlib.Path(f"{self.FileDir}\\GoogleTranslate\\{File}")), "rb") as f:
            Bytes = f.read()
        with open(str(pathlib.Path(f"{self.FileDir}\\GoogleTranslate\\{File}")), "wb") as f:
            Bytes = Bytes*Repeat
            f.write(Bytes)
        print(f"Done! File Located at: {self.FileDir}\\GoogleTranslate\\{File}")
        return pathlib.Path(f"{self.FileDir}/GoogleTranslate/{File}")

    def _TiktokTTS(self, Voice:str, Text:str): #internal function
        #!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        List300 = Text.split(".")
        for Index, x in enumerate(List300):
            if len(x) > 300:
                print("A chunk for tiktokTTS are too big. Trying to cut the chunk into smaller chunks... (if there is a error, try different submission)")
                temp = x.replace("?", ".").replace(";", ".").replace("(", ".").replace(")", ".").replace(",", ".").split(".")
                List300 = List300[0:Index]+temp+List300[Index+1:]
        for x in List300:
            if x == "" or x.replace("\n", " ").replace(" ", "") == "": #empty
                List300.remove(x)
        List300Length = len(List300)
        print(f"There are {List300Length} request(s)")
        Requests = []
        for Index, Text in enumerate(List300):
            Data = {"text": f"{Text}", "voice": Voice}
            Req = requests.post(self.TiktokTTSLink+self.TiktokGenerate, json=Data)
            OutputText = f"Tiktok Voice {Voice}: {"Done" if Req.status_code==200 else f"Error Code: {Req.status_code}"} ({Index+1} of {List300Length} - {(Index+1)/List300Length:.2%})\r"
            sys.stdout.write(OutputText)
            if Req.status_code != 200:
                with open(f"{self.FileDir}\\VoiceErrors.txt", "a") as f:
                    f.write(f"Error {Req.status_code} ({Req.json().get("error", "Error details unknown")}) ({Index+1} of {List300Length}) with:\n{Data["text"]}\n")
            Requests.append(Req)
        sys.stdout.write(" "*len(OutputText)+"                          \r")
        sys.stdout.flush()
        return Requests

    def TiktokTTS(self, Voice:str="en_uk_003", File:str="TiktokTTS.mp3", Repeat:int=1):
        """
        For a whole list of possible voices look at: https://github.com/Weilbyte/tiktok-tts/blob/main/index.html
        (Lines 42 to 123).\n
        Note: Not all voices will work.\n
        Credit to Weilbyte for the actual tiktok voices and RESTful API!\n
        en_us_006\n
        en_us_009\n
        en_us_010\n
        en_uk_003\n
        en_au_002\n
        en_us_007\n
        en_us_001
        """
        self.TiktokTTSVoice = Voice
        Requests = self._TiktokTTS(Voice, self.text)
        print("Status Codes of all the request(s) were 200." if all(map(lambda x: x.status_code==200, Requests)) else "Status Codes of all the requests WEREN'T 200. :(")
        Count = 0
        Errors = any(map(lambda x: x.status_code!=200 or x.json().get("error", None) != None, Requests))
        while Errors: #3 tries for it to work
            #Voice = random.choice([
            #"en_us_006",
            #"en_us_009",
            #"en_us_010",
            #"en_uk_003", # <- Personal Favorite
            #"en_au_002",
            #"en_us_007",
            #"en_us_001"
            #])
            print(f"Trying again... Using {Voice} as the voice. Attempt: {Count+1}")
            Requests = self._TiktokTTS(Voice, self.text)
            Errors = any(map(lambda x: x.status_code!=200 or x.json().get("error", None) != None, Requests))
            if all(map(lambda x: x.status_code==200, Requests)):
                break
            Count+=1
            if Count >= 3:
                print("Tiktok TTS resulted in a Error!", list(map(lambda x : x.json()["error"], Requests)))
                return ("error", list(map(lambda x : x.json()["error"], Requests))[0])
        if not os.path.exists(f"{self.FileDir}\\Tiktok\\"):
            print(f"Creating {self.FileDir}\\Tiktok\\")
            os.mkdir(f"{self.FileDir}\\Tiktok\\")
        with open(f"{self.FileDir}\\Tiktok\\{File}", "wb") as f:
            for x in map(lambda x: base64.b64decode(x.json()["data"]), Requests*Repeat):
                f.write(x)
        Path = pathlib.Path(f"{self.FileDir}/Tiktok/{File}")
        print(f"Done! File Located at: {Path}")
        return Path
    
    def CreateALLTiktokVoices(self):
        Voices = \
            [
            "en_us_006",
            "en_us_009",
            "en_us_010",
            "en_uk_003", # <- Personal Favorite
            "en_au_002",
            "en_us_007",
            "en_us_001"
            ]
        for x in Voices:
            Filename = f"{x}TikTokTTS.mp3"
            self.TiktokTTS(x, Filename)
        return pathlib.Path(f"{self.FileDir}/Tiktok/{input("All voices have been made!\nSelect a voice:\n")}TikTokTTS.mp3")

    def GetpyTTSVoices(self=""):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        return voices

    def PyTTS(self, File:str="PyTTS.wav", VoiceID=random.choice(GetpyTTSVoices()).id, Repeat:int=1, Rate=200):
        engine = self.PyTTSengine
        if not os.path.exists(f"{self.FileDir}\\PyTTS\\"):
            print(f"Creating {self.FileDir}\\PyTTS\\")
            os.mkdir(f"{self.FileDir}\\PyTTS\\")
        engine.setProperty('voice', VoiceID)
        engine.setProperty('rate', Rate)
        #engine.say(self.text)
        FilePath = str(pathlib.Path(f"{self.FileDir}/PyTTS/{File}"))
        engine.save_to_file(self.text, FilePath)
        engine.runAndWait()
        Clip = moviepy.editor.AudioFileClip(FilePath)
        moviepy.editor.concatenate_audioclips([Clip]*Repeat).write_audiofile("temp.wav")
        moviepy.editor.AudioFileClip("temp.wav").write_audiofile(FilePath)
        print(f"Done! File Located at: {self.FileDir}\\PyTTS\\{File}")
        return pathlib.Path(f"{self.FileDir}/PyTTS/{File}")

if __name__ == "__main__":
    tts = TTS("Hi there")
    Repeat = 20
    print(tts.TiktokTTS(Repeat=Repeat))
    print(tts.GoogleTranslateTTS(Repeat=Repeat))
    print(tts.PyTTS(Repeat=Repeat, Rate=150))
