import tkinter as tk
from tkinter import scrolledtext
import os

from news import News


# 뉴스 기사 입력 후 버튼 클릭 시 관련 기사를 출력하는 함수
def on_generate_articles():
    news_text = news_entry.get("1.0", tk.END).strip()
    
    # 뉴스 기사를 입력했을 때 관련 기사를 생성
    if news_text:
        related1, related2 = news.recommend_articles(news_text).values()
        
        # 관련기사1과 관련기사2를 각각의 텍스트 위젯에 출력
        in_related.delete("1.0", tk.END)  # 기존 내용을 지우고 새로 출력
        cross_related.delete("1.0", tk.END)
        
        for article in related1:
            in_related.insert(tk.END, article + "\n")
        
        for article in related2:
            cross_related.insert(tk.END, article + "\n")
    else:
        # 뉴스 기사가 입력되지 않았을 경우 경고
        in_related.delete("1.0", tk.END)
        cross_related.delete("1.0", tk.END)
        in_related.insert(tk.END, "뉴스 기사를 입력하세요.")
        cross_related.insert(tk.END, "뉴스 기사를 입력하세요.")

# News 불러오기
data_path = os.path.join("D:\python_project\sesac02\data", 'similarity_data_3m.csv')
news = News(data_path)
print(news.df.head(5))

# 메인 윈도우 생성
window = tk.Tk()
window.title("연관 뉴스 추천")
window.geometry("960x500+100+100")
# window.resizable(False, False)

# 안내
label=tk.Label(window, text="뉴스 URL을 입력하세요.")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# 뉴스 기사 입력 창 (스크롤 가능하게 설정)
news_entry = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=10)
news_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# 버튼: 관련기사 생성
generate_button = tk.Button(window, text="관련기사 찾기!", command=on_generate_articles)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

# 관련기사1 표시 창 (왼쪽 아래)
in_related_label = tk.Label(window, text="카테고리 내 관련 기사")
in_related_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

in_related = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=10)
in_related.grid(row=4, column=0, padx=10, pady=5)

# 관련기사2 표시 창 (오른쪽 아래)
cross_related_label = tk.Label(window, text="다른 카테고리의 관련 기사")
cross_related_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

cross_related = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=10)
cross_related.grid(row=4, column=1, padx=10, pady=5)

# 메인 루프 시작
window.mainloop()
