import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="주식 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

st.title("📈 실시간 주식 분석 대시보드")

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "애플": "AAPL",
    "엔비디아": "NVDA",
    "테슬라": "TSLA"
}

selected = st.selectbox(
    "종목 선택",
    list(stocks.keys())
)

ticker = stocks[selected]

with st.spinner("데이터 불러오는 중..."):
    stock = yf.Ticker(ticker)

    info = stock.info

    hist = stock.history(period="1mo")

if len(hist) == 0:
    st.error("주가 데이터를 불러올 수 없습니다.")
    st.stop()

current_price = hist["Close"].iloc[-1]
previous_price = hist["Close"].iloc[-2]

change = current_price - previous_price
change_percent = (change / previous_price) * 100

col1, col2, col3 = st.columns(3)

col1.metric(
    "현재가",
    f"{current_price:,.2f}"
)

col2.metric(
    "전일 대비",
    f"{change:,.2f}",
    f"{change_percent:.2f}%"
)

col3.metric(
    "거래량",
    f"{hist['Volume'].iloc[-1]:,.0f}"
)

st.subheader("📊 최근 1개월 주가")

st.line_chart(hist["Close"])

st.subheader("🤖 AI 스타일 분석")

if change_percent > 3:
    st.success(
        "🚀 강한 상승세가 나타나고 있습니다. 투자자들의 매수세가 강한 상태입니다."
    )

elif change_percent > 0:
    st.info(
        "📈 완만한 상승세입니다. 긍정적인 흐름을 유지하고 있습니다."
    )

elif change_percent > -3:
    st.warning(
        "📉 소폭 하락 중입니다. 단기 변동성에 주의하세요."
    )

else:
    st.error(
        "⚠️ 강한 하락세가 나타나고 있습니다. 리스크 관리가 필요합니다."
    )

st.subheader("ℹ️ 기업 정보")

try:
    st.write(info.get("longBusinessSummary", "기업 정보 없음"))
except:
    st.write("기업 정보를 불러올 수 없습니다.")
