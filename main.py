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
                    "x-ig-app-id": "936619743392459",
                }

    payload = f"username={user_name}"
    try:
        resp = requests.get(reqUrl, data=payload,  headers=headersList)
        from_cache = resp.from_cache
        if resp.ok:
            data = resp.json()
        else: 
            data = {"message": f"invalid user_name: {user_name}"}
    except Exception as e:
        data = {"message": f"invalid user_name: {user_name}", "error": str(e)}
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
