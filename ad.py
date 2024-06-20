# 필요한 라이브러리 설치 및 불러오기
!pip install finance-datareader pandas matplotlib
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

# KRX 종목 코드 정보 가져오기
krx_data = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
# 필요한 열(회사명, 종목코드)만 추출
krx_data = krx_data[['회사명', '종목코드']]
# 열 이름을 영어로 변경
krx_data = krx_data.rename(columns={'회사명': 'Company', '종목코드': 'Code'})
# 종목 코드를 문자열로 변환하고 6자리 형식으로 맞추기
krx_data['Code'] = krx_data['Code'].apply(lambda x: str(x).zfill(6))

# 회사 이름으로 종목 코드를 찾는 함수
def get_stock_code(company_name):
    # 회사 이름으로 종목 코드 찾기
    code = krx_data.loc[krx_data['Company'] == company_name, 'Code']
    # 종목 코드가 있으면 반환, 없으면 None 반환
    return code.values[0] if not code.empty else None

# 사용자로부터 회사명 입력 받기 (콤마로 구분)
company_names = input("Enter company names separated by a comma (e.g., '삼성전자,LG전자'): ").split(',')

# 각 회사의 주식 데이터를 저장할 딕셔너리
stock_data = {}
for company in company_names:
    company = company.strip()  # 회사명 앞뒤 공백 제거
    code = get_stock_code(company)  # 회사명에 해당하는 종목 코드 가져오기
    if code:
        # 종목 코드로 주식 데이터 가져와서 딕셔너리에 저장
        stock_data[company] = fdr.DataReader(code)

# 데이터를 일, 주, 월, 년 단위로 리샘플링하는 함수
def resample_data(df, period):
    return df['Close'].resample(period).ohlc()

# 리샘플링할 기간 설정 (일, 주, 월, 년)
resample_periods = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'M', 'Yearly': 'Y'}

# 그래프 그리기
fig, axs = plt.subplots(len(stock_data), len(resample_periods), figsize=(20, 10))

# 회사가 하나만 있을 때 axs를 리스트로 변환하여 일관성 유지
if len(stock_data) == 1:
    axs = [axs]

# 각 회사의 데이터를 각 기간별로 그래프에 표시
for i, (company, data) in enumerate(stock_data.items()):
    for j, (period_name, period) in enumerate(resample_periods.items()):
        # 데이터 리샘플링
        resampled_data = resample_data(data, period)
        # 리샘플링된 데이터로 그래프 그리기
        axs[i][j].plot(resampled_data.index, resampled_data['close'], label=f'{company} ({period_name})')
        # 그래프 제목 설정
        axs[i][j].set_title(f'{company} ({period_name})')
        # 범례 표시
        axs[i][j].legend()

# 그래프 간 여백 조정
plt.tight_layout()
# 그래프 보여주기
plt.show()
