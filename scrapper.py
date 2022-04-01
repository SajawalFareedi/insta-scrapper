import instagramy as insta

import requests
from urllib.request import Request, urlopen

import json
import csv
import pandas as pd

from time import sleep
from random import randint

from config.variables import Variables
from config.urls import Urls

var = Variables()
org_proxy = {
    "http": "http://rynym:aNaPEHnJDW4gma4u@54.81.215.168:31112",
    "https": "https://rynym:aNaPEHnJDW4gma4u@54.81.215.168:31112"
}


def getProxy():
    r = requests.get(var.PROXY_SERVER_URL)
    return {
        "http": f"http://{r.text}",
        "https": f"https://{r.text}"
    }


proxy = getProxy()
proxy_host = proxy["http"].split("//")[1]


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
    # userDataJSON = json.dumps(userData)
    userDataAoA = dictToAoA(userData, isFirstTime)
    # dataFrame = pd.read_json(userDataJSON, typ='series')
    # userData_CSV = dataFrame.to_csv()
    # userData_CSV = ''
    if isFirstTime == True:
        with open(var.USERINFO_FILE, mode="w+", encoding="utf8", newline='') as usersInfoFile:
            writer = csv.writer(usersInfoFile, delimiter=',')
            writer.writerows(userDataAoA)
            return

    with open(var.USERINFO_FILE, mode="a", encoding="utf8", newline='') as usersInfoFile:
        usersInfoFile.write(userDataAoA)
        usersInfoFile.close()


def get(url, headers={}):
    # headers = {
    #     # "authority": "i.instagram.com",
    #     # "accept": "*/*",
    #     # "accept-language": "en-US,en;q=0.9,nl;q=0.8,he;q=0.7",
    #     "cookie": "sessionid=",
    #     # "dnt": "1",
    #     # "origin": "https://www.instagram.com",
    #     # "referer": "https://www.instagram.com/",
    #     # "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    #     # "sec-ch-ua-mobile": "?0",
    #     # "sec-ch-ua-platform": '"Windows"',
    #     # "sec-fetch-dest": "empty",
    #     # "sec-fetch-mode": "cors",
    #     # "sec-fetch-site": "same-site",
    #     "user-agent": "Googlebot/2.1 (+http://www.googlebot.com/bot.html)",
    #     # x-asbd-id: 198387
    #     # x-ig-app-id: 936619743392459
    #     # x-ig-www-claim: hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYHbC
    # }
    # r = requests.get(url=url, headers=headers,
    #                  verify=False)  # proxies=org_proxy
    # print(r.text)
    # return r.text if r.status_code == 200 else r.headers
    request = Request(
        url=url, headers={
            "User-Agent": 'user-agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"'}
    )
    request.add_header("Authority", "authority: i.instagram.com")
    request.add_header("dnt", "dnt: 1")
    request.add_header("origin", "origin: https://www.instagram.com")
    request.add_header("referer", "referer: https://www.instagram.com/")
    request.add_header(
        "sec-ch-ua", 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"')
    request.add_header("sec-ch-ua-mobile", "sec-ch-ua-mobile: ?0")
    request.add_header("sec-ch-ua-platform", 'sec-ch-ua-platform: "Windows"')
    request.add_header("sec-fetch-dest", "sec-fetch-dest: empty")
    request.add_header("sec-fetch-mode", "sec-fetch-mode: cors")
    request.add_header("sec-fetch-site", "sec-fetch-site: same-site")
    request.add_header("Accept", "accept: */*")
    request.add_header("Cookie", '')
    request.add_header("x-asbd-id", "x-asbd-id: 198387")
    request.add_header("x-ig-app-id", "x-ig-app-id: 936619743392459")
    request.add_header(
        "x-ig-www-claim", "x-ig-www-claim: hmac.AR1XVfLthoJcGua0kPRgkBRzVvg8OG6uhaQndtxIfRZNYHbC")
    # request.set_proxy(proxy_host, "http")
    with urlopen(request) as response:
        html = response.read()

    return html.decode("utf-8")


def getFollowers(User, totalCount, maxCount):
    # page_count = round((totalCount/maxCount) + 1)
    url = Urls(User, totalCountToFetchAtOnce=maxCount).generateUrl("followers")
    followers = get(url)
    print(followers)
    # print(followers)
    # for i in range(page_count):
    #     pass


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
        getFollowers(userInfo['id'], 50)

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
    # usernames = readInputFile()
    # usernames = usernames.split("\n")
    # extractDataWithInstagramy(usernames)
    # getFollowers("0000000000", 100)
    getFollowers("2504145151", 3638, 12)
