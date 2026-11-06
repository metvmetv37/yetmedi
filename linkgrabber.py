import subprocess
import os

def get_stream_url(channel_id):
    try:
        if channel_id.startswith('@'):
            url = f"https://www.youtube.com/{channel_id}/live"
        else:
            url = f"https://www.youtube.com/channel/{channel_id}/live"

        # Çerez dosyasını (cookies.txt) kullanarak bot korumasını aşıyoruz
        result = subprocess.run(
            ['yt-dlp', '-g', '-f', 'best[protocol^=m3u8]', '--cookies', 'cookies.txt', url],
            capture_output=True, text=True, timeout=25
        )
        
        if result.returncode != 0:
            print(f"yt-dlp Hatası ({channel_id}): {result.stderr.strip()}")
            return None
            
        return result.stdout.strip()
    except Exception as e:
        print(f"İstisna ({channel_id}): {e}")
        return None

def main():
    m3u8_content = "#EXTM3U\n"
    
    if not os.path.exists('youtubeLink.txt'):
        print("HATA: youtubeLink.txt bulunamadı!")
        return

    with open('youtubeLink.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or '||' not in line:
            continue
        
        parts = line.split('||')
        name = parts[0].strip()
        channel_id = parts[1].strip()
        group = parts[2].strip() if len(parts) > 2 else "Genel"

        print(f"İşleniyor: {name} ({channel_id})...")
        stream_url = get_stream_url(channel_id)
        
        if stream_url:
            m3u8_content += f'#EXTINF:-1 group-title="{group}",{name}\n{stream_url}\n'
            print(f"BAŞARILI: {name}")
        else:
            print(f"BAŞARISIZ: {name}")

    with open('youtube.m3u8', 'w', encoding='utf-8') as f:
        f.write(m3u8_content)
    print("İşlem tamamlandı. youtube.m3u8 güncellendi.")

if __name__ == "__main__":
    main()
