# from uvicorn import run
from fastapi import FastAPI, Response
import requests
import requests_cache
import requests_random_user_agent
import os
from deta import Deta

# deta = Deta(os.getenv())
# create and use as many Drives as you want!
# insta_cache = deta.Drive("cache")
requests_cache.install_cache("insta_cache", backend='sqlite', expire_after=60*60*24, match_headers=False, cache_control=False)

# ========================== scraping the data ========================== 
def UserInfo(user_name: str) -> dict:
    reqUrl = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}"

    headersList = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.6",
                    "cookie": "ig_did=B53E4A33-B794-45BF-9256-502AE69A49AE; ig_nrcb=1; dpr=1.25; csrftoken=SmW4ETW22IVvjTwCao7A1UsAObL7xGQu; mid=Y4svWQALAAE1lXoDKjKaO06NFmAF",
                    "referer": "https://www.instagram.com/gima_ashi/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "sec-gpc": "1",
                    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "x-asbd-id": "198387",
                    "x-csrftoken": "SmW4ETW22IVvjTwCao7A1UsAObL7xGQu",
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "0",
                    "x-instagram-ajax": "1006680707",
                    "x-requested-with": "XMLHttpRequest" 
                }

    payload = f"username={user_name}"
    resp = requests.get(reqUrl, data=payload,  headers=headersList)
    from_cache = resp.from_cache
    data = resp.json()
    # return response.json()
    
    return data, from_cache
# ========================== scraping the data ========================== 

app = FastAPI(
    title="Instagram FastAPI",
    description="This is simple instagram scraping API developed by Ritik Verma",
    copyright="gritikverma331@gmai.com",
    version="0.0.1",
    docs_url="/"

)

@app.get("/getUserInfo/{user_name}", description="Get the user info of Instagram user by it's name like \"gime_ashi\"", tags=["Instagram"])
def read_root(response: Response,user_name):
    info, is_from_cache = UserInfo(user_name=str(user_name).strip())
    response.headers["from-cache"] = str(is_from_cache)
    
    return {"message": info}


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5500")
#     run(app, host="127.0.0.1", port=5500)