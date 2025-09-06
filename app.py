import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
# ========= Google Sheets 認証（Secretsから読み込み） =========
creds_dict = st.secrets["gcp_service_account"]  # ← Secrets の [gcp_service_account] を読む

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)

SPREADSHEET_ID = "1-6TncaQSXhRURxpJU7a-uw-5jDIYPDi9YzOKjQPnHF8"  # ← あなたのID
sh = gc.open_by_key(SPREADSHEET_ID)
worksheet = sh.sheet1



# =====================
# UI
# =====================
st.title("🥛 ヨーグルト記録アプリ")

date_input = st.date_input("仕込み日", datetime.now().date())
milk_type1  = st.selectbox("牛乳1", ["低脂肪","無調整","豆乳","ブレンド"])
milk_ratio1 = st.slider("割合1(%)", 0, 100, 50, 10)
milk_amount1= st.number_input("量1(ml)", min_value=0, value=500)

milk_type2  = st.selectbox("牛乳2", ["-","低脂肪","無調整","豆乳","ブレンド"])
milk_ratio2 = st.slider("割合2(%)", 0, 100, 0, 10)
milk_amount2= st.number_input("量2(ml)", min_value=0, value=0)

milk_brand  = st.text_input("メーカー")
starter_name   = st.text_input("種ヨーグルト")
starter_amount = st.number_input("種ヨーグルト量(g)", min_value=0, value=20)
fermentation_temp = st.slider("発酵温度(℃)", 30, 50, 42)
fermentation_time = st.slider("発酵時間(h)", 1, 12, 8)
drain_time        = st.slider("水切り(h)", 0, 12, 0)
result_weight = st.number_input("出来上がり(g)", min_value=0, value=200)
memo          = st.text_input("メモ")

# =====================
# 保存処理
# =====================
if st.button("記録する"):
    record = [
        date.strftime("%Y-%m-%d"),
        milk1, milk1_ratio, milk1_amount,
        milk2, milk2_ratio, milk2_amount,
        brand,
        starter_name, starter_amount,
        temp, time, drain,
        result, memo
    ]
    worksheet.append_row(record)
    st.success("✅ スプレッドシートに保存しました！")

# --- 直近の記録表示 ---
data = worksheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    st.subheader("📒 直近の記録")
    # 直近5件
    for _, row in df.tail(5).iterrows():
        card_html = f"""
        <div style="border:1px solid #e5e7eb;border-radius:12px;
                    padding:12px;margin:8px 0;
                    box-shadow:0 1px 3px rgba(0,0,0,0.06)">
          <div>📅 <b>仕込み日</b>: {row.get('仕込み日','')}</div>
          <div>🥛 <b>牛乳1</b>: {row.get('牛乳1','')} ({row.get('量1(ml)','')}ml, {row.get('割合1(%)','')}%)</div>
          <div>🥛 <b>牛乳2</b>: {row.get('牛乳2','')} ({row.get('量2(ml)','')}ml, {row.get('割合2(%)','')}%)</div>
          <div>🏭 <b>メーカー</b>: {row.get('メーカー','')}</div>
          <div>🧫 <b>種ヨーグルト</b>: {row.get('種ヨーグルト','')} ({row.get('種ヨーグルト量(g)','')}g)</div>
          <div>🌡 <b>発酵温度</b>: {row.get('発酵温度(℃)','')}</div>
          <div>⏳ <b>発酵時間</b>: {row.get('発酵時間(h)','')}h</div>
          <div>💧 <b>水切り時間</b>: {row.get('水切り(h)','')}h</div>
          <div>⚖️ <b>出来上がり</b>: {row.get('出来上(g)','')}</div>
          <div>📝 <b>メモ</b>: {row.get('メモ','')}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)







