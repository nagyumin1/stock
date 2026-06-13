import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="국내외 주요 주가 분석", layout="wide")
st.title("📊 최근 1년 주요 기업 주가 변동 분석 웹앱")
st.markdown("삼성전자, SK하이닉스, 구글, 마이크로소프트, 애플의 최근 1개년 주가 데이터를 분석합니다.")

# 2. 주식 티커 설정
tickers = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "구글 (Google)": "GOOG",
    "마이크로소프트 (MS)": "MSFT",
    "애플 (Apple)": "AAPL"
}

# 3. 데이터 수집 기간 설정 (최근 1년)
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# 4. 데이터 캐싱 및 로드 (속도 최적화)
@st.cache_data
def load_data(ticker_dict, start, end):
    all_data = pd.DataFrame()
    for name, ticker in ticker_dict.items():
        # 주가 데이터 가져오기 (수정종가 Adj Close 기준)
        df = yf.download(ticker, start=start, end=end)['Adj Close']
        all_data[name] = df
    return all_data

with st.spinner('야후 파이낸스에서 데이터를 가져오는 중입니다...'):
    data = load_data(tickers, start_date, end_date)

# 5. 레이아웃 구획 및 대시보드 구현
tab1, tab2, tab3 = st.tabs(["📈 주가 변동 차트", "🔄 누적 수익률 비교", "📋 원본 데이터"])

with tab1:
    st.subheader("기업
