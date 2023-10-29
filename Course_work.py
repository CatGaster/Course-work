import json
import requests
import yadisk


app_id=51774439
vk_oauth_url= "https://oauth.vk.com/authorize"
params_dict={
    "client_id": app_id,
    "redirect_uri": "https://oauth.vk.com/blank.html",
    "display": "page",
    "scope": "photos",
    "response_type": "token",
}
token = ""


class VKAPIClient:
    
    api_url = "https://api.vk.com/method/"

    def __init__(self, token, user_id):
        self.access_token = token
        self.user_id = user_id

    def common_params(self):
        return {
        "access_token": self.access_token,
        "v": "5.154",
        "user_id": self.user_id,
        }

    def get_photos(self,):
        method_params = self.common_params()
        method_params.update({"owner_id": self.user_id, "count": self.count,
                            "rev": self.rev, "album_id": "profile", "extended": "likes",
                            "photo_sizes": "o", })
        response = requests.get(f"{self.api_url}photos.get", params=method_params).json()
        return response
    
    def get_count(self,count):
        self.count = count
        method_params = self.common_params()
        method_params.update({"count": self.count})
        
    def get_rev(self,rev):
        self.rev = rev
        method_params = self.common_params()
        method_params.update({"rev": self.rev})

        
def upload():
        
    client = VKAPIClient(token,input("Введите VK id : "),)
    y_token = input("Введите Яндекс OAuth Токен: ")

    client.get_rev(int(input("Введите Порядок (0 Хронологический) (1 Антихронологический) : ")))
    client.get_count(int(input("Введите количество фото : ")))
    for photo in client.get_photos()["response"]["items"]:
        vk_save_photo = photo["sizes"][-1]["url"]
        like = f"{photo["likes"]["count"]} like "
        id_=f'{photo["id"]} id фото;'

        with open("vk_save_photo.json", "w") as file:
            json.dump(vk_save_photo, file)
    
        with open("vk_save_photo.json", "r") as file:
            vk_save_photo = json.load(file)
            response= requests.get(vk_save_photo)

            with open(like + id_ + ".jpg","wb") as f1:
                f1.write(response.content)

            yandex_token = yadisk.YaDisk(token = y_token)
            yandex_token.upload(like + id_ +".jpg", like + id_ +".jpg")
            
            print(vk_save_photo, like, id_)

if __name__ == "__main__":
    upload()