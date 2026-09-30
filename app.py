import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="頂級財富傳承精算系統", layout="wide", initial_sidebar_state="expanded")

# 針對手機端優化：高對比色塊與強制發光字體防護
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans TC', sans-serif; background-color: #0d1b2a !important; color: #e0e1dd !important;
    }
    [data-testid="stSidebar"] { background-color: #1b263b !important; border-right: 2px solid #e0a96d !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #ffcc66 !important; font-weight: 500 !important; background-color: #111c2c !important;
        padding: 4px 10px !important; border-radius: 6px !important; display: inline-block !important;
    }
    .mobile-safe-title {
        color: #ffcc66 !important; background-color: #1b263b !important; padding: 8px 16px !important;
        border-radius: 8px !important; border-left: 4px solid #e0a96d !important; font-weight: 700 !important;
    }
    .wealth-card {
        background: linear-gradient(145deg, #1b263b, #0d1b2a); padding: 20px;
        border-radius: 12px; border: 1px solid rgba(224, 169, 109, 0.3); margin-bottom: 15px;
    }
    .brand-header {
        background: linear-gradient(90deg, #112233, #1b263b); padding: 30px;
        border-radius: 16px; border-left: 6px solid #e0a96d; margin-bottom: 35px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<div class="brand-header"><span style="font-size: 14px; color: #e0a96d; font-weight:700;">FAMILY OFFICE</span>
<h1 style="margin:5px 0 0 0; font-size:32px; color:#ffffff;">🏛️ 輝煌家族辦公室 · 資產傳承壓力測試</h1></div>""", unsafe_allow_html=True)

CITY_TAX_RATES = {"台北市": 0.35, "新北市": 0.35, "台中市": 0.28, "高雄市": 0.28, "桃園市": 0.28, "新竹市": 0.28, "其他縣市": 0.22}

st.sidebar.markdown("<h2 style='color:#e0a96d; font-size:20px;'>👤 客戶基本參數設定</h2>", unsafe_allow_html=True)
client_name = st.sidebar.text_input("客戶姓名/專案編號", value="尊榮 VIP 客戶")
current_age = st.sidebar.number_input("當前年齡", min_value=1, max_value=119, value=40)
retirement_age = st.sidebar.number_input("預計退休年齡", min_value=current_age, max_value=120, value=int(max(current_age, 60)))
initial_cash = st.sidebar.number_input("現有流動現金/總存款 (元)", value=5000000)
annual_work_income = st.sidebar.number_input("目前年工作收入 (元)", value=1200000)
annual_pension_income = st.sidebar.number_input("年領退休金總額 *退休後計入*", value=300000)
annual_expenses = st.sidebar.number_input("目前年生活總開銷 (元)", value=600000)

tab1, tab2 = st.tabs(["🔒 自由配置動態資產清單", "🏆 執行終身資產精算簡報"])

with tab1:
    st.markdown("<div class='mobile-safe-title'>🏠 不動產活化配置清單</div>", unsafe_allow_html=True)
    if 're_count' not in st.session_state: st.session_state.re_count = 1
    real_estate_list = []
    for i in range(st.session_state.re_count):
        st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
        re_name = st.text_input(f"物業 {i+1} 名稱", value="信義路大樓" if i==0 else f"自訂不動產物業 {i+1}", key=f"re_name_{i}")
        re_market = st.number_input(f"估計市值", value=50000000 if i==0 else 10000000, key=f"re_market_{i}")
        re_city = st.selectbox(f"所在縣市", list(CITY_TAX_RATES.keys()), index=0 if i==0 else 6, key=f"re_city_{i}")
        re_is_lev = st.checkbox(f"啟動理財增貸套利", value=True if i==0 else False, key=f"re_lev_{i}")
        re_ratio, re_rate = 0.0, 0.0
        if re_is_lev:
            re_ratio = st.slider(f"增貸成數", 0.0, 0.8, 0.7, key=f"re_ratio_{i}")
            re_rate = st.number_input(f"增貸年利率 (%)", value=2.15, key=f"re_rate_{i}") / 100
        st.markdown("</div>", unsafe_allow_html=True)
        real_estate_list.append({"market_value": re_market, "city": re_city, "is_leverage": re_is_lev, "leverage_ratio": re_ratio, "loan_rate": re_rate})
    if st.button("➕ 新增一筆房地產物業"):
        st.session_state.re_count += 1
        st.rerun()

    st.markdown("<div class='mobile-safe-title'>📈 上市股票動態資產清單</div>", unsafe_allow_html=True)
    if 'stock_count' not in st.session_state: st.session_state.stock_count = 1
    stock_list = []
    for i in range(st.session_state.stock_count):
        st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
        st_name = st.text_input(f"股票名稱", value="台積電 2330" if i==0 else f"自訂股票 {i+1}", key=f"st_name_{i}")
        st_shares = st.number_input(f"持有總股數", value=10000 if i==0 else 1000, key=f"st_shares_{i}")
        st_now = st.number_input(f"昨日收盤價", value=950 if i==0 else 100, key=f"st_now_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        stock_list.append({"shares": st_shares, "price": st_now})
    if st.button("➕ 新增一筆股票標的"):
        st.session_state.stock_count += 1
        st.rerun()

    st.markdown("<div class='mobile-safe-title'>💎 海外配息基金動態清單</div>", unsafe_allow_html=True)
    if 'fund_count' not in st.session_state: st.session_state.fund_count = 1
    fund_list = []
    for i in range(st.session_state.fund_count):
        st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
        fd_name = st.text_input(f"基金名稱", value="全球高收益債券基金" if i==0 else f"自訂配息項目 {i+1}", key=f"fd_name_{i}")
        fd_value = st.number_input(f"目前持有總市值", value=2040000 if i==0 else 500000, key=f"fd_value_{i}")
        fd_rate = st.number_input(f"預估年化配息率 (%)", value=7.5 if i==0 else 5.0, key=f"fd_rate_{i}") / 100
        st.markdown("</div>", unsafe_allow_html=True)
        fund_list.append({"market_value": fd_value, "dividend_rate": fd_rate})
    if st.button("➕ 新增一筆基金/配息項目"):
        st.session_state.fund_count += 1
        st.rerun()

# --- 核心精算計算 ---
total_re_market = sum([re['market_value'] for re in real_estate_list])
total_re_tax = sum([re['market_value'] * CITY_TAX_RATES[re['city']] for re in real_estate_list])
total_leverage_cash = sum([re['market_value'] * re['leverage_ratio'] for re in real_estate_list if re['is_leverage']])
annual_loan_interest = sum([re['market_value'] * re['leverage_ratio'] * re['loan_rate'] for re in real_estate_list if re['is_leverage']])
stock_market_value = sum([stk['shares'] * stk['price'] for stk in stock_list])
base_fund_market_value = sum([f['market_value'] for f in fund_list])
base_annual_dividend = sum([f['market_value'] * f['dividend_rate'] for f in fund_list])

projection = []
cash_pool = initial_cash + total_leverage_cash
bankruptcy_age = -1
max_estate_tax, max_estate_tax_age = 0.0, current_age

for age in range(current_age, 121):
    total_annual_dividend = base_annual_dividend
    if total_leverage_cash > 0:
        avg_rate = (base_annual_dividend / base_fund_market_value) if base_fund_market_value > 0 else 0.06
        total_annual_dividend += total_leverage_cash * avg_rate
    basic_tax = (total_annual_dividend - 7500000.0) * 0.20 if (total_annual_dividend >= 1000000.0 and total_annual_dividend > 7500000.0) else 0.0
    work_inc = annual_work_income if age < retirement_age else 0
    pension_inc = annual_pension_income if age >= retirement_age else 0
    
    net_cash_flow = work_inc + pension_inc + total_annual_dividend - annual_expenses - annual_loan_interest - basic_tax
    cash_pool += net_cash_flow
    if cash_pool < 0 and bankruptcy_age == -1: bankruptcy_age = age
    
    estate_total = max(0, cash_pool) + stock_market_value + total_re_tax
    net_estate = estate_total - 13330000
    estate_tax = 0.0
    if net_estate > 0:
        if net_estate <= 50000000: estate_tax = net_estate * 0.10
        elif net_estate <= 100000000: estate_tax = net_estate * 0.15 - 250000
        else: estate_tax = net_estate * 0.20 - 5250000
    if estate_tax > max_estate_tax: max_estate_tax, max_estate_tax_age = estate_tax, age
        
    projection.append({"年齡": age, "總資產流動市值": max(0, cash_pool) + stock_market_value + total_re_market, "預估遺產稅": max(0, estate_tax), "當年度淨現金流": net_cash_flow})

df = pd.DataFrame(projection)

with tab2:
    st.markdown(f"<h2>📜 {client_name} 專屬終身資產規劃報告</h2>", unsafe_allow_html=True)
    st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
    if bankruptcy_age != -1: st.error(f"⚠️ 現金流安全警訊：資產池預計於 {bankruptcy_age} 歲 現金流告急。")
    if bankruptcy_age == -1: st.success("✅ 終身現金流檢測：現金流安全無虞至120歲。")
    st.info(f"🔮 身故傳承風險預警：最高身故遺產稅預估為新台幣 {max_estate_tax:,.0f} 元 (於 {max_estate_tax_age} 歲時)。")
    st.markdown("</div>", unsafe_allow_html=True)
    st.dataframe(df.style.format({"總資產流動市值": "{:,.0f}", "預估遺產稅": "{:,.0f}", "當年度淨現金流": "{:,.0f}"}), use_container_width=True)
