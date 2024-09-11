import re

stopword = ['기자', 'com', '.co', '저작권', '무단', '전재', '재배포', 'Copyr', 'copyr', '경향비즈', '영상', '취재', '편집', '문의', '금지', '특파원', '아이뉴스', '한경', '뉴스', '보도합니다']

# 문장내 <>, [], 구문 제거(앞뒤 공백 제거 포함)
def cleansing(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    return text.strip()

# ASCII 범위를 벗어나는 특수문자들을 제거
def remove_except_ascii(text):
    # \x20-\x7E : ASCII 문자 중 키보드에서 입력할 수 있는 문자(공백 포함)
    return re.sub(r'[^\x20-\x7E]', ' ', text)

# 단어별 처리 함수
def process_words(words, del_words, stopwords):
    processed_words=[]
    for word in words:
        if word == '기자':
            if processed_words:
                processed_words.pop()
            continue
        
        if any(del_word in word for del_word in del_words):
            continue

        if '@' in word:
            continue
        # word = re.sub(r'\d+','', word)
        word = re.sub(r'[^\w\s.]','', word)
        
        if re.search('[a-zA-Z]', word):
            word = word.lower()
        
        for stopword in stopwords:
            if word.endswith(stopword):
                word = word[:-len(stopword)]
        
        if len(word) <= 1:
            continue
                
        if word:
            processed_words.append(word)
    return processed_words