import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_atplotlib

# 데이터 로드
file_path = '202406_202406_연령별인구현황_월간.csv'  # 파일 경로를 확인하세요
try:
    df = pd.read_csv(file_path, encoding='euc-kr')
except FileNotFoundError:
    st.error('데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요.')
    st.stop()

# 데이터 전처리
df = df.replace(',', '', regex=True)
try:
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)
except ValueError:
    st.error('데이터 형식이 올바르지 않습니다.')
    st.stop()

# 사용자 입력 받기
st.title('지역별 중학생 인구 비율')
region = st.selectbox('지역을 선택하세요:', df['행정구역'].unique())

# 선택한 지역의 데이터 필터링
region_data = df[df['행정구역'] == region]

if region_data.empty:
    st.error('선택한 지역의 데이터가 없습니다.')
else:
    # 중학생 인구 계산 (13세~15세)
    try:
        middle_school_population = region_data[['2024년06월_계_13세', '2024년06월_계_14세', '2024년06월_계_15세']].sum(axis=1).values[0]
        total_population = region_data['2024년06월_계_총인구수'].values[0]
        middle_school_ratio = middle_school_population / total_population * 100

        # 원 그래프 생성
        labels = ['중학생 인구', '기타 인구']
        sizes = [middle_school_ratio, 100 - middle_school_ratio]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)  # 중학생 인구 비율을 강조하기 위해 약간 분리

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # 원 그래프를 원형으로 그리기

        st.pyplot(fig1)
    except KeyError:
        st.error('필요한 열이 데이터에 없습니다.')
    except ZeroDivisionError:
        st.error('총 인구수가 0입니다. 중학생 인구 비율을 계산할 수 없습니다.')
