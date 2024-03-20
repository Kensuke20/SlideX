from PIL import Image
from datetime import datetime

def save_photo(new_file):
    fname = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    file_path = './static/images/' + fname

    new_file.save(file_path)

    return file_path


def bmp2jpg(bmp_urls):
    for bmp_url in bmp_urls:
        space, name, extension = bmp_url.split(".")
        bmp_img = Image.open(bmp_url)
        bmp_img.convert("RGB").save('.' + name + 'converted.jpg', "JPEG")

        # with Image.open(bmp_url) as img:
        #     # 拡張メタデータを取得
        #     exif_data = img.info.get('exif')
        #     if exif_data:
        #         # Exif情報から作成日時を抽出
        #         exif_creation_time = exif_data.get(36867)
        #         if exif_creation_time:
        #             print(datetime.strptime(exif_creation_time, "%Y:%m:%d %H:%M:%S"))
        #         else:
        #             print("not exist exif")
        #     else:
        #         print("not exist meta")


    return