import requests, sys
import ssl,json
import base64,urllib


# client_id 为官网获取的AK， client_secret 为官网获取的SK

def get_access_token():

    URL = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=pQr27gTvrqnInrsVFycZTulH&client_secret=GrDWR7PGKhheQgfwpYaPxb2P5GvGddBi'
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.post(URL, headers=header)
    if (response):
        access_token = json.loads(response.text)['access_token']

    return access_token

def identify_face(access_token, img):

    URL = "https://aip.baidubce.com/rest/2.0/face/v3/search" + "?access_token=" + access_token
    params = {'image': img, 'image_type': 'BASE64', 'group_id_list': 'admin,user'}
    header = {'Content-Type': 'application/json'}
    response = requests.post(URL, headers=header, data=params)
    if response:
        print(response.text)
        result = json.loads(response.text)
    return result


if __name__ == '__main__':

    access_token =get_access_token()
    f = open('D:\\TempData\\微信图片_20190225221854.jpg', 'rb')
    img = base64.b64encode(f.read())
    result = identify_face(access_token, img)
    print(result['error_msg'])