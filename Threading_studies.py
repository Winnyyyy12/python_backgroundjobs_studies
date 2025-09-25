import os
import threading

import requests


def download_file(url):
    local_filename = url.split('/')[-1]
    os.makedirs("downloads", exist_ok=True)
    print(f"Starting download of {local_filename} from {url}")
    response = requests.get(url)
    with open(os.path.join("downloads", local_filename), 'wb') as f:
        f.write(response.content)
        print(f"Finished download of {local_filename}")


urls = [
    "https://images.pexels.com/photos/19321355/pexels-photo-19321355.jpeg",
    "https://images.pexels.com/photos/33423804/pexels-photo-33423804.jpeg",
    "https://cdn.artstation.com/p/video_sources/002/841/622/motel-concept-video-the-rainmaker.mp4"
]

threads = []
for url in urls:
    threads.append(threading.Thread(target=download_file, args=(url,)))


for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
print("All downloads completed!")
