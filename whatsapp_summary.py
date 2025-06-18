import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# === CONFIG ===
CHAT_FILE = "D:\\ML\\Whatsapp_Summarizer\\WhatsApp Chat with AIDS '28.txt"  # exported WhatsApp .txt file
KEYWORDS = ['assignment', 'exam', 'test', 'deadline']

# === 1. Parse WhatsApp Chat File ===
def parse_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2})[^\-]* - ([^:]+): (.+)$')

    for line in lines:
        match = pattern.match(line)
        if match:
            date, time, sender, message = match.groups()
            data.append([date, time, sender.strip(), message.strip()])
    return pd.DataFrame(data, columns=['Date', 'Time', 'Sender', 'Message'])

# === 2. Analyze Data ===
def analyze(df):
    print("🧾 Total messages:", len(df))
    print("\n📊 Top senders:")
    print(df['Sender'].value_counts().head(10))

    # Messages per date
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    daily_count = df.groupby('Date').size()

    plt.figure(figsize=(10, 4))
    daily_count.plot()
    plt.title("Messages Per Day")
    plt.xlabel("Date")
    plt.ylabel("Messages")
    plt.tight_layout()
    plt.show()

    # Top words (basic)
    all_words = ' '.join(df['Message'].str.lower()).split()
    common_words = Counter(all_words)
    print("\n📝 Top 10 common words:")
    print(common_words.most_common(10))

    # Word Cloud
    wc = WordCloud(width=800, height=300, background_color='white').generate(' '.join(df['Message']))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title("☁️ Word Cloud of Messages")
    plt.show()

    # Keyword mentions
    print("\n🔍 Keyword Mentions:")
    for kw in KEYWORDS:
        count = df['Message'].str.lower().str.contains(kw).sum()
        print(f"'{kw}': {count} times")

# === MAIN ===
if __name__ == '__main__':
    df_chat = parse_chat(CHAT_FILE)
    if df_chat.empty:
        print("⚠️ Could not parse chat file. Check format.")
    else:
        analyze(df_chat)
