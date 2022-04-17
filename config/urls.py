class Urls():
    def __init__(self, user_id=None, totalCountToFetchAtOnce=12, media_id=None, postsToFetchAtOnce=12, page_count=2):
        self.count = totalCountToFetchAtOnce
        self.user = user_id
        self.media = media_id
        self.posts_count = postsToFetchAtOnce
        self.page_count = page_count

    def generateUrl(self, url_type=None, max_id=None, next_page=None):
        if url_type == "followers":
            if self.page_count <= 1:
                return f"https://i.instagram.com/api/v1/friendships/{self.user}/followers/?count={self.count}&search_surface=follow_list_page"
            return f"https://i.instagram.com/api/v1/friendships/{self.user}/followers/?count={self.count}&max_id={max_id}&search_surface=follow_list_page"
        elif url_type == "following":
            if self.page_count <= 1:
                return f"https://i.instagram.com/api/v1/friendships/{self.user}/following/?count={self.count}"
            return f"https://i.instagram.com/api/v1/friendships/{self.user}/following/?count={self.count}&max_id={max_id}"
        elif url_type == "comments":
            if self.page_count <= 1:
                return f"https://i.instagram.com/api/v1/media/{self.media}/comments/?can_support_threading=true&permalink_enabled=false"
            return f"https://i.instagram.com/api/v1/media/{self.media}/comments/?can_support_threading=true&permalink_enabled=true"
        elif url_type == "posts":
            return f"https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%22{self.user}%22%2C%22first%22%3A{self.posts_count}%2C%22after%22%3A%22{next_page}%3D%3D%22%7D"
        else:
            return """
No Url found for the given url_type. Available types are following:\n
    1) followers
    2) following
    3) comments
    4) posts
            """
