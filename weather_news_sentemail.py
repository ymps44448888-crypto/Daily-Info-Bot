import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

API_KEY = "請填入你的_API_KEY"

# 抓取天氣
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=25.01&longitude=121.46&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FTaipei"
    
    response = requests.get(url) 
    data = response.json()       

    # 抓取今天(第0筆)
    max_temp = data['daily']['temperature_2m_max'][0]
    min_temp = data['daily']['temperature_2m_min'][0]
    rain_prob = data['daily']['precipitation_probability_max'][0]
    
    return f"板橋區今日最低溫: {min_temp}°C，最高溫: {max_temp}°C，下雨機率: {rain_prob}%"

# 抓取新聞
def get_news():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # 台灣與國際新聞
    url_tw = f"https://newsapi.org/v2/everything?q=台灣&from={yesterday}&sortBy=popularity&pageSize=5&language=zh&apiKey={API_KEY}"
    data_tw = requests.get(url_tw).json()
    tw_news = data_tw['articles']
    
    url_int = f"https://newsapi.org/v2/everything?q=國際&from={yesterday}&sortBy=popularity&pageSize=5&language=zh&apiKey={API_KEY}"
    data_int = requests.get(url_int).json()
    int_news = data_int['articles']

    all_articles = int_news + tw_news
    
    final_report = "--- 今日重點新聞 ---\n1-5國際新聞 6-10台灣新聞\n\n"
    
    count = 1
    for art in all_articles:
        title = art['title']
        
        # 確保新聞有提供摘要
        if 'description' in art and art['description'] != None:
            desc = art['description'][:150] # 擷取前150個字
        else:
            desc = "無提供摘要"
            
        final_report += f"{count}. {title}:\n        摘要: {desc}...\n\n"
        count += 1

    return final_report

# 寄送email
def sent_email(context):
    sender = "填寫寄出者的Gmail"
    pw = "請填入寄出者的Google應用程式密碼"
    to_sender = "填寫收信者的Gmail"
    
    # 設定信件內容與標題
    msg = MIMEText(context)
    msg['Subject'] = "每日天氣與新聞摘要"
    msg['From'] = sender
    msg['To'] = to_sender

    # 建立伺服器連線、登入、寄信、手動登出
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, pw)
    server.send_message(msg)
    server.quit() # 必須手動關閉連線
    
    print("郵件已成功寄出！")

# 執行
weather = get_weather()
news = get_news()
full_message = f"{weather}\n\n{news}"
sent_email(full_message)