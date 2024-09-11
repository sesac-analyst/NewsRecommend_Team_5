# 구글 코랩에서 실행 권장(gpu 권장)
# from transformers import BertModel, BertTokenizer
from kobert_transformers import get_tokenizer, get_kobert_model
import torch

import multiprocessing as mp
from io import StringIO
import pandas as pd
import numpy as np

from google.colab import files


def get_document_embedding(sentences:list):
    inputs = tokenizer(
        sentences,
        return_tensors='pt',
        padding=True,
        truncation=True
    )
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Get the sentence embeddings
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract the embeddings for the [CLS] token (shape: [batch_size, hidden_size])
    cls_embeddings = outputs.last_hidden_state[:, 0, :]
    
    # Pool the sentence embeddings to create a single document embedding by averaging
    document_embedding = torch.mean(cls_embeddings, dim=0)

    return document_embedding.cpu().numpy()

# 병렬화 위한 함수
def process_sentence(sentences):
    sentences = eval(sentences)  # Convert string to list
    return get_document_embedding(sentences)

# 멀티프로세싱 이용
def compute_embeddings_in_parallel(data, num_workers=4):
    with mp.Pool(processes=num_workers) as pool:
        # Use multiprocessing Pool to compute embeddings in parallel
        results = pool.map(process_sentence, data)
    return results


model = get_kobert_model()
tokenizer = get_tokenizer()

# 파일 불러오기
with open("/content/month_sample3.csv", encoding='utf-8') as f:
    contents = f.read()

cleaned_contents = contents.lstrip('\ufeff')
df = pd.read_csv(StringIO(cleaned_contents), index_col=0)

# df에서 문서행 추출
sam = df["clear_sentence_split"]

# worker 수 설정
num_workers = mp.cpu_count()  # This will use all available CPU cores

# 병렬 진행
vector_list = compute_embeddings_in_parallel(sam, num_workers=num_workers)

# 파일 저장
vector_list.to_csv('/content/embedded_data.csv')
files.download('/content/embedded.csv')

print("Complete")