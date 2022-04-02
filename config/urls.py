class Urls():
    def __init__(self, user_id=None, totalCountToFetchAtOnce=12, media_id=None):
        self.count = totalCountToFetchAtOnce
        self.user = user_id
        self.media = media_id

    def generateUrl(self, url_type=None, max_id=None):
        if url_type == "followers":
            return f"https://i.instagram.com/api/v1/friendships/{self.user}/followers/?count={self.count}&max_id={max_id}&search_surface=follow_list_page"
        elif url_type == "following":
            return f"https://i.instagram.com/api/v1/friendships/{self.user}/following/?count={self.count}"
        elif url_type == "comments":
            return f"https://i.instagram.com/api/v1/media/{self.media}/comments/?can_support_threading=true&permalink_enabled=true"
        else:
            return """
No Url found for the given url_type. Available types are following:\n
    1) followers
    2) following
    3) comments
            """
