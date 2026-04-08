import praw
import praw.models
import os
import os.path
import pathlib
import json
import base64
import sys
import random
import dotenv
import praw.models.comment_forest
import praw.models.reddit
import praw.models.reddit.submission

class Reddit:
    dotenv.load_dotenv(f"{os.path.dirname(__file__)}\\RedditClient.env")
    def __init__(self,
                 ClientID:str = os.environ["REDDIT_SCRIPT_CLIENTID"],
                 ClientSecret:str = os.environ["REDDIT_SCRIPT_SECRET"],
                 ClientUsername:str = os.environ["REDDIT_SCRIPT_USERNAME"]) -> None:
        UserAgent = f"script: RedditStoryBot: 0.0.0 (by /u{ClientUsername})"
        self.reddit = praw.Reddit(
            client_id=ClientID,
            client_secret=ClientSecret,
            user_agent=UserAgent
            )
        self.RandomDefault = \
        ["amiwrong",
        "offmychest",
        "AITAH",
        "AmItheAsshole",
        "TrueOffMyChest"] #TODO, add more subreddits to this list
        Undef = None
        #praw sadly doesnt have typehinting so im addding it here
        self.Submission: praw.models.reddit.submission.Submission = Undef
        self.SubmissionTitle: str = str()
        self.SubmissionScore: int = int()
        self.SubmissionCommentAmount:int = int()
        self.SubmissionAuthorName: str = str()
        self.SubmissionCommentsForest: praw.models.comment_forest.CommentForest = Undef
        self.SubmissionNSFW: bool = bool()
        self.SubmissionBody: str = str()
        self.SubmissionBodyOnly: bool = bool()
        self.SubmissionLink: str = str()
        self.SubmissionModPost: bool = bool()
        self.SubmissionShortLink: str = str()
        self.SubmissionLPermink: str = str()

    def getSubmissionURL(self, URL:str="") -> praw.models.Submission:
        Submission:praw.models.Submission = self.reddit.submission(url=URL)
        print(f"Using {Submission.url}")
        #idk how to use super() so im doing it this way: (also i can rename variables if I do it this way)
        self.Submission: praw.models.reddit.submission.Submission = Submission
        self.SubmissionTitle: str = Submission.title
        self.SubmissionScore: int = Submission.score
        self.SubmissionCommentAmount: int = Submission.num_comments
        self.SubmissionAuthorName: str = Submission.author.name
        self.SubmissionCommentsForest: praw.models.comment_forest.CommentForest = Submission.comments
        self.SubmissionNSFW: bool = Submission.over_18
        self.SubmissionBody: str = Submission.selftext
        self.SubmissionBodyOnly: bool = Submission.is_self
        self.SubmissionLink: str = Submission.url
        self.SubmissionModPost: bool = Submission.stickied
        self.SubmissionShortLink: str = Submission.shortlink
        self.SubmissionLPermink: str = Submission.permalink
        return Submission
    
    def getSubmissionSubreddit(self, subreddit:praw.models.Subreddit|str, Sortby:str, time_filter="all", limit=5) -> praw.models.Submission:
        """
        Time_filter can be: "all", "day", "hour", "month", "week", or "year" (default: "all").
        """
        if type(subreddit) == str:
            subreddit = self.reddit.subreddit(subreddit.replace("r/", ""))
        match Sortby.lower():
            case "h" | "hot":
                Submission:praw.models.Submission = random.choice(list(subreddit.hot(limit=limit)))
            case "c" | "controversial":
                Submission:praw.models.Submission = random.choice(list(subreddit.controversial(time_filter=time_filter, limit=limit)))
            case "n" | "new":
                Submission:praw.models.Submission = random.choice(list(subreddit.new(limit=limit)))
            case "r" | "rising":
                Submission:praw.models.Submission = random.choice(list(subreddit.rising(limit=limit)))
            case "t" | "top":
                Submission:praw.models.Submission = random.choice(list(subreddit.top(time_filter=time_filter, limit=limit)))
            case _:
                Submission:praw.models.Submission = subreddit.random()
        #idk how to use super() so im doing it this way:
        self.Submission: praw.models.reddit.submission.Submission = Submission
        self.SubmissionTitle: str = Submission.title
        self.SubmissionScore: int = Submission.score
        self.SubmissionCommentAmount : int = Submission.num_comments
        self.SubmissionAuthorName: str = Submission.author.name
        self.SubmissionCommentsForest: praw.models.comment_forest.CommentForest = Submission.comments
        self.SubmissionNSFW: bool = Submission.over_18
        self.SubmissionBody: str = Submission.selftext
        self.SubmissionBodyOnly: bool = Submission.is_self
        self.SubmissionLink: str = Submission.url
        self.SubmissionModPost: bool = Submission.stickied
        self.SubmissionShortLink: str = Submission.shortlink
        self.SubmissionLPermink: str = Submission.permalink
        return Submission
    
    def getRandomSubreddit(self, List:list=[], UseMulti:bool=False) -> praw.models.Subreddit:
        if UseMulti and List: 
            Subreddit = "+".join(List)
        elif not UseMulti and List:
            Subreddit = random.choice(List)
        elif UseMulti and not List: #Empty lists are False
            Subreddit = "+".join(self.RandomDefault) 
        elif not UseMulti and not List:
            Subreddit = random.choice(self.RandomDefault)
        return self.reddit.subreddit(Subreddit.replace("r/", ""))
    

#reddit.subreddit("test").random()


if __name__ == "__main__":
    A = Reddit()
    A.getSubmissionSubreddit("AmItheAsshole", "hot")
    print(A.Submission)
    print(A.SubmissionTitle)
    print(A.SubmissionScore)
    print(A.SubmissionCommentAmount)
    print(A.SubmissionAuthorName)
    print(A.SubmissionCommentsForest)
    print(A.SubmissionNSFW)
    print(A.SubmissionBody)
    print(A.SubmissionBodyOnly)
    print(A.SubmissionLink)
    print(A.SubmissionModPost)
    print(A.SubmissionShortLink)
    print(A.SubmissionLPermink)

