import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 設定網頁標題與樣式
st.set_page_config(page_title="頂級財富傳承精算系統", layout="wide", initial_sidebar_state="expanded")

# --- 皇家私人銀行高階視覺風格注入 (CSS) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans TC', sans-serif;
        background-color: #0d1b2a !important;
        color: #e0e1dd !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1b263b !important;
        border-right: 2px solid #e0a96d !important;
    }
    .wealth-card {
        background: linear-gradient(145deg, #1b263b, #0d1b2a);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(224, 169, 109, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    .brand-header {
        background: linear-gradient(90deg, #112233, #1b263b);
        padding: 30px;
        border-radius: 16px;
        border-left: 6px solid #e0a96d;
        margin-bottom: 35px;
    }
    @media print {
        div[data-testid="stSidebar"] { display: none !important; }
        header { display: none !important; }
        footer { display: none !important; }
        div.stButton { display: none !important; }
        .brand-header { border-left: 10px solid #000 !important; background: #fff !important; color: #000 !important;}
        body { background-color: #ffffff !important; color: #000000 !important; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <span style="font-size: 14px; letter-spacing: 2px; color: #e0a96d; font-weight:700;">FAMILY OFFICE & WEALTH MANAGEMENT</span>
        <h1 style="margin: 5px 0 0 0; font-size: 32px; font-weight: 700; color: #ffffff; letter-spacing: 1px;">
            🏛️ 輝煌家族辦公室 · 資產傳承壓力測試系統
        </h1>
    </div>
""", unsafe_allow_html=True)

CITY_TAX_RATES = {
    "台北市": 0.35, "新北市": 0.35, "台中市": 0.28, "高雄市": 0.28, "桃園市": 0.28, "新竹市": 0.28, "其他縣市": 0.22
}

st.sidebar.markdown("<h2 style='color:#e0a96d; font-size:20px;'>👤 客戶基本參數設定</h2>", unsafe_allow_html=True)
client_name = st.sidebar.text_input("客戶姓名/專案編號", value="尊榮 VIP 客戶")
current_age = st.sidebar.number_input("當前年齡", min_value=1, max_value=119, value=40)

# 動態調整退休年齡預設值，解決年齡大於60歲時的崩潰問題
default_retirement = max(current_age, 60)
retirement_age = st.sidebar.number_input("預計退休年齡", min_value=current_age, max_value=120, value=int(default_retirement))

initial_cash = st.sidebar.number_input("現有流動現金/總存款 (元)", value=5000000)
annual_work_income = st.sidebar.number_input("目前年工作收入 (元)", value=1200000)
annual_expenses = st.sidebar.number_input("目前年生活總開銷 (元)", value=600000)

tab1, tab2 = st.tabs(["🔒 自由配置動態資產清單", "🏆 執行終身資產精算簡報"])

with tab1:
    st.markdown("<h3 style='color:#e0a96d;'>🏠 不動產活化配置清單</h3>", unsafe_allow_html=True)
    if 're_count' not in st.session_state:
        st.session_state.re_count = 1
        
    real_estate_list = []
    for i in range(st.session_state.re_count):
        st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
        re_name = st.text_input(f"物業 {i+1} 名稱 / 地段描述", value="信義路大樓" if i==0 else f"自訂不動產物業 {i+1}", key=f"re_name_{i}")
        re_market = st.number_input(f"估計市值 (元)", value=50000000 if i==0 else 10000000, key=f"re_market_{i}")
        re_city = st.selectbox(f"所在縣市", list(CITY_TAX_RATES.keys()), index=0 if i==0 else 6, key=f"re_city_{i}")
        re_is_lev = st.checkbox(f"啟動理財增貸套利", value=True if i==0 else False, key=f"re_lev_{i}")
        
        re_ratio = 0.0
        re_rate = 0.0
        if re_is_lev:
            re_ratio = st.slider(f"增貸成數", 0.0, 0.8, 0.7, key=f"re_ratio_{i}")
            re_rate = st.number_input(f"增貸年利率 (%)", value=2.15, key=f"re_rate_{i}") / 100
            
        st.markdown("</div>", unsafe_allow_html=True)
        real_estate_list.append({"name": re_name, "market_value": re_market, "city": re_city, "is_leverage": re_is_lev, "leverage_ratio": re_ratio, "loan_rate": re_rate})
        
    if st.button("➕ 新增一筆房地產物業"):
        st.session_state.re_count += 1
        st.rerun()

    st.markdown("<h3 style='color:#e0a96d;'>📈 上市股票動態資產清單</h3>", unsafe_allow_html=True)
    if 'stock_count' not in st.session_state:
        st.session_state.stock_count = 1
        
    stock_list = []
    for i in range(st.session_state.stock_count):
        st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
        st_name = st.text_input(f"股票名稱 / 代號", value="台積電 2330" if i==0 else f"自訂股票 {i+1}", key=f"st_name_{i}")
        st_shares = st.number_input(f"持有總股數", value=10000 if i==0 else 1000, key=f"st_shares_{i}")
        st_now = st.number_input(f"昨日收盤價 (元)", value=950 if i==0 else 100, key=f"st_now_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        stock_list.append({"name": st_name, "shares": st_shares, "price": st_now})
        
    if st.button("➕ 新增一筆股票標的"):
        st.session_state.stock_count += 1
        st.rerun()

    st.markdown("<h3 style='color:#e0a96d;'>💎 海外配息基金動態清單</h3>", unsafe_allow_html=True)
    if 'fund_count' not in st.session_state:
        st.session_state.fund_count = 1
        
    fund_list = []
    for i in range(st.session_state.fund_count):
        st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
        fd_name = st.text_input(f"基金或配息型項目名稱", value="全球高收益債券基金" if i==0 else f"自訂配息項目 {i+1}", key=f"fd_name_{i}")
        fd_value = st.number_input(f"目前持有總市值 (元)", value=2040000 if i==0 else 500000, key=f"fd_value_{i}")
        fd_rate = st.number_input(f"預估年化配息率 (%)", value=7.5 if i==0 else 5.0, key=f"fd_rate_{i}") / 100
        st.markdown("</div>", unsafe_allow_html=True)
        fund_list.append({"name": fd_name, "market_value": fd_value, "dividend_rate": fd_rate})
        
    if st.button("➕ 新增一筆基金/配息項目"):
        st.session_state.fund_count += 1
        st.rerun()

total_re_market = sum([re['market_value'] for re in real_estate_list])
total_re_tax = sum([re['market_value'] * CITY_TAX_RATES[re['city']] for re in real_estate_list])

total_leverage_cash = 0
annual_loan_interest = 0
for re in real_estate_list:
    if re['is_leverage']:
        lev_amt = re['market_value'] * re['leverage_ratio']
        total_leverage_cash += lev_amt
        annual_loan_interest += lev_amt * re['loan_rate']

stock_market_value = sum([stk['shares'] * stk['price'] for stk in stock_list])
base_fund_market_value = sum([f['market_value'] for f in fund_list])

projection = []
cash_pool = initial_cash + total_leverage_cash
bankruptcy_age = -1
max_estate_tax = 0.0
max_estate_tax_age = current_age

base_annual_dividend = sum([f['market_value'] * f['dividend_rate'] for f in fund_list])

for age in range(current_age, 121):
    total_annual_dividend = base_annual_dividend
    if total_leverage_cash > 0:
        if base_fund_market_value > 0:
            avg_rate = base_annual_dividend / base_fund_market_value
        else:
            avg_rate = 0.06
        total_annual_dividend += total_leverage_cash * avg_rate
        
    basic_tax = 0.0
    if total_annual_dividend >= 1000000.0 and total_annual_dividend > 7500000.0:
        basic_tax = (total_annual_dividend - 7500000.0) * 0.20
        
    if age < retirement_age:
        work_inc = annual_work_income
    else:
        work_inc = 0
    
    net_cash_flow = work_inc + total_annual_dividend - annual_expenses - annual_loan_interest - basic_tax
    cash_pool += net_cash_flow
    
    if cash_pool < 0 and bankruptcy_age == -1:
        bankruptcy_age = age
        
    estate_total = max(0, cash_pool) + stock_market_value + total_re_tax
    net_estate = estate_total - 13330000
    
    estate_tax = 0.0
    if net_estate > 0:
        if net_estate <= 50000000:
            estate_tax = net_estate * 0.10
        elif net_estate <= 100000000:
            estate_tax = net_estate * 0.15 - 250000
        else:
            estate_tax = net_estate * 0.20 - 5250000
        
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
    st.markdown(f"<h2>📜 {client_name} 專屬終身資產規劃報告</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='wealth-card'>", unsafe_allow_html=True)
    if bankruptcy_age != -1:
        st.error(f"⚠️ 現金流安全警訊：資產池預計於 {bankruptcy_age} 歲 現金流告急。")
    if bankruptcy_age == -1:
        st.success("✅ 終身現金流檢測：現金流安全無虞至120歲。")
    st.info(f"🔮 身故傳承風險預警：最高遺產稅為新台幣 {max_estate_tax:,.0f} 元。")
    st.markdown("</div>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["年齡"], y=df["總資產市值"], name="總資產", line=dict(color='#e0a96d', width=3)))
    fig.add_trace(go.Scatter(x=df["年齡"], y=df["預估遺產稅"], name="遺產稅", line=dict(color='#ff4b4b', width=2, dash='dash')))
    fig.update_layout(title="終身資產傳承與壓力測試", xaxis_title="年齡", yaxis_title="元", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df.style.format({"總資產市值": "{:,.0f}", "預估遺產稅": "{:,.0f}", "淨現金流": "{:,.0f}"}), use_container_width=True)
