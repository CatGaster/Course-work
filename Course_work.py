import json
import requests


app_id = 51774439
vk_oauth_url = "https://oauth.vk.com/authorize"
params_dict = {
    "client_id": app_id,
    "redirect_uri": "https://oauth.vk.com/blank.html",
    "display": "page",
    "scope": "photos",
    "response_type": "token",
}

token = ""


class VKAPIClient:

    '''
    Класс для работы с API ВК, получение фотографий со страницы профиля
    '''

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

    def get_count(self, count):
        self.count = count

    def get_rev(self, rev):
        self.rev = rev

    def get_photos(self):
        method_params = self.common_params()
        method_params.update({"owner_id": self.user_id, "count": self.count,
                              "rev": self.rev, "album_id": "profile", "extended": "likes",
                              "photo_sizes": "o", })
        response = requests.get(f"{self.api_url}photos.get", params=method_params).json()
        return response


class YandexDiskAPI:

    '''
    Класс для работы с Яндекс.Диском, создание папок и загрузка на диск
    '''

    def __init__(self, y_token):
        self.y_token = y_token

    def get_headers(self):
        return {
            "Authorization": self.y_token
        }

    def name_folder(self):
        return {
            "path": "VK_image"
        }

    def param(self, params):
        self.params = params

    def create_folder(self):
        return requests.put("https://cloud-api.yandex.net/v1/disk/resources", 
                            headers = self.get_headers(), params = self.name_folder())

    def resource_upload(self):
        response = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload",
                                headers=self.get_headers(), params=self.params)
        url = response.json().get("href")
        return url


def upload():

    ''' Функция для скачивания фотографий из VK с помощью API и отправки на Яндекс Диск

    используя OAuth токен VK и указанный id пользователя VK в качестве параметров,
    сохраняет выбранное колличество фотографий
    Используя Яндекс OAuth токен пользователя, создает папку VK_image на Яндекс диске пользователя
    и сохраняет на него полученные из VK фотографии в формате jpg
    создаёт json файл с перечнем загруженных фотографий
    '''

    client = VKAPIClient(token, input("Введите VK id : "))
    yandex_disk = YandexDiskAPI(input("Введите YandexDisk OAuth token : "))

    response = yandex_disk.create_folder()
    if response.status_code == 201:
        print(f"Создана Папка{yandex_disk.name_folder()['path']} на вашем Яндекс диске")
    else:
        print("Папка уже существует или произолша иная ошибка: ", response.status_code)

    client.get_rev(int(input("Введите Порядок поиска (0 Хронологический) (1 Антихронологический) : ")))
    client.get_count(int(input("Введите количество фото : ")))

    json_save_photos = {"photos": []}

    for photo in client.get_photos()["response"]["items"]:
        vk_save_photo = photo["sizes"][-1]["url"]
        like = (f"{photo["likes"]["count"]} like ")
        id_ = (f'{photo["id"]} id фото')

        with open("vk_save_photo.json", "w") as file:
            json.dump(vk_save_photo, file)

        with open("vk_save_photo.json", "r") as file:
            vk_save_photo = json.load(file)
            response = requests.get(vk_save_photo)

        with open(like + id_ + ".jpg", "wb") as f1:
            f1.write(response.content)

        yandex_disk.param({"path": "VK_image/" + like + id_ + ".jpg"})
        with open(like + id_ + ".jpg", "rb") as file:
            response = requests.put(
                yandex_disk.resource_upload(), files={"file": file})

        print(vk_save_photo, like, id_)
        json_save_photos["photos"].append(vk_save_photo)

    with open("vk_save_photo.json", "w") as file:
        json.dump(json_save_photos, file)


if __name__ == "__main__":
    upload()
