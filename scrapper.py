import instagramy as insta

import requests

import json
import csv
import pandas as pd

import time
from time import sleep
from random import randint

from config.variables import Variables
from config.urls import Urls

var = Variables()

org_proxy = {
    "http": "http://kuetxqpq-rotate:dwcgpcu5fdwv@p.webshare.io:9999/",
    "https": "http://kuetxqpq-rotate:dwcgpcu5fdwv@p.webshare.io:9999/"
}

# org_proxy = {
#     "http": "http://rynym:aNaPEHnJDW4gma4u@proxy.packetstream.io:31112",
#     "https": "http://rynym:aNaPEHnJDW4gma4u@proxy.packetstream.io:31112"
# }


def getProxy():
    r = requests.get(var.PROXY_SERVER_URL)
    return {
        "http": f"http://{r.text}",
        "https": f"https://{r.text}"
    }


# proxy = getProxy()
proxy_host = ""  # proxy["http"].split("//")[1]
next_max_id = 100
next_page = ""

Followers_ings = set()
ImagesPosts = []
VideosPosts = []
MediaIds = set()
Comments = []


def get_userInfo(user, session_id=var.SESSION_ID):
    instaUser = insta.InstagramUser(
        user, sessionid=session_id, proxy=proxy_host)

    userInfo = instaUser.get_json()
    # with open("./json/mo_space.json", "w+", encoding="utf8") as file:
    #     file.write(json.dumps(userInfo))
    #     file.close()
    return userInfo


def readInputFile():
    data = ""
    with open(var.INPUT_FILE, "r", encoding="utf8") as inputFile:
        data = inputFile.read()
        inputFile.close()
    return data


def dictToAoA(userData, isFirstTime):
    newUserData = []
    header = []
    row = []
    userData = dict(userData)

    for key in userData.keys():
        header.append(key)
    newUserData.append(header)

    for key in userData:
        row.append(userData[key])
    newUserData.append(row)

    if isFirstTime == True:
        return newUserData
    else:
        return (",".join(row)) + "\n"


def saveUserInfo(userData, isFirstTime):
    userDataAoA = dictToAoA(userData, isFirstTime)
    if isFirstTime == True:
        with open(var.USERINFO_FILE, mode="w+", encoding="utf8", newline='') as usersInfoFile:
            writer = csv.writer(usersInfoFile, delimiter=',')
            writer.writerows(userDataAoA)
            return

    with open(var.USERINFO_FILE, mode="a", encoding="utf8", newline='') as usersInfoFile:
        usersInfoFile.write(userDataAoA)
        usersInfoFile.close()


def saveFollowers_ings():
    pass


def savePosts():
    pass


def saveComments():
    pass


def getFollowers(User, totalCount, maxCount):
    page_count = round((totalCount/maxCount) + 1)
    next_max_id = maxCount
    headers = {
        "authority": "i.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
        "cookie": 'csrftoken=D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0; ds_user_id=52486738194; sessionid=52486738194%3AwVUZoEFumSmC2O%3A21',
        "dnt": "1",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        "x-asbd-id": "198387",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYDRW"
    }
    for i in range(page_count):
        url = Urls(User, totalCountToFetchAtOnce=maxCount).generateUrl(
            "followers", next_max_id)
        r = requests.get(url=url, headers=headers,
                         proxies=org_proxy, verify=False)

        data = json.loads(r.text) if r.status_code == 200 else r.status_code
        next_max_id = data['next_max_id']
        followers = data['users']
        for follower in followers:
            Followers_ings.add(follower['username'])
        # print(Followers_ings.__len__())
        sleep(var.DELAY_BETWEEN_EACH_USER + randint(4, 11))
    # print(Followers_ings)


