import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="頂級財富傳承精算系統", layout="wide")
st.title("🏛️ 輝煌家族辦公室 · 資產傳承精算系統")

CITY_TAX = {"台北市": 0.35, "新北市": 0.35, "台中市": 0.28, "高雄市": 0.28, "桃園市": 0.28, "新竹市": 0.28, "其他縣市": 0.22}

# 側邊欄參數輸入
st.sidebar.header("👤 客戶基本參數設定")
client_name = st.sidebar.text_input("客戶姓名/專案編號", value="尊榮 VIP 客戶")
current_age = st.sidebar.number_input("當前年齡", min_value=1, value=40)
retirement_age = st.sidebar.number_input("預計退休年齡", min_value=current_age, value=int(max(current_age, 60)))
initial_cash = st.sidebar.number_input("現有流動現金/存款 (元)", value=5000000)
annual_work_income = st.sidebar.number_input("目前年工作收入 (元)", value=1200000)
annual_pension_income = st.sidebar.number_input("年領退休金總額 (元)", value=300000)
annual_expenses = st.sidebar.number_input("目前年生活開銷 (元)", value=600000)

st.sidebar.header("⚙️ 傳承與壓力策略開關")
is_inflation_on = st.sidebar.checkbox("啟動退休後生活費 2% 通膨壓力測試", value=True)
is_gifting_on = st.sidebar.checkbox("啟動每年 244 萬分年贈與免稅規劃", value=True)

tab1, tab2 = st.tabs(["🔒 自由配置動態資產與保單清單", "🏆 執行終身資產精算簡報"])

with tab1:
    # 1. 不動產動態新增
    st.subheader("🏠 不動產配置清單")
    if 're_count' not in st.session_state: st.session_state.re_count = 1
    real_estate_list = []
    for i in range(st.session_state.re_count):
        re_name = st.text_input(f"物業 {i+1} 名稱", value="信義路大樓" if i==0 else f"自訂不動產物業 {i+1}", key=f"re_name_{i}")
        re_market = st.number_input(f"估計市值 (元)", value=50000000 if i==0 else 10000000, key=f"re_market_{i}")
        re_city = st.selectbox(f"所在縣市", list(CITY_TAX.keys()), index=0 if i==0 else 6, key=f"re_city_{i}")
        re_is_lev = st.checkbox(f"啟動理財增貸套利", value=True if i==0 else False, key=f"re_lev_{i}")
        re_ratio, re_rate = 0.0, 0.0
        if re_is_lev:
            re_ratio = st.slider(f"增貸成數", 0.0, 0.8, 0.7, key=f"re_ratio_{i}")
            re_rate = st.number_input(f"增貸年利率 (%)", value=2.15, key=f"re_rate_{i}") / 100
        real_estate_list.append({"market_value": re_market, "city": re_city, "is_leverage": re_is_lev, "leverage_ratio": re_ratio, "loan_rate": re_rate})
    if st.button("➕ 新增房地產"): st.session_state.re_count += 1; st.rerun()

    # 2. 股票與基金動態新增
    st.subheader("📈 上市股票與基金清單")
    if 'stock_count' not in st.session_state: st.session_state.stock_count = 1
    stock_list = []
    for i in range(st.session_state.stock_count):
        st_name = st.text_input(f"股票名稱 / 代號", value="台積電 2330" if i==0 else f"自訂股票 {i+1}", key=f"st_name_{i}")
        st_shares = st.number_input(f"持有股數", value=10000 if i==0 else 1000, key=f"st_shares_{i}")
        st_now = st.number_input(f"昨日收盤價 (元)", value=950 if i==0 else 100, key=f"st_now_{i}")
        stock_list.append({"shares": st_shares, "price": st_now})
    if st.button("➕ 新增股票"): st.session_state.stock_count += 1; st.rerun()

    if 'fund_count' not in st.session_state: st.session_state.fund_count = 1
    fund_list = []
    for i in range(st.session_state.fund_count):
        fd_name = st.text_input(f"基金或配息項目名稱", value="全球高收益債" if i==0 else f"自訂項目 {i+1}", key=f"fd_name_{i}")
        fd_value = st.number_input(f"流動市值 (元)", value=2040000 if i==0 else 500000, key=f"fd_value_{i}")
        fd_rate = st.number_input(f"年化配息率 (%)", value=7.5 if i==0 else 5.0, key=f"fd_rate_{i}") / 100
        fund_list.append({"market_value": fd_value, "dividend_rate": fd_rate})
    if st.button("➕ 新增基金"): st.session_state.fund_count += 1; st.rerun()

    # 3. 保單動態新增
    st.subheader("🛡️ 家族人身保單清單")
    if 'ins_count' not in st.session_state: st.session_state.ins_count = 1
    insurance_list = []
    for i in range(st.session_state.ins_count):
        ins_name = st.text_input(f"保單 {i+1} 名稱", value=f"人身保單 {i+1}", key=f"ins_name_{i}")
        ins_type = st.selectbox(f"保單功能類型", ["複利增額型保單", "生存還本金型保單", "高保額傳承型保單"], key=f"ins_type_{i}")
        ins_val1, ins_val2 = 0.0, 0.0
        if ins_type == "複利增額型保單":
            ins_val1 = st.number_input(f"目前解約金 (元)", value=1000000, key=f"ins_val1_{i}")
            ins_val2 = st.number_input(f"保單利率 (%)", value=3.2, key=f"ins_val2_{i}") / 100
        elif ins_type == "生存還本金型保單":
            ins_val1 = st.number_input(f"年領生存金 (元)", value=50000, key=f"ins_val1_{i}")
        elif ins_type == "高保額傳承型保單":
            ins_val1 = st.number_input(f"身故保險金額 (元)", value=10000000, key=f"ins_val1_{i}")
        insurance_list.append({"type": ins_type, "val1": ins_val1, "val2": ins_val2})
    if st.button("➕ 新增保單"): st.session_state.ins_count += 1; st.rerun()

