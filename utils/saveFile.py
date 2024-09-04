import pandas as pd
import os


SAVE_DIRECTORY = 'D:\python_project\sesac02\data'

def save_mat2DF(mat: list, columns: list, file_name: str):
    df = pd.DataFrame(mat, columns=columns)
    file_path = os.path.join(SAVE_DIRECTORY, file_name)
    save_DF(df, file_path=file_path)
    return

def save_DF(df: pd.DataFrame, file_path: str):
    # 최초 생성 이후 mode는 append
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, mode='w')
        print(f"Write {len(df)}개 in {file_path}")
    else:
        df.to_csv(file_path, index=False, mode='a', header=False)
        print(f"Add {len(df)}개 in {file_path}")
    return