def getFollowing(User, totalCount, maxCount):
    try:
        page_count = round((totalCount/maxCount) + 1)
        next_max_id = maxCount
        headers = {
            "authority": "i.instagram.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
            "cookie": 'csrftoken=D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0; ds_user_id=52486738194; sessionid=52486738194%3AwVUZoEFumSmC2O%3A21',
            "dnt": "1",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "x-asbd-id": "198387",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "hmac.AR0FDdQJ0pjagtbdzFvaYn-bjAXDKiMoN3-eSe16cbp9L95X"
        }
        for i in range(page_count):
            url = Urls(User, totalCountToFetchAtOnce=maxCount).generateUrl(
                "following", 600)

            r = requests.get(url=url, headers=headers,
                             proxies=org_proxy, verify=False)
            data = json.loads(
                r.text) if r.status_code == 200 else r.status_code
            next_max_id = data['next_max_id']
            followers = data['users']
            print(r.text)
            for follower in followers:
                Followers_ings.add(follower['username'])
            print(Followers_ings.__len__())
            sleep(var.DELAY_BETWEEN_EACH_USER + randint(4, 11))
            break
        print(Followers_ings)
    except Exception as e:
        print("Got an error while fetching followings:", e)


def extractPosts(posts):
    for post in posts:
        node = post['node']
        tagged_users = []

        isVideo = True if node['__typename'] == "GraphVideo" else False

        for user in node["edge_media_to_tagged_user"]["edges"]:
            User = user["node"]["user"]
            tagged_user = {
                "id": User["id"],
                "username": User["username"],
                "full_name": User["full_name"],
                "is_verified": User["is_verified"],
                # "followed_by_viewer": User["followed_by_viewer"],
                "profile_pic_url": User["profile_pic_url"]
            }

            tagged_users.append(tagged_user)

        postInfo = {
            "searchable_id": node['shortcode'],
            "id": node["id"],
            "post_date": time.ctime(node["taken_at_timestamp"]),
            "likes_count": node["edge_media_preview_like"]["count"],
            "comments_count": node["edge_media_to_comment"]["count"],
            "tagged_users": tagged_users
        }

        MediaIds.append(node["id"])

        if isVideo == True:
            VideosPosts.append(json.dumps(postInfo))
        else:
            ImagesPosts.append(json.dumps(postInfo))


def getPosts(next_page, user_id, maxCount, user_name):
    hasMorePosts = True
    csrf = "D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0"
    headers = {
        "authority": "www.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
        "cookie": f"csrftoken={csrf}; ds_user_id=52486738194; sessionid=52486738194%3AwVUZoEFumSmC2O%3A21",
        "dnt": "1",
        "referer": f"https://www.instagram.com/{user_name}/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        "x-asbd-id": "198387",
        "x-csrftoken": f"{csrf}",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYFPz",
        "x-requested-with": "XMLHttpRequest"
    }

    while hasMorePosts == True:
        url = Urls(user_id=user_id, postsToFetchAtOnce=maxCount).generateUrl(
            "posts", next_page=next_page)
        r = requests.get(url=url, headers=headers,
                         proxies=org_proxy, verify=False)
        data = json.loads(r.text) if r.status_code == 200 else r.status_code
        posts = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        extractPosts(posts)
        hasMorePosts = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
        next_page = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"].replace(
            "==", "")


def extractComments(data, media_id):
    tagged_users = []

    for word in data['caption']['text'].split(" "):
        if word.startswith("@"):
            tagged_users.append(word.strip())

    for comment in data['comments']:
        replies = []
        for word in comment['text'].split(" "):
            if word.strip().startswith("@"):
                tagged_users.append(word.strip())

        if comment['child_comment_count'] > 0:
            for child_comment in comment['preview_child_comments']:
                reply = {
                    "user_id": child_comment['user']['pk'],
                    "username": child_comment['user']['username']
                }
                replies.append(reply)

        comment_data = {
            "id": media_id,
            "user": comment['user']['username'],
            "comment_like_count": comment['comment_like_count'],
            "comment_date": time.ctime(comment['created_at']),
            "comment": comment['text'],
            "tagged_users": ",".join(tagged_users),
            "replies_count": comment['child_comment_count'],
            "replies": replies,
        }

        Comments.append(json.dumps(comment_data))
        tagged_users = []


