import requests
import json
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

# oauth_url = f'{vk_oauth_url}?{urlencode(params_dict)}'
token = "vk1.a.CZ-1CakxnwPv23oPW3pQ6KoVX7jHTqoA0iSlJgkRMQRyeHLz_lSzZHQbfm2bxSdvVKvqaSnjmZhS_nsmkPgj7tvYG7fqAqrzkZQ-vTB_Kn9kyg7K8wug8SUZkavrgfbTAQ4h0qGTODDHqNfGhSjWa8-OETTsJiieFjKE3PIoaOhUyIi4pus-l72bvzs_mLfS"

class VKAPICLIENT:
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


    def get_photos(self,count=int(input("Введите количество фотографий(): ")), rev = int(input("Выберите порядок поиска (1 антихронологический) (0 хронологический): "))):
        self.count=count
        self.rev= rev
        method_params = self.common_params()
        method_params.update({"owner_id": self.user_id,"count": self.count, "album_id": "profile", "extended": "likes","rev": self.rev, "photo_sizes": "o", })
        response = requests.get(f"{self.api_url}photos.get", params=method_params).json()
        # print (len(response["response"]["items"]))
        return response

client = VKAPICLIENT(token, int(input("Введите VK id : ")))
y_token = input("Введите Яндекс OAuth Токен: ")

def Upload():

    for photo in client.get_photos()["response"]["items"]:
        vk_save_photo=photo["sizes"][-1]["url"]
        like = f"{photo["likes"]["count"]} like "
        id_=f'{photo["id"]} id фото;'

        with open ("vk_save_photo.json", "w") as file:
            json.dump(vk_save_photo, file)
    
        with open("vk_save_photo.json", "r") as file:
            vk_save_photo = json.load(file)
            response= requests.get(vk_save_photo)

            with open(like + id_ + ".jpg","wb") as f1:
                f1.write(response.content)

            Y_token=yadisk.YaDisk(token=y_token)
            Y_token.upload(like + id_ +".jpg", like + id_ +".jpg")
            
            print(vk_save_photo, like, id_)
Upload()
