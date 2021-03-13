import os
import sys
import urllib


def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


# takes a url and downloads image from that url
def image_downloader(img_links, folder_name):
    """
    Download images from a list of image urls.
    :param img_links:
    :param folder_name:
    :return: list of image names downloaded
    """
    img_names = []

    try:
        parent = os.getcwd()
        try:
            folder = os.path.join(parent, folder_name)
            create_folder(folder)
            os.chdir(folder)
        except Exception:
            print("Error in changing directory.")

        for link in img_links:
            img_name = "None"

            if link != "None":
                img_name = (link.split(".jpg")[0]).split("/")[-1] + ".jpg"
                try:
                    urllib.request.urlretrieve(link, img_name)
                except Exception:
                    img_name = "None"

            img_names.append(img_name)

    except Exception:
        print("Exception (image_downloader):", sys.exc_info()[0])
    finally:
        os.chdir(parent)
    return img_names


# -------------------------------------------------------------