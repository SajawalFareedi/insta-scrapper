import instagramy as insta
import requests

import json
import csv

import time
from time import sleep
from random import randint, choice
import traceback

from tqdm import tqdm

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


def getUserAgents():
    with open("./config/user-agents.txt", encoding="utf8") as UserAgentsFile:
        UserAgents = UserAgentsFile.read().split("\n")
        UserAgentsFile.close()
    return UserAgents


UserAgents = getUserAgents()

# proxy = getProxy()
proxy_host = ""  # proxy["http"].split("//")[1]
next_max_id = 24
next_page = ""

UserAgents.pop()

# Followers_ings = set()
# ImagesPosts = []
# VideosPosts = []
# MediaIds = set()
# Comments = []


def get_userInfo(user, session_id=var.SESSION_ID):
    instaUser = insta.InstagramUser(
        user, sessionid=session_id)  # , proxy=proxy_host

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


def saveFollowers_ings(username, isFirstTime):
    if isFirstTime == True:
        with open(var.NEW_USERS_FILE, mode="w+", encoding="utf8") as newUsersFile:
            newUsersFile.write(username + "\n")
            newUsersFile.close()
        return

    with open(var.NEW_USERS_FILE, mode="a", encoding="utf8") as newUsersFile:
        newUsersFile.write(username + "\n")
        newUsersFile.close()


def savePosts(isVideo, postInfo, isFirstTime):
    outputFile = var.VIDEOS_POSTS_FILE if isVideo == True else var.POSTS_FILE
    postInfoAoA = dictToAoA(postInfo, isFirstTime)

    if isFirstTime == True:
        with open(outputFile, mode="w+", encoding="utf8", newline='') as usersInfoFile:
            writer = csv.writer(usersInfoFile, delimiter=',')
            writer.writerows(postInfoAoA)
        return

    with open(outputFile, mode="a", encoding="utf8", newline='') as usersInfoFile:
        usersInfoFile.write(postInfoAoA)
        usersInfoFile.close()


def saveMediaId(id, isFirstTime):
    if isFirstTime == True:
        with open(var.MEDIA_IDS_FILE, mode="w+", encoding="utf8") as mediaInfoFile:
            mediaInfoFile.write(id + "\n")
            mediaInfoFile.close()
        return

    with open(var.MEDIA_IDS_FILE, mode="a", encoding="utf8") as mediaInfoFile:
        mediaInfoFile.write(id + "\n")
        mediaInfoFile.close()


def saveComments(data, isFirstTime):
    postInfoAoA = dictToAoA(data, isFirstTime)

    if isFirstTime == True:
        with open(var.COMMENTS_FILE, mode="w+", encoding="utf8", newline='') as commentsInfoFile:
            writer = csv.writer(commentsInfoFile, delimiter=',')
            writer.writerows(postInfoAoA)
        return

    with open(var.COMMENTS_FILE, mode="a", encoding="utf8", newline='') as commentsInfoFile:
        commentsInfoFile.write(postInfoAoA)
        commentsInfoFile.close()


def getFollowers(User, totalCount, maxCount, isFirstTime):
    try:
        page_count = round((totalCount/maxCount))
        if (totalCount/maxCount).is_integer():
            page_count += 1

        next_max_id = maxCount
        headers = {
            "authority": "i.instagram.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
            "cookie": f'csrftoken=D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0; ds_user_id=52486738194; sessionid={var.SESSION_ID}',
            "dnt": "1",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": f"{choice(UserAgents)}",
            "x-asbd-id": "198387",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYDRW"
        }
        for i in range(page_count):

            url = Urls(User, totalCountToFetchAtOnce=maxCount).generateUrl(
                "followers", next_max_id)
            r = requests.get(url=url, headers=headers,
                             proxies=org_proxy, verify=False)

            data = json.loads(
                r.text) if r.status_code == 200 else r.status_code
            if type(data).__name__ != "int":
                next_max_id = data['next_max_id']
                followers = data['users']
                for follower in followers:
                    saveFollowers_ings(follower['username'],  isFirstTime)
                    # Followers_ings.add(follower['username'])
                # print(Followers_ings.__len__())
            sleep(var.DELAY_BETWEEN_EACH_USER + randint(4, 11))
        # print(Followers_ings)
    except Exception as e:
        pass


def getFollowing(User, totalCount, maxCount, isFirstTime):
    try:
        page_count = round((totalCount/maxCount))
        if (totalCount/maxCount).is_integer():
            page_count += 1

        next_max_id = maxCount
        headers = {
            "authority": "i.instagram.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
            "cookie": f'csrftoken=D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0; ds_user_id=52486738194; sessionid={var.SESSION_ID}',
            "dnt": "1",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": f"{choice(UserAgents)}",
            "x-asbd-id": "198387",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "hmac.AR0FDdQJ0pjagtbdzFvaYn-bjAXDKiMoN3-eSe16cbp9L95X"
        }
        for i in range(page_count):

            url = Urls(User, totalCountToFetchAtOnce=maxCount).generateUrl(
                "following", next_max_id)

            r = requests.get(url=url, headers=headers,
                             proxies=org_proxy, verify=False)
            data = json.loads(
                r.text) if r.status_code == 200 else r.status_code
            if type(data).__name__ != "int":
                next_max_id = data['next_max_id']
                followers = data['users']
                for follower in followers:
                    # Followers_ings.add(follower['username'])
                    saveFollowers_ings(follower['username'], isFirstTime)
                # print(Followers_ings.__len__())
            sleep(var.DELAY_BETWEEN_EACH_USER + randint(4, 11))
        # print(Followers_ings)
    except Exception as e:
        pass


