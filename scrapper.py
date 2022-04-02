import instagramy as insta

import requests

import json
import csv
import pandas as pd

from time import sleep
from random import randint

from config.variables import Variables
from config.urls import Urls

var = Variables()

# org_proxy = {
#     "http": "http://kuetxqpq-rotate:dwcgpcu5fdwv@p.webshare.io:9999/",
#     "https": "http://kuetxqpq-rotate:dwcgpcu5fdwv@p.webshare.io:9999/"
# }

org_proxy = {
    "http": "http://rynym:aNaPEHnJDW4gma4u@proxy.packetstream.io:31112",
    "https": "http://rynym:aNaPEHnJDW4gma4u@proxy.packetstream.io:31112"
}


def getProxy():
    r = requests.get(var.PROXY_SERVER_URL)
    return {
        "http": f"http://{r.text}",
        "https": f"https://{r.text}"
    }


# proxy = getProxy()
proxy_host = ""  # proxy["http"].split("//")[1]


def get_userInfo(user, session_id=var.SESSION_ID):
    instaUser = insta.InstagramUser(
        user, sessionid=session_id, proxy=proxy_host)

    userInfo = instaUser.get_json()

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


def getFollowers(User, totalCount, maxCount):
    page_count = round((totalCount/maxCount) + 1)
    headers = {
        "authority": "i.instagram.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
        "cookie": 'csrftoken=imei0lpcmj8TJW6pUjr8Tmm3mthio0AK; ds_user_id=24802582994; sessionid=24802582994%3ADsAxOtayIBO4eA%3A25',
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
    for i in range(5):
        next_max_id = maxCount
        url = Urls(User, totalCountToFetchAtOnce=maxCount).generateUrl(
            "followers", next_max_id)
        r = requests.get(url=url, headers=headers,
                         proxies=org_proxy, verify=False)

        data = json.loads(r.text) if r.status_code == 200 else r.status_code
        next_max_id = data['next_max_id']
        followers = data['users']
        print("Username: ", followers[0]["username"])
        sleep(var.DELAY_BETWEEN_EACH_USER + randint(4, 11))


def extractDataWithInstagramy(usernames):
    isFirstTime = False

    if len(usernames[len(usernames) - 1]) == 0:
        usernames.pop()

    for i in range(0, 10):  # len(usernames) - 1
        User = usernames[i]
        Delay = var.DELAY_BETWEEN_EACH_USER + randint(3, 8)

        if i == 0:
            isFirstTime = True
        else:
            isFirstTime = False

        userInfo = get_userInfo(User)[
            'entry_data']['ProfilePage'][0]['graphql']['user']

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
        getFollowers(userInfo['id'],
                     userInfo['edge_followed_by']['count'], 100)

        # edge_owner_to_timeline_media = []
        # edge_felix_video_timeline = []

        # if userInfo.edge_felix_video_timeline.page_info.has_next_page == False:
        #     videos_posts = userInfo.edge_felix_video_timeline.edges
        #     # for
        print(f"Scraping Successful for user: {User}")
        sleep(Delay)
        # break


# TODO: Create Progress Bar, getPosts, getComments, getFollowers, and getFollowing.

if __name__ == "__main__":
    try:
        # usernames = readInputFile()
        # usernames = usernames.split("\n")
        # extractDataWithInstagramy(usernames)
        getFollowers("6048734544", 3848, 100)
    except Exception as e:
        print(e)
