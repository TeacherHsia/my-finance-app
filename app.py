import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 設定網頁標題與樣式
st.set_page_config(page_title="高階財務傳承精算報告", layout="wide")

# CSS 樣式：優化列印排版（列印時隱藏側邊欄與 Streamlit 雜項）
st.markdown("""
    <style>
    @media print {
        div[data-testid="stSidebar"] { display: none !important; }
        header { display: none !important; }
        footer { display: none !important; }
        div.stButton { display: none !important; }
        .stTabs { display: none !important; }
        #MainMenu { visibility: hidden; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 高階財富管理：終身資產壓力測試與傳承精算系統")
st.markdown("---")

# 縣市遺產稅推估率
CITY_TAX_RATES = {
    "台北市": 0.35, "新北市": 0.35,
    "台中市": 0.28, "高雄市": 0.28, "桃園市": 0.28, "新竹市": 0.28,
    "其他縣市": 0.22
}

# 側邊欄：客戶基本資料
st.sidebar.header("👤 客戶基本設定")
client_name = st.sidebar.text_input("客戶姓名/編號", value="VIP 客戶")
current_age = st.sidebar.number_input("當前年齡", min_value=1, max_value=119, value=40)
retirement_age = st.sidebar.number_input("預計退休年齡", min_value=current_age, max_value=120, value=60)
initial_cash = st.sidebar.number_input("現有現金/存款 (元)", value=5000000)
annual_work_income = st.sidebar.number_input("目前年工作收入 (元)", value=1200000)
annual_expenses = st.sidebar.number_input("目前年生活總開銷 (元)", value=600000)

# 主畫面分頁
tab1, tab2 = st.tabs(["🏠 房地產與投資配置", "🚀 執行精算報告"])

with tab1:
    st.subheader("多筆房地產與增貸理財設定")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**房產 A 設定**")
        re1_market = st.number_input("房產 A 目前市價 (元)", value=50000000)
        re1_city = st.selectbox("房產 A 所在縣市", list(CITY_TAX_RATES.keys()), index=0)
        re1_is_lev = st.checkbox("房產 A 啟動增貸套利", value=True)
        re1_ratio = st.slider("房產 A 增貸成數", 0.0, 0.8, 0.7)
        re1_rate = st.number_input("房產 A 增貸年利率 (%)", value=2.15) / 100
    with col2:
        st.markdown("**房產 B 設定**")
        re2_market = st.number_input("房產 B 目前市價 (元)", value=25000000)
        re2_city = st.selectbox("房產 B 所在縣市", list(CITY_TAX_RATES.keys()), index=2)
        re2_is_lev = st.checkbox("房產 B 啟動增貸套利", value=False)

    st.markdown("---")
    st.subheader("投資組合與即時市值推估")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**股票部位 (例如: 台積電 2330)**")
        stock_shares = st.number_input("持有股數", value=10000)
        stock_now = st.number_input("即時收盤價 (元)", value=950)
    with col4:
        st.markdown("**基金部位 (月配息債券)**")
        fund_value = st.number_input("基金目前總現值 (元)", value=2040000)
        fund_div_rate = st.number_input("預估年化配息率 (%)", value=7.5) / 100

# 核心精算邏輯
total_re_market = re1_market + re2_market
total_re_tax = (re1_market * CITY_TAX_RATES[re1_city]) + (re2_market * CITY_TAX_RATES[re2_city])

total_leverage_cash = 0
annual_loan_interest = 0
if re1_is_lev:
    lev_amt = re1_market * re1_ratio
    total_leverage_cash += lev_amt
    annual_loan_interest += lev_amt * re1_rate
    
stock_market_value = stock_shares * stock_now

projection = []
cash_pool = initial_cash + total_leverage_cash
bankruptcy_age = None
max_estate_tax = 0
max_estate_tax_age = current_age

for age in range(current_age, 121):
    annual_dividend = (fund_value + (total_leverage_cash if re1_is_lev else 0)) * fund_div_rate
    
    basic_tax = 0
    if annual_dividend >= 1000000 and annual_dividend > 7500000:
        basic_tax = (annual_dividend - 7500000) * 0.20
        
    work_inc = annual_work_income if age < retirement_age else 0
    net_cash_flow = work_inc + annual_dividend - annual_expenses - annual_loan_interest - basic_tax
    cash_pool += net_cash_flow
    
    if cash_pool < 0 and bankruptcy_age is None:
        bankruptcy_age = age
        
    estate_total = max(0, cash_pool) + stock_market_value + total_re_tax
    net_estate = estate_total - 13330000
    estate_tax = 0
    if net_estate > 0:
        if net_estate <= 50000000: estate_tax = net_estate * 0.10
        elif net_estate <= 100000000: estate_tax = net_estate * 0.15 - 250000
        else: estate_tax = net_estate * 0.20 - 5250000
        
    if estate_tax > max_estate_tax:
        max_estate_tax = estate_tax
        max_estate_tax_age = age
        
    projection.append({
        "年齡": age,
        "總資產市值": max(0, cash_pool) + stock_market_value + total_re_market,
        "預估遺產稅": max(0, estate_tax),
        "淨現金流": net_cash_flow
    })
    
df = pd.DataFrame(projection)

with tab2:
    st.header(f"📜 {client_name} 專屬終身資產規劃簡報")
    st.caption(f"報告產出日期：{datetime.date.today().strftime('%Y-%m-%d')} | 精算模擬終點：120歲")
    
    # 專家建議區塊
    st.subheader("💡 系統專家精算建議")
    col_a, col_b = st.columns(2)
    with col_a:
        if bankruptcy_age:
            st.error(f"⚠️ **現金流警訊**：資產預計於 **{bankruptcy_age} 歲** 出現缺口，請調整退休開銷或提高投資回報率。")
        else:
            st.success("✅ **現金流安全**：終身現金流安全無虞，流動性充足。")
            
        fund_total_annual = (fund_value + (total_leverage_cash if re1_is_lev else 0)) * fund_div_rate
        if fund_total_annual >= 7500000:
            st.warning("⚠️ **最低稅負制風險**：海外配息已達基本所得稅額免稅紅線，需注意年度補稅。")
        else:
            st.success("✅ **最低稅負制安全**：海外所得未達補稅門檻。")
            
    with col_b:
        st.info(f"🔮 **最高遺產稅預警**：預計在 **{max_estate_tax_age} 歲** 時達到最高身故遺產稅，金額約為 **\${max_estate_tax:,.0f} 元**。建議提早規劃傳承工具（如人身保險預留稅源）。")

    # 圖表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["年齡"], y=df["總資產市值"], name="總資產市值 (含房產市價)", line=dict(color='#1f77b4', width=3)))
    fig.add_trace(go.Scatter(x=df["年齡"], y=df["預估遺產稅"], name="預估身故遺產稅 (法定現值計)", line=dict(color='#d62728', width=3, dash='dash')))
    fig.update_layout(title="終身資產消長與身故遺產稅壓力測試", xaxis_title="年齡 (歲)", yaxis_title="新台幣 (元)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    # 資料表
    st.subheader("📋 逐年精算數據明細")
    st.dataframe(df.style.format({"總資產市值": "{:,.0f}", "預估遺產稅": "{:,.0f}", "淨現金流": "{:,.0f}"}), use_container_width=True)

    st.markdown("---")
    st.markdown("👉 **如何列印 / 匯出 PDF？**：請直接按下鍵盤的 **`Command (⌘) + P`**，在列印選項中選擇「另存為 PDF」即可。側邊欄與按鈕會自動被隱藏。")
