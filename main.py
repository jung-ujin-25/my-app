import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize-matplotlib

# 데이터 로드
df = pd.read_csv('/mnt/data/202406_202406_연령별인구현황_월간.csv', encoding='euc-kr')

# 데이터 전처리
df = df.replace(',', '', regex=True)
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)

# 사용자 입력 받기
st.title('지역별 중학생 인구 비율')
region = st.selectbox('지역을 선택하세요:', df['행정구역'].unique())

# 선택한 지역의 데이터 필터링
region_data = df[df['행정구역'] == region]

# 중학생 인구 계산 (13세~15세)
middle_school_population = region_data[['2024년06월_계_13세', '2024년06월_계_14세', '2024년06월_계_15세']].sum(axis=1).values[0]

# 총 인구수 계산
total_population = region_data['2024년06월_계_총인구수'].values[0]

# 비율 계산
middle_school_ratio = middle_school_population / total_population * 100

# 원 그래프 생성
labels = ['중학생 인구', '기타 인구']
sizes = [middle_school_ratio, 100 - middle_school_ratio]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)  # 중학생 인구 비율을 강조하기 위해 약간 분리

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # 원 그래프를 원형으로 그리기

st.pyplot(fig1)