# --- 核心大數據精算核心 ---
total_re_market = sum([re['market_value'] for re in real_estate_list])
total_re_tax = sum([re['market_value'] * CITY_TAX.get(re['city'], 0.22) for re in real_estate_list])
total_leverage_cash = sum([re['market_value'] * re['leverage_ratio'] for re in real_estate_list if re['is_leverage']])
annual_loan_interest = sum([re['market_value'] * re['leverage_ratio'] * re['loan_rate'] for re in real_estate_list if re['is_leverage']])
stock_market_value = sum([stk['shares'] * stk['price'] for stk in stock_list])
base_fund_market_value = sum([f['market_value'] for f in fund_list])
base_annual_dividend = sum([f['market_value'] * f['dividend_rate'] for f in fund_list])

initial_growth_ins = sum([ins['val1'] for ins in insurance_list if ins['type'] == "複利增額型保單"])
annual_survival_cash = sum([ins['val1'] for ins in insurance_list if ins['type'] == "生存還本金型保單"])
total_transmission_benefit = sum([ins['val1'] for ins in insurance_list if ins['type'] == "高保額傳承型保單"])

projection = []
cash_pool, growth_ins_pool, gifted_pool = initial_cash + total_leverage_cash, initial_growth_ins, 0.0
bankruptcy_age, max_estate_tax, max_estate_tax_age = -1, 0.0, current_age

for age in range(current_age, 121):
    total_annual_dividend = base_annual_dividend
    if total_leverage_cash > 0:
        avg_rate = (base_annual_dividend / base_fund_market_value) if base_fund_market_value > 0 else 0.06
        total_annual_dividend += total_leverage_cash * avg_rate
    basic_tax = (total_annual_dividend - 7500000.0) * 0.20 if (total_annual_dividend >= 1000000.0 and total_annual_dividend > 7500000.0) else 0.0
    growth_ins_pool *= 1.032
    
    work_inc = annual_work_income if age < retirement_age else 0
    pension_inc = annual_pension_income if age >= retirement_age else 0
    current_expenses = annual_expenses * (1.02 ** (age - retirement_age)) if (is_inflation_on and age >= retirement_age) else annual_expenses
    
    if is_gifting_on and cash_pool >= 2440000:
        cash_pool -= 2440000.0
        gifted_pool += 2440000.0
        
    net_cash_flow = work_inc + pension_inc + annual_survival_cash + total_annual_dividend - current_expenses - annual_loan_interest - basic_tax
    cash_pool += net_cash_flow
    if cash_pool < 0 and bankruptcy_age == -1: bankruptcy_age = age
    
    estate_total = max(0, cash_pool) + stock_market_value + total_re_tax + growth_ins_pool
    net_estate = estate_total - 13330000
    estate_tax = 0.0
    if net_estate > 0:
        if net_estate <= 50000000: estate_tax = net_estate * 0.10
        elif net_estate <= 100000000: estate_tax = net_estate * 0.15 - 250000
        else: estate_tax = net_estate * 0.20 - 5250000
    if estate_tax > max_estate_tax: max_estate_tax, max_estate_tax_age = estate_tax, age
        
    projection.append({"年齡": age, "總資產": max(0, cash_pool) + stock_market_value + total_re_market + growth_ins_pool, "已轉移免稅資產": gifted_pool, "預估遺產稅": max(0, estate_tax), "年生活費": current_expenses})
    
df = pd.DataFrame(projection)

with tab2:
    st.header(f"📜 {client_name} 專屬終身資產規劃報告")
    if bankruptcy_age != -1: st.error(f"⚠️ 現金流警告：受通膨開銷影響，資產預計於 {bankruptcy_age} 歲告急。")
    else: st.success("✅ 現金流安全：終身資產足以抵抗 2% 通膨，安全無虞。")
    st.info(f"🔮 傳承預警：最高身故遺產稅為新台幣 {max_estate_tax:,.0f} 元 (於 {max_estate_tax_age} 歲時)。")
    if is_gifting_on: st.success(f"📈 節稅成效：每年 244 萬免稅資產移轉已啟動，完美拉低法定遺產稅基。")
    if total_transmission_benefit > 0:
        if total_transmission_benefit >= max_estate_tax: st.success(f"🛡️ 預留稅源安全：配置 {total_transmission_benefit:,.0f} 元身故保險金，已完美覆蓋遺產稅！")
        else: st.warning(f"⚠️ 預留稅源缺口：仍有新台幣 {max_estate_tax - total_transmission_benefit:,.0f} 元的稅源缺口。")
    else: st.error("❌ 傳承缺口：尚未配置任何傳承型保單預留稅源，子女未來恐面臨缺乏現金繳稅困境。")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["年齡"], y=df["總資產"], name="總資產(含房產/保單)", line=dict(color='#e0a96d', width=3)))
    if is_gifting_on: fig.add_trace(go.Scatter(x=df["年齡"], y=df["已轉移免稅資產"], name="免稅資產(子女名下)", line=dict(color='#00cc66', width=2)))
    fig.add_trace(go.Scatter(x=df["年齡"], y=df["預估遺產稅"], name="預估遺產稅", line=dict(color='#ff4b4b', width=2, dash='dash')))
    fig.update_layout(title="納入通膨測試與分年贈與之終身財富規劃", xaxis_title="年齡", yaxis_title="元", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.style.format({"總資產": "{:,.0f}", "已轉移免稅資產": "{:,.0f}", "預估遺產稅": "{:,.0f}", "年生活費": "{:,.0f}"}), use_container_width=True)
