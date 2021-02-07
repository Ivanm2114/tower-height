from math import cos, radians
def delta(toponym):
    also = toponym['boundedBy']['Envelope']
    upper_corn = list(map(float, also['upperCorner'].split()))
    lower_corn = list(map(float, also['lowerCorner'].split()))
    delta = str((((upper_corn[0] - lower_corn[0]) ** 2 + ((upper_corn[0] - lower_corn[0]) ** 2)) ** 0.5)/4)
    return delta


def count_dist(address_ll, org_point):
    point = (float(address_ll.split()[1]) + float(org_point.split()[1])) / 2
    a = abs(float(address_ll.split()[0]) - float(org_point.split()[0])) * 111000 * cos(radians(point))
    b = abs(float(address_ll.split()[1]) - float(org_point.split()[1])) * 111000
    dist = (a**2 + b**2) ** 0.5
    return dist


def get_coords(place):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={place}&format=json"
    response = requests.get(geocoder_request)
    
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Печатаем извлечённые из ответа поля:
        return toponym_coodrinates
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")

