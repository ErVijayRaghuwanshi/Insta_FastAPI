from uvicorn import run
from fastapi import FastAPI
import requests


app = FastAPI(
    title="Instagram FastAPI",
    description="This is simple instagram scraping API developed by Vijay Raghuwanshi",
    copyright="ervijayraghuwanshigmai.com",
    version="0.0.1",
    docs_url="/"

)

@app.get("/getUserInfo/{user_name}", description="Get the user info of Instagram user by it's name like \"gima_ashi\"", tags=["Instagram"])
def read_root(user_name):
    data = {}

    reqUrl = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}"
    headersList = {
    "x-ig-app-id": "936619743392459" 
    }
    try:
        response = requests.get(reqUrl, headers=headersList)
        if response.ok:
            data = response.json()
        else:
            data = {"message": f"invalid user_name: {user_name}", "status_code": response.status_code}
    except Exception as e:
        data = {"message": "error", "exception": str(e)}

    return {"message": data}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0")
