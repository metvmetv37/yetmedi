import subprocess
import os

def get_stream_url(channel_id):
    # yt-dlp kullanarak canlı yayın linkini al
    # Not: Bazı durumlarda bot korumasını aşmak için çerez gerekebilir
    try:
        url = f"https://www.youtube.com/{channel_id}/live"
        result = subprocess.run(
            ['yt-dlp', '-g', '-f', 'best[protocol^=m3u8]', url],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Hata: {channel_id} -> {e}")
        return None

def main():
    m3u8_content = "#EXTM3U\n"
    
    if not os.path.exists('youtubeLink.txt'):
        print("youtubeLink.txt bulunamadı!")
        return

    with open('youtubeLink.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if not line.strip() or '||' not in line:
            continue
        
        parts = line.split('||')
        name = parts[0].strip()
        channel_id = parts[1].strip()
        group = parts[2].strip() if len(parts) > 2 else "Genel"

        print(f"İşleniyor: {name}...")
        stream_url = get_stream_url(channel_id)
        
        if stream_url:
            m3u8_content += f'#EXTINF:-1 group-title="{group}",{name}\n{stream_url}\n'
            print(f"Başarılı: {name}")
        else:
            print(f"Atlandı: {name} (Yayında değil veya hata var)")

    with open('youtube.m3u8', 'w', encoding='utf-8') as f:
        f.write(m3u8_content)
    print("youtube.m3u8 güncellendi.")

if __name__ == "__main__":
    main()
