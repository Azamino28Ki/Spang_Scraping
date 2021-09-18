import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_video_info(soup):
    video_infos = []
    for item in soup.find_all('div', attrs={'data-id':True}, class_='video-item', id=True):

        try:
            full_video = item.find("a", class_='thumb')['href']
        except:
            print(f'No videos found for:')

        # sometimes /category/ shows up
        # which isn't a video link.
        if "/category/" in full_video:
            continue

        # cba to find the proper title from html
        # note that this may not always give proper title
        title = full_video.split('/')[3].replace('+', ' ')

        prev = item.picture.img
        # sometimes preview image or preview video
        # won't load for whatever reason.
        try:
            prev_vid = prev['data-preview']
            image = prev['data-src']
        except:
            prev_vid = "Not Found"
            image = "Not Found"
        
        video_infos.append({
            'title': title,
            'thumbnail': 'image',
            'preview_video': 'prev_vid',
            'url': f'https://spankbang.com{full_video}',
        })

    return video_infos

url = input("Search: ")

r = requests.get(url).text
soup = BeautifulSoup(r, 'lxml')

print(scrape_video_info(soup))

video_urls = []

for video_info in scrape_video_info(soup):
    r = requests.get(video_info['url']).text
    soup = BeautifulSoup(r, 'lxml')

    try:
        video_url = soup.video.source['src']
        if video_url is not None:
            video_urls.append(video_url)
    except:
        print(f'No videos found for: {video_info["title"]}')

for i, url in enumerate(video_urls, 1):
    response = requests.get(url)
    with open(f'./test_{i}.mp4', 'wb') as saveFile:
        # ファイルサイズ取得
        if requests.head(video_url).status_code == 302 :
            video_url = requests.head(video_url).headers["Location"]
        file_size = int(requests.head(video_url).headers["content-length"])
        pbar = tqdm(total=file_size, unit="B", unit_scale=True)
        # チャンクダウンロード
        for chunk in requests.get(url, stream=True).iter_content(chunk_size=1024):
            ff = saveFile.write(chunk)
            pbar.update(len(chunk))
        pbar.close()