def getComments(media_ids):
    headers = {
        "authority": "i.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
        "cookie": 'csrftoken=D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0; ds_user_id=52486738194; sessionid=52486738194%3AwVUZoEFumSmC2O%3A21',
        "dnt": "1",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        "x-asbd-id": "198387",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYF3u"
    }
    for media_id in media_ids:
        url = Urls(media_id=media_id).generateUrl(url_type="comments")
        r = requests.get(url=url, headers=headers,
                         proxies=org_proxy, verify=False)
        data = json.loads(r.text) if r.status_code == 200 else r.status_code
        extractComments(data, media_id)
    print(Comments)


def scrapeUser(User, isFirstTime):
    userInfo = get_userInfo(User)[
        'entry_data']['ProfilePage'][0]['graphql']['user']

    posts = userInfo['edge_owner_to_timeline_media']['edges']
    next_page = userInfo['edge_owner_to_timeline_media']['page_info']['end_cursor'].replace(
        "==", "")

    userData = {
        "external_url": f"'{userInfo['external_url']}",
        "is_verified": f"'{userInfo['is_verified']}",
        "edge_followed_by_count": f"'{userInfo['edge_followed_by']['count']}",
        "edge_follow_count": f"'{userInfo['edge_follow']['count']}",
        "id": f"'{userInfo['id']}",
        "highlight_reel_count": f"'{userInfo['highlight_reel_count']}",
        "is_business_account": f"'{userInfo['is_business_account']}",
        "is_professional_account": f"'{userInfo['is_professional_account']}",
        "category_enum": f"'{userInfo['category_enum']}",
        "category_name": f"'{userInfo['category_name']}",
        "is_private": f"'{userInfo['is_private']}",
        "profile_pic_url": f"'{userInfo['profile_pic_url']}",
        "username": f"'{userInfo['username']}",
        "edge_owner_to_timeline_media_count": f"'{userInfo['edge_owner_to_timeline_media']['count']}",
    }

    user_id = userInfo['id']
    username = userInfo['username']
    followersCount = userInfo['edge_followed_by']['count']
    followingCount = userInfo['edge_follow']['count']

    getFollowers(user_id, followersCount, var.MAX_FOLLOWERS)
    getFollowing(user_id, followingCount, var.MAX_FOLLOWINGS)

    if userInfo['edge_owner_to_timeline_media']['page_info']['has_next_page'] == True:
        extractPosts(posts)
        getPosts(next_page, user_id, var.MAX_POSTS, username)
    else:
        extractPosts(posts)

    getComments(list(MediaIds))

    saveUserInfo(userData, isFirstTime)
    savePosts()
    saveComments()


def main(usernames):
    usernames.pop() if len(usernames[len(usernames) - 1]) == 0 else None

    for i in range(0, len(usernames) - 1):
        User = usernames[i]
        Delay = var.DELAY_BETWEEN_EACH_USER + randint(3, 8)
        isFirstTime = True if i == 0 else False

        for i in range(var.HOPS):
            if i == 0:
                scrapeUser(User, isFirstTime)
            else:
                pass

        print(f"Scraping Successful for user: {User}")
        sleep(Delay)


# TODO: Create Progress Bar
# TODO: Check Status Code
# TODO: Handle 'next_max_id' error
# TODO: Add functionality to continue instead of starting over again
if __name__ == "__main__":
    try:
        # usernames = readInputFile()
        # usernames = usernames.split("\n")
        # extractDataWithInstagramy(usernames)
        # getFollowers("6048734544", 3640, 100)
        # getPosts(next_page="QVFETE00WHpoT1BHQ21CT2hGZlpZNTVvTlI2cmZweE05RVc5QWpYaTF3cUdGeUpWRkF0ZzFZcFNSZzRTYjEtWFRKMi0yMFZobEJhTDZUNVJZMnV2UWlRZg",
        #          user_id="2504145151", maxCount=50, user_name="mo_space")
        # getComments(["2718218520583178499", "2708877775376216707"])
        getFollowing("6048734544", 634, var.MAX_FOLLOWINGS)
        pass
    except Exception as e:
        print("Got an error", e)
