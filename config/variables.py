class Variables():
    def __init__(self):

        self.PROXY_SERVER_URL = "http://127.0.0.1:8080/generate-proxy-tunnel/"

        self.SESSION_ID = "52486738194%3AwVUZoEFumSmC2O%3A21"
        self.DELAY_BETWEEN_EACH_USER = 1
        self.HOPS = 3
        self.FILES_EXTENSION = ".csv"

        self.OUTPUT_FILE_PATH = "./output/"
        self.INPUT_FILE_PATH = "./input/"

        self.INPUT_FILE_NAME = "input"
        self.USERINFO_OUTPUT_FILE_NAME = "userInfo"
        self.POSTS_OUTPUT_FILE_NAME = "postsInfo"
        self.VIDEOS_POSTS_OUTPUT_FILE_NAME = "videosPostsInfo"
        self.COMMENTS_OUTPUT_FILE_NAME = "commentsInfo"
        self.NEW_USERS_OUTPUT_FILE_NAME = "newUserInfo"
        self.MEDIA_IDS_FILE_NAME = "mediaIds"

        self.INPUT_FILE = f"{self.INPUT_FILE_PATH}{self.INPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.USERINFO_FILE = f"{self.OUTPUT_FILE_PATH}{self.USERINFO_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.POSTS_FILE = f"{self.OUTPUT_FILE_PATH}{self.POSTS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.VIDEOS_POSTS_FILE = f"{self.OUTPUT_FILE_PATH}{self.VIDEOS_POSTS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.COMMENTS_FILE = f"{self.OUTPUT_FILE_PATH}{self.COMMENTS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.NEW_USERS_FILE = f"{self.OUTPUT_FILE_PATH}{self.NEW_USERS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.MEDIA_IDS_FILE = f"{self.OUTPUT_FILE_PATH}{self.MEDIA_IDS_FILE_NAME}{self.FILES_EXTENSION}"

        self.MAX_FOLLOWERS = 12
        self.MAX_FOLLOWINGS = 12
        self.MAX_POSTS = 12
