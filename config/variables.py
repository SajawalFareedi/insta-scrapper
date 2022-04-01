class Variables():
    def __init__(self):

        self.PROXY_SERVER_URL = "http://127.0.0.1:8080/generate-proxy/"

        self.SESSION_ID = "24802582994%3AAHTOMNWLTOdHaH%3A13"
        self.DELAY_BETWEEN_EACH_USER = 1
        self.HOPS = 2
        self.FILES_EXTENSION = ".csv"

        self.OUTPUT_FILE_PATH = "./output/"
        self.INPUT_FILE_PATH = "./input/"

        self.INPUT_FILE_NAME = "input"
        self.USERINFO_OUTPUT_FILE_NAME = "userInfo"
        self.POSTS_OUTPUT_FILE_NAME = "postsInfo"
        self.COMMENTS_OUTPUT_FILE_NAME = "commentsInfo"
        self.NEW_USERS_OUTPUT_FILE_NAME = "newUserInfo"

        self.INPUT_FILE = f"{self.INPUT_FILE_PATH}{self.INPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.USERINFO_FILE = f"{self.OUTPUT_FILE_PATH}{self.USERINFO_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.POSTS_FILE = f"{self.OUTPUT_FILE_PATH}{self.POSTS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.COMMENTS_FILE = f"{self.OUTPUT_FILE_PATH}{self.COMMENTS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
        self.NEW_USERS_FILE = f"{self.OUTPUT_FILE_PATH}{self.NEW_USERS_OUTPUT_FILE_NAME}{self.FILES_EXTENSION}"
