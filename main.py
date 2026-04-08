print("Importing libraries and files")
#external modules:
import praw.models
import moviepy.editor
import moviepy.video.fx.all as vfx
import PIL.Image
import faster_whisper
#bulitin:
import random
import os
import os.path, pathlib
import subprocess
import string
import time
#files:
import Reddit
import Voices
import Background
import TextParser
print("Done!\n\n")

class VideoMaker:
    def __init__(self, Subreddit="", Multi=False, TitleOnly=False) -> None:
        self.reddit = Reddit.Reddit()
        self.UseMultipleSubreddits:bool = Multi
        self.TitleOnly = TitleOnly
        self.UsedURL = False #True when self.GetSubmissionURL is used
        self.Subreddit: str | praw.models.Subreddit = self.SubredditGetterHelper(Subreddit)
        self.OGText:str = ""
        self.Text:str = ""
        self.VoiceText:str = ""
        self.Replace:iter = ("’", "aita", "AITA") #used in self.Reroll ONLY
        self.ReplaceWith:iter = ("'", "am I the asshole", "Am I The Asshole") #used in self.Reroll ONLY
        self.TiktokPath:str | pathlib.Path = ""
        self.gTTSPath:str | pathlib.Path = ""
        self.PyPath:str | pathlib.Path = ""
    
    def SubredditGetterHelper(self, Subreddit=""):
        if Subreddit and Subreddit != "random":
            return Subreddit
        return self.reddit.getRandomSubreddit(UseMulti=self.UseMultipleSubreddits)

    """
    (For reference)
    self.Submission = Submission
    self.SubmissionTitle = Submission.title
    self.SubmissionScore = Submission.score
    self.SubmissionCommentAmount = Submission.num_comments
    self.SubmissionAuthorName = Submission.author.name 
    self.SubmissionCommentsForest = Submission.comments
    self.SubmissionNSFW = Submission.over_18
    self.SubmissionBody = Submission.selftext
    self.SubmissionBodyOnly = Submission.is_self
    self.SubmissionLink = Submission.url
    self.SubmissionModPost = Submission.stickied
    """ 

    def GetSubmission(self, Subreddit="", Sortby="h", limit=20, ScoreGreaterThan=0):
        if not Subreddit: #if subreddit param is a empty str 
            Subreddit = self.Subreddit
        self.reddit.getSubmissionSubreddit(self.SubredditGetterHelper(Subreddit), Sortby=Sortby, limit=limit)
        self.reddit.SubmissionScore 
        if not self.TitleOnly: #Submission body matters
            SubmissionBool = not bool(self.reddit.SubmissionBodyOnly) #is True if no submission body
        elif self.TitleOnly: #submission body doesn't matter, title matters
            SubmissionBool = not bool(self.reddit.SubmissionTitle) #is True if not a title
        while self.reddit.SubmissionModPost or SubmissionBool: #mod post or no submission
            print("The post is not a submission only post.\n" if not self.reddit.SubmissionBodyOnly else "The post is stickied. (Probably a mod post!)\n" if self.reddit.SubmissionModPost else "\r", end="")
            print(f"The post is: {self.reddit.Submission.shortlink} (or https://www.reddit.com{self.reddit.Submission.permalink})")
            print("Getting a submission again")
            self.reddit.getSubmissionSubreddit(self.SubredditGetterHelper(Subreddit), Sortby=Sortby, limit=limit)
        print(f"The post is: {self.reddit.Submission.shortlink} (or https://www.reddit.com{self.reddit.Submission.permalink})")
        self.Reroll(Sortby=Sortby, limit=limit)

    def GetSubmissionURL(self, URL):
        self.reddit.getSubmissionURL(URL)
        self.UsedURL = True
        self.Subreddit = self.reddit.Submission.subreddit #The subreddit parameter in __init__ is overridden
        print(f"The post is: {self.reddit.Submission.shortlink} (or https://www.reddit.com{self.reddit.Submission.permalink})")
        self.OGText = f"{self.reddit.SubmissionTitle}\n\n\n{self.reddit.SubmissionBody}" #OG stands for original
        if self.TitleOnly:
            self.OGText = f"{self.reddit.SubmissionTitle}" #i just like f-strings lol
        self.Text = self.OGText
        for x, y in zip(self.Replace, self.ReplaceWith):
            self.Text = self.Text.replace(x, y)
        return False #return is used in self.Voice - acts same as self.Reroll
    
    def Reroll(self, Subreddit="", Sortby="h", limit=20):
        Reroll = input("R for reroll, else press enter\n")
        Rerolled = False
        while "r" in Reroll.lower():
            Rerolled = True
            self.GetSubmission(Subreddit=Subreddit, Sortby=Sortby, limit=limit)
            Reroll = input("R for reroll, else press enter\n")
            if "r" in Reroll.lower():
                break
        self.OGText = f"{self.reddit.SubmissionTitle}\n\n\n{self.reddit.SubmissionBody}" #OG stands for original
        self.Text = self.OGText
        for x, y in zip(self.Replace, self.ReplaceWith):
            self.Text = self.Text.replace(x, y)
        return Rerolled #return is used in self.Voice

    def Voice(self, Voice=None, Repeats:int=1, CreateALL=False, Rate=200):
        self.VoiceText = TextParser.ManualParser(self.Text)
        #self.VoiceText = self.Text
        if not self.UsedURL:
            print("Last chance to reroll!")
            if self.Reroll():
                self.VoiceText = TextParser.ManualParser(self.Text)
        TTSs = Voices.TTS(self.VoiceText)
        if Voice:
            pass
            #self.TiktokPath = TTSs.TiktokTTS(Voice=Voice, Repeat=Repeats)
        elif CreateALL:
            self.TiktokPath = TTSs.CreateALLTiktokVoices()
        else:
            Voice = random.choice([
            "en_us_006",
            "en_us_009",
            "en_us_010",
            "en_uk_003",
            "en_au_002",
            "en_us_007",
            "en_us_001"])
            self.TiktokPath = TTSs.TiktokTTS(Voice=Voice, Repeat=Repeats)
        self.gTTSPath = TTSs.GoogleTranslateTTS(Repeat=Repeats)
        self.PyPath = TTSs.PyTTS(Repeat=Repeats, Rate=Rate)