def extractPosts(posts, isFirstTime):
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
            "searchable_id": f"'{node['shortcode']}",
            "id": f"'{node['id']}",
            "post_date": f"'{time.ctime(node['taken_at_timestamp'])}",
            "likes_count": f"'{node['edge_media_preview_like']['count']}",
            "comments_count": f"'{node['edge_media_to_comment']['count']}",
            "tagged_users": f"\"{tagged_users}\""
        }

        saveMediaId(node["id"], isFirstTime)

        savePosts(isVideo, postInfo, isFirstTime)

        # if isVideo == True:
        # VideosPosts.append(json.dumps(postInfo))
        # else:
        # ImagesPosts.append(json.dumps(postInfo))


def getPosts(next_page, user_id, maxCount, user_name, isFirstTime):
    hasMorePosts = True
    csrf = "D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0"
    headers = {
        "authority": "www.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
        "cookie": f"csrftoken={csrf}; ds_user_id=52486738194; sessionid={var.SESSION_ID}",
        "dnt": "1",
        "referer": f"https://www.instagram.com/{user_name}/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": f"{choice(UserAgents)}",
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
        if type(data).__name__ != "int":
            posts = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
            extractPosts(posts, isFirstTime)
            hasMorePosts = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
            next_page = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"].replace(
                "==", "")
        else:
            hasMorePosts = False


def extractComments(data, media_id, isFirstTime):
    tagged_users = []
    i = 0

    if data['caption'] and data['caption']['text']:
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
            "id": f"'{media_id}",
            "user": f"'{comment['user']['username']}",
            "comment_like_count": f"'{comment['comment_like_count']}",
            "comment_date": f"'{time.ctime(comment['created_at'])}",
            "comment": f"'{comment['text']}",
            "tagged_users": f"'{','.join(tagged_users)}",
            "replies_count": f"'{comment['child_comment_count']}",
            "replies": f"'{replies}",
        }

        saveComments(comment_data, isFirstTime)
        # Comments.append(json.dumps(comment_data))
        tagged_users = []
        i += 1


def getComments(media_ids, isFirstTime):
    headers = {
        "authority": "i.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
        "cookie": f'csrftoken=D54W8UuHIkjTihGkZ5Q0Mk8B8g7fyKw0; ds_user_id=52486738194; sessionid={var.SESSION_ID}',
        "dnt": "1",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": f"{choice(UserAgents)}",
        "x-asbd-id": "198387",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYF3u"
    }
    for media_id in media_ids:
        if len(media_id) > 0:
            url = Urls(media_id=media_id).generateUrl(url_type="comments")
            r = requests.get(url=url, headers=headers,
                             proxies=org_proxy, verify=False)
            data = json.loads(
                r.text) if r.status_code == 200 else r.status_code
            if type(data).__name__ != "int":
                extractComments(data, media_id, isFirstTime)


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

    saveUserInfo(userData, isFirstTime)

    user_id = userInfo['id']
    username = userInfo['username']
    followersCount = userInfo['edge_followed_by']['count']
    followingCount = userInfo['edge_follow']['count']

    getFollowers(user_id, followersCount, var.MAX_FOLLOWERS, isFirstTime)
    getFollowing(user_id, followingCount, var.MAX_FOLLOWINGS, isFirstTime)

    if userInfo['edge_owner_to_timeline_media']['page_info']['has_next_page'] == True:
        extractPosts(posts, isFirstTime)
        getPosts(next_page, user_id, var.MAX_POSTS, username, isFirstTime)
    else:
        extractPosts(posts, isFirstTime)

    with open(var.MEDIA_IDS_FILE, "r", encoding="utf8") as mediaIdsFile:
        mediaIds = mediaIdsFile.read().split("\n")
        getComments(mediaIds, isFirstTime)


def main(usernames):
    usernames.pop() if len(usernames[len(usernames) - 1]) == 0 else None

    for i in tqdm(range(len(usernames)), leave=False, colour='blue'):
        User = usernames[i]
        Delay = var.DELAY_BETWEEN_EACH_USER + randint(3, 8)
        isFirstTime = True if i == 0 else False
        for i in tqdm(range(var.HOPS), colour='green'):
            if i == 0:
                scrapeUser(User, isFirstTime)
            else:
                pass

        sleep(Delay)


# TODO: Develop HOPS functionality
# TODO: Fix save issue

if __name__ == "__main__":
    try:
        # usernames = readInputFile()
        # usernames = usernames.split("\n")
        main(['artvestest1'])
        # getFollowers("6048734544", 3640, 100)
        # getPosts(next_page="QVFETE00WHpoT1BHQ21CT2hGZlpZNTVvTlI2cmZweE05RVc5QWpYaTF3cUdGeUpWRkF0ZzFZcFNSZzRTYjEtWFRKMi0yMFZobEJhTDZUNVJZMnV2UWlRZg",
        #          user_id="2504145151", maxCount=50, user_name="mo_space")
        # getComments(["2718218520583178499", "2708877775376216707"])
        # getFollowing("6048734544", 634, var.MAX_FOLLOWINGS)
        pass
    except Exception:
        print(traceback.format_exc())
