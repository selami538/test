import requests
from flask import Flask, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/<m3u8>')
def index(m3u8):
    # URL manipülasyonları
    m3u8 = request.url.replace('__', '/')
    source = m3u8
    source = source.replace('https://sea-lion-app-mx8cy.ondigitalocean.app/', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    
    videoid = request.args.get("videoid")
    
    # videoid parametresi kontrolü
    if not videoid:
        return "Error: videoid is required", 400  # 400 Bad Request hatası döndür

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q=0.9",
        "origin": "https://www.apiredirect.buzz",
        "referer": "https://www.apiredirect.buzz/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    # Kaynağa GET isteği yapıyoruz
    ts = requests.get(source, headers=headers)
    
    if ts.status_code != 200:
        return "Error: Unable to fetch source", 500  # Eğer kaynağa ulaşılamazsa hata döndür
    
    tsal = ts.text
    
    # videoid ile segment URL'lerini güncelle
    tsal = tsal.replace(videoid + '_', 'https://sea-lion-app-mx8cy.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/' + videoid + '_')
    
    if "internal" in tsal:
        tsal = tsal.replace('internal', 'https://sea-lion-app-mx8cy.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/internal')
    
    if "segment" in tsal:
        tsal = tsal.replace('\n' + 'media', '\n' + 'https://sea-lion-app-mx8cy.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/media')
    
    return tsal


@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    source = request.url
    source = source.replace('https://sea-lion-app-mx8cy.ondigitalocean.app/getm3u8?source=', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    
    videoid = request.args.get("videoid")
    
    # videoid parametresi kontrolü
    if not videoid:
        return "Error: videoid is required", 400  # 400 Bad Request hatası döndür

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q=0.9",
        "origin": "https://www.maltinok.com",
        "referer": "https://www.maltinok.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    # Kaynağa GET isteği yapıyoruz
    ts = requests.get(source, headers=headers)
    
    if ts.status_code != 200:
        return "Error: Unable to fetch m3u8 source", 500  # Eğer kaynağa ulaşılamazsa hata döndür
    
    tsal = ts.text
    
    # videoid ile segment URL'lerini güncelle
    tsal = tsal.replace(videoid + '_', 'https://sea-lion-app-mx8cy.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/' + videoid + '_')
    
    return tsal


@app.route('/getstream', methods=['GET'])
def getstream():
    param = request.args.get("param")
    
    if param == "getts":
        source = request.url
        source = source.replace('https://sea-lion-app-mx8cy.ondigitalocean.app/getstream?param=getts&source=', '')
        source = source.replace('%2F', '/')
        source = source.replace('%3F', '?')
        
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'tr-TR,tr;q=0.9',
            'origin': 'https://www.apiredirect.buzz',
            'referer': 'https://www.apiredirect.buzz/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        
        # Kaynağa GET isteği yapıyoruz
        ts = requests.get(source, headers=headers)
        
        if ts.status_code != 200:
            return "Error: Unable to fetch stream", 500  # Eğer kaynağa ulaşılamazsa hata döndür
        
        return ts.content
    
    if param == "getm3u8":
        videoid = request.args.get("videoid")
        
        # videoid parametresi kontrolü
        if not videoid:
            return "Error: videoid is required", 400  # 400 Bad Request hatası döndür

        veriler = {
            "AppId": "3",
            "AppVer": "1025",
            "VpcVer": "1.0.12",
            "Language": "tr",
            "Token": "",
            "VideoId": videoid
        }

        r = requests.post("https://1xlite-900665.top/cinema", json=veriler)
        
        if r.status_code != 200:
            return "Error: Unable to fetch m3u8 data", 500  # Eğer kaynağa ulaşılamazsa hata döndür
        
        if "FullscreenAllowed" in r.text:
            veri = r.text
            veri = re.findall('"URL":"(.*?)"', veri)
            
            if veri:
                veri = veri[0].replace("\/", "__")
                veri = veri.replace('edge3', 'edge10').replace('edge100', 'edge10').replace('edge4', 'edge10').replace('edge2', 'edge10')
                veri = veri.replace('edge5', 'edge10').replace('edge1', 'edge10').replace('edge6', 'edge10').replace('edge7', 'edge10')
                veri = veri.replace(':43434', '')
                
                if "m3u8" in veri:
                    return "https://sea-lion-app-mx8cy.ondigitalocean.app/" + veri + '&videoid=' + videoid
        else:
            return "Error: No data found", 404  # Eğer veri bulunmazsa 404 döndür

    return "Error: Invalid parameter", 400  # Eğer parametre geçersizse 400 döndür


if __name__ == '__main__':
    app.run()
