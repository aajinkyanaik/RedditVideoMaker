import pytube
import os.path

MinecraftParkour = "https://www.youtube.com/watch?v=n_Dv4JMiwK8&ab_channel=bbswitzer"

#adaptive streams are split, video and audio (higher quality though)
#progressive are one video stream

def YoutubeMinecraftParkour(MinecraftParkour:str="https://www.youtu.be/watch?v=n_Dv4JMiwK8",
                            output_path: str|None = os.path.dirname(__file__),
                            filename_prefix: str|None ="", 
                            filename: str|None = None,
                            skip_existing: bool = True,
                            Res:str = "720p"
                            ):
    Streams = pytube.YouTube(MinecraftParkour).streams.filter(progressive=True) #adaptive because sound won't be used
    Path = Streams.filter(file_extension="mp4", type="video", res=Res).desc().first()
    print(Path)
    Path.download(
        output_path=output_path, filename_prefix=filename_prefix,
        filename=filename, skip_existing=skip_existing
        )
    print(f"Path to Youtube video: {Path}")
    return Path

if __name__ == "__main__":
    YoutubeMinecraftParkour(MinecraftParkour, filename="MinecraftVid.mp4")

