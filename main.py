from uvicorn import run
from fastapi import FastAPI, Response
import requests
import requests_cache
import requests_random_user_agent

requests_cache.install_cache("insta_cache", backend='sqlite', expire_after=60*60*24*30, match_headers=False, cache_control=False)

# ========================== scraping the data ========================== 
def UserInfo(user_name: str) -> dict:
    reqUrl = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}"

    headersList = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.6",
                    "cookie": "ig_did=E0E9A21C-A45A-46DC-8911-5E199137F8B0; ig_nrcb=1; dpr=1.25; csrftoken=D6zBG6I6Vry5jGV67rEDSLkGsCUZyCEa; mid=Y61aPwALAAFW05FCaBCy7rRlKZA8; datr=PFqtYzrYYjq11_466YXZsaUo",
                    "referer": f"https://www.instagram.com/{user_name}/",
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
    description="This is simple instagram scraping API developed by Vijay Raghuwanshi",
    copyright="ervijayraghuwanshigmai.com",
    version="0.0.1",
    docs_url="/"

)

@app.get("/getUserInfo/{user_name}", description="Get the user info of Instagram user by it's name like \"gima_ashi\"", tags=["Instagram"])
def read_root(response: Response,user_name):
    info, is_from_cache = UserInfo(user_name=str(user_name).strip())
    response.headers["from-cache"] = str(is_from_cache)
    
    return {"message": info}


if __name__ == "__main__":
    # import webbrowser
    # webbrowser.open("http://127.0.0.1:5500")
    run(app, host="127.0.0.1", port=5500)
