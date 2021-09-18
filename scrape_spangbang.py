import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_playlist(soup):
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

def download_mp4(file, url):
    with open(file, 'wb') as saveFile:
        # ファイルサイズ取得
        if requests.head(url).status_code == 302 :
            file_size = int(requests.head(url).headers["content-length"])
            pbar = tqdm(total=file_size, unit="B", unit_scale=True)
            # チャンクダウンロード
            for chunk in requests.get(url, stream=True).iter_content(chunk_size=1024):
                ff = saveFile.write(chunk)
                pbar.update(len(chunk))
            pbar.close()

url = input("Search: ")

r = requests.get(url).text
soup = BeautifulSoup(r, 'lxml')

video_urls = []

# 詳細画面
for video_info in scrape_playlist(soup):
    r = requests.get(video_info['url']).text
    soup = BeautifulSoup(r, 'lxml')
    # videoタグのsrcからvideoをダウンロード
    try:
        video_url = soup.video.source['src']
        if video_url is not None:
            download_mp4(f'./{video_info["title"]}.mp4', video_url)
    except:
        print(f'No videos found for: {video_info["title"]}')