if __name__ == "__main__": #driver code
    TimeStart = time.perf_counter()
    FinalVidsDir = "GeneratedVideos"
    if not os.path.exists(f".\\{FinalVidsDir}\\"):
            print(f"Creating .\\{FinalVidsDir}\\")
            os.mkdir(f".\\{FinalVidsDir}\\")
    if not os.path.exists(".\\MinecraftVid.mp4"):
        MinecraftParkour = "https://www.youtube.com/watch?v=n_Dv4JMiwK8&ab_channel=bbswitzer"
        Background.YoutubeMinecraftParkour(MinecraftParkour, filename="MinecraftVid.mp4")
    FinalVidName = input("What should the name of the final video be? (without the file extension)\n")
    #VideoMaker = VideoMaker("AskReddit+nosleep+tifu+relationship_advice+AmItheAsshole+UnresolvedMysteries+humansoflatecapitalism", Multi=True)
    print("Getting a submission...")
    #VideoMaker.GetSubmission()
    #VideoMaker.GetSubmissionURL("https://www.reddit.com/r/todayilearned/comments/1c9hbvm/til_in_the_1870s_the_city_of_liège_belgium_tried/")
    #"https://www.reddit.com/r/todayilearned/comments/1cevz1a/til_there_is_a_species_of_lizard_that_removes/"
    
    VideoMaker = VideoMaker()
    VideoMaker.Text = "I would like to thank Lucas for nominating me for the USC speak your mind challenge. \
        splash splash. splash. splash splash splash. \
        I would like to nominate Heider Al Chalabi, Nick Greasepan, and Magnus La Plante. you got 24 hours. Time starts now."
    VideoMaker.Voice("en_uk_003", Rate=130)
    TTSChoice = input("Tiktok, Google Translate or PyTTS?\n").lower()
    while TTSChoice not in ("tt", "tiktok", "t", "ttts", "tttts",
                            "g", "google", "gg", "gtts",
                            "p", "pythonTTS", "py", "pytts", "ptts"):
        TTSChoice = input("Tiktok, Google Translate or PyTTS?\n").lower()
    match TTSChoice:
        case ("tt"| "tiktok"| "t"| "ttts"| "tttts"):
            TTSChoice = VideoMaker.TiktokPath
        case ("g" | "google" | "gg" | "gtts"):
            TTSChoice = VideoMaker.gTTSPath
        case ("p" | "pythonTTS" | "py" | "pytts" | "ptts"):
            TTSChoice = VideoMaker.PyPath
        case _:
            print("You did the impossible! A random TTS voice will be choosen.")
            TTSChoice = random.choice((VideoMaker.TiktokPath, VideoMaker.gTTSPath, VideoMaker.PyPath))
    TTSClip = moviepy.editor.AudioFileClip(str(TTSChoice))
    TTSClipDuration = TTSClip.duration #duration in seconds
    BackgroundClip = moviepy.editor.VideoFileClip(f"{os.path.dirname(__file__)}\\MinecraftVid.mp4")
    BackgroundClipDuration = BackgroundClip.duration
    RandomStartPoint = random.randint(0, int(BackgroundClipDuration-TTSClipDuration))
    BackgroundClip = BackgroundClip.subclip(RandomStartPoint, RandomStartPoint+TTSClipDuration)
    w, h = BackgroundClip.size
    #print(f"16/9 is {16/9}, 9/16 is {9/16}")
    #print(w, h, w/h, h/w)
    NewWidth = h*(h/w)
    NewHeight = w*(h/w) #height should be the same
    #print(NewWidth, NewHeight, NewWidth/NewHeight, NewHeight/NewWidth)
    XTranslate1 = w/2-NewWidth/2 #translate to center it
    #x = width
    #y = height
    BackgroundClip = BackgroundClip.fx(vfx.crop, x1=0+XTranslate1, y1=0, x2=NewWidth+XTranslate1, y2=NewHeight)
    SubtitlesText = VideoMaker.VoiceText
    WhisperAudioFile = f".\\{FinalVidsDir}\\{FinalVidName}.mp3"
    TTSClip.write_audiofile(WhisperAudioFile)
    print("Using (faster) Whisper to make subtitles...")
    model_size = "large-v3"
    model = faster_whisper.WhisperModel(model_size, device="cpu", compute_type="float32")
    segments, info = model.transcribe(WhisperAudioFile, beam_size=10, language="en", word_timestamps=True)
    print("Transcribing done! Making Subtitle file...")
    WhisperSubtitlesList = []
    Count = 0
    for segment in segments:
        for word in segment.words:
            Count +=1
            WhisperSubtitlesList.append(f"{word.start} --> {word.end}:{word.word}") #basically like a .srt file format
    print("Done creating subtitle file contents!")
    with open("SubtitlesReference.txt", "w") as f:
        f.write(VideoMaker.VoiceText.replace(" ", "\n"))
        f.flush()
        os.fsync(f.fileno())
    print("Done with subtitle file generation!")
    print("opening subtitle file for manual editing")
    subprocess.run(["code", f"{os.getcwd()}\\SubtitlesReference.txt", "-r"], shell=True)
    WhisperSubtitlesList = TextParser.ManualParser("\n".join(WhisperSubtitlesList), filename=f".\\{FinalVidsDir}\\{FinalVidName}_Subtitles.txt").split("\n")
    print("Extracting values from subtitle file")
    for Index, x in enumerate(WhisperSubtitlesList):
        Start = float(x[:x.index("-->")])
        End = float(x[x.index("--> ")+4:x.index(":")])
        Word = (x[x.index(":")+2:])
        WhisperSubtitlesList[Index] = Start, End, Word
    ColorList = list(map(lambda x: x.decode(), moviepy.editor.TextClip.list("color")))
    for x in ColorList:
        if "grey" in x or "gray" in x:
            ColorList.remove(x)
    Color = "cyan"#random.choice(ColorList)
    ColorStroke = "black" #random.choice(ColorList)
    SubtitleClips = []
    print(f"There are {len(WhisperSubtitlesList)} words! Generating subtitles...")
    for (Index, (Start, End, Word)) in enumerate(WhisperSubtitlesList):
        SubtitleClip = (moviepy.editor.TextClip(
            Word, color=Color, font="Source-Sans-Pro-Black",
            stroke_color=ColorStroke, method="caption", stroke_width=1.5, size=(w/1.2, h/12)
            )
            .set_duration(End-Start).set_position("center").set_start(Start).crossfadein(.1)
            )
        #Color = random.choice(ColorList)
        SubtitleClips.append(SubtitleClip)
    print("Subtitles done!")
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS #resize function uses PIL.Image.ANTIALIAS, but that has been removed in PIL 10.0.0
    BackgroundClip = BackgroundClip.fx(vfx.resize, height=1080)
    w, h = BackgroundClip.size
    BackgroundClip = moviepy.editor.CompositeVideoClip([BackgroundClip, *SubtitleClips], use_bgclip=True)
    BackgroundClip = BackgroundClip.set_audio(TTSClip)
    #On my computer these work best (with a mp4 file extension): (a=audio codec, v=video codec)
    #aac (a)
    #libx264 (v)
    #h264_nvenc (v)
    #libvpx-vp9 (v)
    TimeWriteStart = time.perf_counter()
    BackgroundClip.write_videofile(f".\\{FinalVidsDir}\\{FinalVidName}.mp4", threads=os.cpu_count(), audio_codec="aac", codec="libx264", fps=30)
    #BackgroundClip.write_videofile(f"TEST.webm", threads=8)
    VideoTime = time.perf_counter()-TimeWriteStart
    TotalTime = time.perf_counter()-TimeStart
    print(f"Video created in {VideoTime} seconds! :)")
    print(f"Total script time: {TotalTime} seconds! :)")
    BackgroundClip.close()
    TTSClip.close()
    print(Color, ColorStroke)
  