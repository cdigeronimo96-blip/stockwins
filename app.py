# ═══════════════════════════════════════════════════════════════════════════════
# STOCKWINS — Premium Stock Analysis & BI Platform
# Data: Twelve Data · Yahoo Finance · StockTwits
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import requests
import pandas as pd
import ta
import yfinance as yf
import hashlib
import time
from datetime import datetime

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StockWins | Smart Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080c14 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] { background: #0d1220 !important; border-right: 1px solid #1e2a3a; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stDecoration"] { visibility: hidden; display: none; }
div.block-container { padding-top: 1rem !important; }

/* Buttons */
.stButton > button {
    background: #111827 !important; border: 1px solid #1e2a3a !important;
    color: #94a3b8 !important; border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { border-color: #3b82f6 !important; color: #60a5fa !important; background: #1a2744 !important; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    border-color: #3b82f6 !important; color: white !important; font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover { background: linear-gradient(135deg, #60a5fa, #3b82f6) !important; color: white !important; }
/* Inputs */
.stTextInput > div > div > input, .stTextArea > div > div > textarea,
.stSelectbox > div > div { background: #111827 !important; border-color: #1e2a3a !important; color: #e2e8f0 !important; border-radius: 8px !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important; }
.stMultiSelect > div { background: #111827 !important; border-color: #1e2a3a !important; }
[data-testid="stCheckbox"] > label { color: #94a3b8 !important; }
[data-testid="stRadio"] > div > label { color: #94a3b8 !important; }
.stProgress > div > div { background: #1e2a3a !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #3b82f6, #06b6d4) !important; }
.streamlit-expanderHeader { background: #111827 !important; border: 1px solid #1e2a3a !important; border-radius: 8px !important; color: #94a3b8 !important; }
.streamlit-expanderContent { background: #0d1220 !important; border: 1px solid #1e2a3a !important; border-top: none !important; }
[data-testid="stDataFrame"] { border: 1px solid #1e2a3a !important; border-radius: 10px !important; overflow: hidden; }
hr { border-color: #1e2a3a !important; }
[data-testid="stTabs"] > div { border-color: #1e2a3a !important; }
[data-testid="stTab"] { color: #64748b !important; }

/* ── Custom ── */
.sw-logo { font-family: 'Space Mono', monospace; font-size: 20px; font-weight: 700; color: #3b82f6; }
.sw-logo span { color: #06b6d4; }

.sw-card { background: #111827; border: 1px solid #1e2a3a; border-radius: 12px; padding: 20px; margin-bottom: 12px; transition: border-color 0.2s; }
.sw-card:hover { border-color: #374151; }
.sw-card-blue { background: linear-gradient(135deg, #0f2460 0%, #111827 100%); border: 1px solid #3b82f6; border-radius: 12px; padding: 20px; margin-bottom: 12px; }
.sw-card-gold { background: linear-gradient(135deg, #1a1200 0%, #111827 100%); border: 1px solid #d97706; border-radius: 12px; padding: 20px; margin-bottom: 12px; }
.sw-card-green { background: linear-gradient(135deg, #052e16 0%, #111827 100%); border: 1px solid #16a34a; border-radius: 12px; padding: 20px; margin-bottom: 12px; }

.hero { background: radial-gradient(ellipse at 50% -10%, #0f2460 0%, #080c14 60%); border: 1px solid #1e2a3a; border-radius: 16px; padding: 72px 40px; text-align: center; margin-bottom: 32px; }
.hero-eyebrow { font-family: 'Space Mono', monospace; font-size: 11px; font-weight: 700; color: #3b82f6; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }
.hero-title { font-size: 50px; font-weight: 800; color: #f1f5f9; line-height: 1.1; margin-bottom: 20px; letter-spacing: -1px; }
.hero-title .accent { color: #3b82f6; }
.hero-sub { font-size: 17px; color: #64748b; max-width: 550px; margin: 0 auto 32px; line-height: 1.7; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge-bull { background: #052e16; color: #4ade80; }
.badge-bear { background: #450a0a; color: #f87171; }
.badge-neutral { background: #1e293b; color: #94a3b8; }
.badge-hot { background: #431407; color: #fb923c; }
.badge-premium { background: #1a1200; color: #d97706; }
.badge-new { background: #0c1a3a; color: #60a5fa; }

.ticker-sym { font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; color: #60a5fa; }
.price-lg { font-family: 'Space Mono', monospace; font-size: 36px; font-weight: 700; color: #f1f5f9; letter-spacing: -1px; }
.chg-pos { color: #4ade80; font-weight: 700; }
.chg-neg { color: #f87171; font-weight: 700; }

.section-hd { font-size: 18px; font-weight: 800; color: #f1f5f9; margin: 24px 0 14px; display: flex; align-items: center; gap: 10px; }
.section-hd::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #1e2a3a, transparent); }

.stat-box { background: #0d1220; border: 1px solid #1e2a3a; border-radius: 10px; padding: 14px 12px; text-align: center; }
.stat-val { font-family: 'Space Mono', monospace; font-size: 17px; font-weight: 700; color: #f1f5f9; }
.stat-lbl { font-size: 10px; color: #475569; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.5px; }

.insight-row { background: #0d1220; border-left: 3px solid #3b82f6; border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 6px 0; }
.insight-bull { border-left-color: #4ade80; }
.insight-bear { border-left-color: #f87171; }

.heat-pos { background: #052e16; color: #4ade80; border-radius: 6px; padding: 8px 4px; text-align: center; font-size: 12px; font-weight: 700; }
.heat-neg { background: #450a0a; color: #f87171; border-radius: 6px; padding: 8px 4px; text-align: center; font-size: 12px; font-weight: 700; }
.heat-neu { background: #1e293b; color: #64748b; border-radius: 6px; padding: 8px 4px; text-align: center; font-size: 12px; font-weight: 700; }

.lock-box { background: rgba(8,12,20,0.92); border: 1px solid #d97706; border-radius: 12px; padding: 40px; text-align: center; }
.pricing-card { background: #111827; border: 1px solid #1e2a3a; border-radius: 14px; padding: 32px 24px; }
.pricing-featured { background: linear-gradient(160deg, #0f2460 0%, #111827 60%); border: 2px solid #3b82f6; border-radius: 14px; padding: 32px 24px; }
.pricing-price { font-family: 'Space Mono', monospace; font-size: 42px; font-weight: 700; color: #f1f5f9; }

.disclaimer { background: #0d1220; border: 1px solid #1e2a3a; border-left: 3px solid #d97706; border-radius: 0 8px 8px 0; padding: 14px 18px; font-size: 12px; color: #475569; line-height: 1.7; margin-top: 20px; }
.footer { background: #0d1220; border-top: 1px solid #1e2a3a; border-radius: 12px; padding: 32px; margin-top: 40px; }

.mover-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-bottom: 1px solid #1e2a3a; font-size: 13px; }
.mover-row:last-child { border-bottom: none; }

.risk-low { color: #4ade80; font-weight: 700; }
.risk-med { color: #fbbf24; font-weight: 700; }
.risk-high { color: #f87171; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
CATEGORIES = {
    "🔥 StockTwits Hot":     [],
    "💻 Tech":               ["AAPL","MSFT","GOOGL","META","AMZN","NVDA","AMD","INTC","QCOM","AVGO","CRM","ORCL","ADBE","NOW","SNOW","UBER","SHOP","SQ","PYPL","NET","DDOG","MDB","OKTA","ZS","CRWD"],
    "🤖 AI":                 ["NVDA","AMD","PLTR","MSFT","GOOGL","IBM","SOUN","BBAI","AI","ASTS","IONQ","QUBT","RGTI","SMCI","DELL","HPE","ARM","ALAB","MRVL","AVGO"],
    "⚡ EV":                 ["TSLA","RIVN","LCID","NIO","LI","XPEV","F","GM","CHPT","BLNK","FSR","GOEV","WKHS","NKLA","ACHR"],
    "🧬 Biotech":            ["MRNA","BNTX","NVAX","VRTX","REGN","BIIB","GILD","AMGN","SRPT","EDIT","CRSP","BEAM","NTLA","ALLO","FATE"],
    "💥 Short Squeeze":      [],
    "📈 Momentum":           [],
    "🔊 High Volume":        [],
    "📉 Oversold Bounce":    [],
    "🚀 Breakouts":          [],
    "🎭 Meme / Social":      ["GME","AMC","BBIG","MULN","FFIE","ATER","SPCE","HOOD","CLOV","WKHS","SNDL","MMAT"],
    "📊 S&P 500":            ["AAPL","MSFT","AMZN","GOOGL","META","TSLA","NVDA","JPM","JNJ","V","PG","MA","UNH","HD","XOM","CVX","LLY","ABBV","MRK","PFE","BAC","WMT","KO","DIS","NFLX"],
    "💹 NASDAQ":             ["AAPL","MSFT","AMZN","NVDA","META","GOOGL","TSLA","AVGO","COST","AMD","CSCO","TMUS","ADBE","TXN","QCOM","AMGN","INTU","ISRG","REGN","VRTX","PANW","LRCX","KLAC","SNPS"],
    "🏦 Russell 1000":       ["IWB","AAPL","MSFT","AMZN","NVDA","META","GOOGL","TSLA","BRK-B","JPM","JNJ","V","PG","MA","UNH","HD","XOM","CVX","LLY","ABBV"],
    "🔬 Small Cap":          ["FFIE","MULN","NKLA","GOEV","WKHS","HCDI","ATER","SPCE","SOUN","BBAI","ASTS","IONQ","QUBT","RGTI","MNMD","ACHR","JOBY","LILM","EVTL","SURF"],
}

PREMIUM_CATS = {"💥 Short Squeeze","📈 Momentum","🔊 High Volume","📉 Oversold Bounce","🚀 Breakouts"}
FREE_CATS    = [c for c in CATEGORIES if c not in PREMIUM_CATS]

SECTOR_ETFS  = {"Technology":"XLK","Healthcare":"XLV","Financials":"XLF","Energy":"XLE",
                "Cons. Disc":"XLY","Industrials":"XLI","Materials":"XLB","Utilities":"XLU",
                "Real Estate":"XLRE","Comm Svcs":"XLC"}

INDEXES = {"S&P 500":"^GSPC","NASDAQ":"^IXIC","DOW":"^DJI","VIX":"^VIX","Russell 2K":"^RUT"}

BI_UNIVERSE = ["AAPL","MSFT","NVDA","AMD","TSLA","META","AMZN","GOOGL","PLTR","MSTR",
               "GME","AMC","HOOD","RIVN","LCID","NIO","MRNA","BNTX","SMCI","ARM",
               "SOUN","ASTS","IONQ","QUBT","BBAI","AI","JPM","BAC","XOM","CVX",
               "LLY","ABBV","VRTX","REGN","CRSP","EDIT","AVGO","QCOM","INTC","IBM"]

RISK_LEVELS = {
    "Small Cap":   "High", "🎭 Meme / Social": "Very High", "🔬 Small Cap": "Very High",
    "⚡ EV":       "High",  "🧬 Biotech": "High", "💥 Short Squeeze": "Very High",
    "🤖 AI":       "Medium-High", "💻 Tech": "Medium", "📊 S&P 500": "Low-Medium",
    "💹 NASDAQ":   "Medium", "🏦 Russell 1000": "Low-Medium",
}

# ── SESSION STATE ─────────────────────────────────────────────────────────────
def init():
    defs = {
        "page": "landing",
        "user": None,
        "role": "guest",
        "watchlist": [],
        "saved_screeners": [],
        "alerts": [],
        "api_key_input": "",
        "detail_ticker": None,
        "detail_data": {},
        "settings_tab": "Profile",
        "users_db": {
            "demo@stockwins.com":    {"pw": hashlib.sha256(b"demo123").hexdigest(),  "name": "Demo User",   "role": "free",    "verified": True,  "alerts": [], "notif_email": True, "notif_vol": False},
            "premium@stockwins.com": {"pw": hashlib.sha256(b"premium1").hexdigest(), "name": "Alex Rivera", "role": "premium", "verified": True,  "alerts": [], "notif_email": True, "notif_vol": True},
            "admin@stockwins.com":   {"pw": hashlib.sha256(b"admin123").hexdigest(), "name": "Admin",       "role": "admin",   "verified": True,  "alerts": [], "notif_email": True, "notif_vol": True},
        },
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ── AUTH ──────────────────────────────────────────────────────────────────────
def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()

def login(email, pw):
    db = st.session_state.users_db
    if email in db and db[email]["pw"] == hp(pw):
        st.session_state.user = {"email": email, "name": db[email]["name"]}
        st.session_state.role = db[email]["role"]
        return True
    return False

def signup(email, pw, name):
    db = st.session_state.users_db
    if email in db: return False, "Account already exists."
    db[email] = {"pw": hp(pw), "name": name, "role": "free", "verified": False,
                 "alerts": [], "notif_email": True, "notif_vol": False}
    st.session_state.user = {"email": email, "name": name}
    st.session_state.role = "free"
    return True, "Welcome!"

def logout():
    st.session_state.user = None; st.session_state.role = "guest"; nav("landing")

def is_premium(): return st.session_state.role in ("premium","admin")
def is_authed():  return st.session_state.user is not None
def nav(p):
    st.session_state.page = p
    st.rerun()

def get_user_db():
    if not is_authed(): return {}
    return st.session_state.users_db.get(st.session_state.user["email"], {})

# ── API KEY ───────────────────────────────────────────────────────────────────
def get_key():
    try:    return st.secrets["TWELVE_DATA_API_KEY"]
    except: return st.session_state.get("api_key_input","")

# ── DATA FETCHING ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=900)
def st_hot():
    try:
        d = requests.get("https://api.stocktwits.com/api/2/trending/symbols.json",timeout=8).json()
        return [s["symbol"] for s in d.get("symbols",[])]
    except: return ["NVDA","TSLA","AAPL","AMD","MSTR","PLTR","META","MSFT","AMZN","GOOGL"]

@st.cache_data(ttl=900)
def st_sentiment(ticker):
    try:
        d = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json",timeout=8).json()
        msgs = d.get("messages",[])
        bull = sum(1 for m in msgs if m.get("entities",{}).get("sentiment",{}) and m["entities"]["sentiment"].get("basic")=="Bullish")
        bear = sum(1 for m in msgs if m.get("entities",{}).get("sentiment",{}) and m["entities"]["sentiment"].get("basic")=="Bearish")
        tot  = bull+bear
        return {"bull": round((bull/tot)*100) if tot else 50, "bear": round((bear/tot)*100) if tot else 50,
                "msgs": len(msgs), "wl": d.get("symbol",{}).get("watchlist_count",0)}
    except: return {"bull":50,"bear":50,"msgs":0,"wl":0}

@st.cache_data(ttl=300)
def td_quote(ticker, api_key):
    if not api_key: return None
    try:
        d = requests.get(f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={api_key}",timeout=8).json()
        if "close" not in d: return None
        return {"price": float(d.get("close",0)), "open": float(d.get("open",0)),
                "high": float(d.get("high",0)), "low": float(d.get("low",0)),
                "volume": int(d.get("volume",0)), "prev": float(d.get("previous_close",0)),
                "chg": float(d.get("change",0)), "chg_pct": float(d.get("percent_change",0)),
                "name": d.get("name",ticker)}
    except: return None

@st.cache_data(ttl=600)
def td_ohlcv(ticker, api_key, n=60):
    if not api_key: return None
    try:
        d = requests.get(f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize={n}&apikey={api_key}",timeout=10).json()
        if "values" not in d: return None
        df = pd.DataFrame(d["values"])
        for c in ["open","high","low","close","volume"]: df[c] = df[c].astype(float)
        return df.iloc[::-1].reset_index(drop=True)
    except: return None

@st.cache_data(ttl=3600)
def yf_info(ticker):
    try:
        i = yf.Ticker(ticker).info
        return {"mktcap": i.get("marketCap",0), "sf": i.get("shortPercentOfFloat",0),
                "dtc": i.get("shortRatio",0), "avgvol": i.get("averageVolume",0),
                "sector": i.get("sector","N/A"), "industry": i.get("industry","N/A"),
                "pe": i.get("trailingPE",None), "hi52": i.get("fiftyTwoWeekHigh",0),
                "lo52": i.get("fiftyTwoWeekLow",0), "beta": i.get("beta",None),
                "desc": (i.get("longBusinessSummary","")[:300]+"...") if i.get("longBusinessSummary") else ""}
    except: return {}

@st.cache_data(ttl=900)
def sector_perf():
    out = {}
    for s, etf in SECTOR_ETFS.items():
        try:
            h = yf.Ticker(etf).history(period="5d")
            if len(h)>=2: out[s] = round(((h["Close"].iloc[-1]-h["Close"].iloc[-2])/h["Close"].iloc[-2])*100,2)
        except: out[s] = 0.0
    return out

@st.cache_data(ttl=300)
def index_data():
    out = {}
    for n, t in INDEXES.items():
        try:
            h = yf.Ticker(t).history(period="2d")
            if len(h)>=2:
                p = h["Close"].iloc[-1]
                out[n] = {"price": round(p,2), "pct": round(((p-h["Close"].iloc[-2])/h["Close"].iloc[-2])*100,2)}
        except: out[n] = {"price":0,"pct":0}
    return out

@st.cache_data(ttl=600)
def get_bi_movers():
    """Fetch price data for BI analytics using yfinance (free, no API credits)."""
    results = []
    for t in BI_UNIVERSE:
        try:
            h = yf.Ticker(t).history(period="5d")
            if len(h)>=2:
                price = h["Close"].iloc[-1]
                prev  = h["Close"].iloc[-2]
                vol   = h["Volume"].iloc[-1]
                avg_v = h["Volume"].mean()
                pct   = ((price-prev)/prev)*100
                results.append({"ticker":t,"price":round(price,2),"pct":round(pct,2),
                                 "volume":int(vol),"vol_ratio":round(vol/avg_v,1) if avg_v>0 else 1})
        except: continue
    return results

@st.cache_data(ttl=900)
def get_st_most_discussed():
    """Get StockTwits watchlist counts for a set of tickers."""
    targets = ["NVDA","TSLA","AMD","AAPL","MSTR","PLTR","GME","AMC","META","MSFT","AMZN","GOOGL"]
    results = []
    for t in targets:
        s = st_sentiment(t)
        if s.get("wl",0) > 0:
            results.append({"ticker":t,"watchlists":s["wl"],"bull":s["bull"],"msgs":s["msgs"]})
    return sorted(results, key=lambda x:x["watchlists"], reverse=True)[:8]

# ── SCORING ENGINE ────────────────────────────────────────────────────────────
def score_stock(df, info=None, sent=None):
    if df is None or len(df)<20: return 0, {}
    s, bd = 0, {}
    try:
        dfc = df.copy()
        dfc["rsi"]   = ta.momentum.RSIIndicator(dfc["close"],14).rsi()
        dfc["ma20"]  = dfc["close"].rolling(20).mean()
        dfc["ma50"]  = dfc["close"].rolling(min(50,len(dfc))).mean()
        macd         = ta.trend.MACD(dfc["close"])
        dfc["macd"]  = macd.macd()
        dfc["macd_s"]= macd.macd_signal()
        lat = dfc.iloc[-1]

        rsi = lat["rsi"]
        if pd.notna(rsi):
            rs = 25 if rsi<30 else 20 if rsi<40 else 18 if rsi<=55 else 12 if rsi<=70 else 4
            s += rs; bd["RSI"] = rs

        if pd.notna(lat["ma20"]) and pd.notna(lat["ma50"]):
            ts = 0
            if lat["close"]>lat["ma20"]: ts+=8
            if lat["close"]>lat["ma50"]: ts+=8
            if lat["ma20"]>lat["ma50"]:  ts+=4
            s+=ts; bd["Trend"]=ts

        if pd.notna(lat["macd"]) and pd.notna(lat["macd_s"]):
            ms = 15 if (lat["macd"]>lat["macd_s"] and lat["macd"]>0) else 9 if lat["macd"]>lat["macd_s"] else 4 if lat["macd"]>0 else 0
            s+=ms; bd["MACD"]=ms

        if "volume" in dfc.columns:
            avg = dfc["volume"].rolling(20).mean().iloc[-1]
            if pd.notna(avg) and avg>0:
                r = lat["volume"]/avg
                vs = 15 if r>=3 else 11 if r>=2 else 7 if r>=1.5 else 4 if r>=1 else 1
                s+=vs; bd["Volume"]=vs

        if sent:
            bp = sent.get("bull",50)
            ss = 15 if bp>=75 else 10 if bp>=60 else 6 if bp>=50 else 2
            s+=ss; bd["Sentiment"]=ss

        if info:
            sf = (info.get("sf",0) or 0)*100
            dt = info.get("dtc",0) or 0
            sq = 10 if (sf>=20 and dt>=5) else 6 if sf>=15 else 2 if sf>=10 else 0
            s+=sq; bd["Squeeze"]=sq

    except: pass
    return min(int(s),100), bd

# ── PLAIN ENGLISH INSIGHTS ────────────────────────────────────────────────────
def insights(df, info=None):
    out = []
    if df is None or len(df)<20: return out
    try:
        dfc = df.copy()
        dfc["rsi"]   = ta.momentum.RSIIndicator(dfc["close"],14).rsi()
        dfc["ma20"]  = dfc["close"].rolling(20).mean()
        dfc["ma50"]  = dfc["close"].rolling(min(50,len(dfc))).mean()
        macd         = ta.trend.MACD(dfc["close"])
        dfc["macd"]  = macd.macd()
        dfc["macd_s"]= macd.macd_signal()
        bb           = ta.volatility.BollingerBands(dfc["close"])
        dfc["bb_p"]  = bb.bollinger_pband()
        lat = dfc.iloc[-1]; prev = dfc.iloc[-2]
        rsi = lat["rsi"]; price = lat["close"]

        if pd.notna(rsi):
            if rsi<30:       out.append(("RSI Oversold","This stock may have fallen too far too fast — historically this can precede a bounce upward.","bull","Medium"))
            elif rsi>70:     out.append(("RSI Overbought","This stock has risen quickly and may face selling pressure or a short-term pullback.","bear","Medium"))
            elif 55<rsi<=70: out.append(("RSI Bullish Momentum","Momentum is strong without being in extreme territory — a constructive signal.","bull","Medium"))
            else:            out.append(("RSI Neutral","Balanced momentum — no extreme buy or sell pressure from RSI right now.","neutral","Low"))

        if pd.notna(lat["ma20"]) and pd.notna(lat["ma50"]):
            if price>lat["ma20"] and price>lat["ma50"]:
                out.append(("Above Key Averages","The stock is trading above both its short and long-term average prices — a sign of a healthy uptrend.","bull","High"))
            elif price<lat["ma20"] and price<lat["ma50"]:
                out.append(("Below Key Averages","The stock is below its recent average prices, suggesting the current trend is pointing downward.","bear","High"))
            if prev["ma20"]<prev["ma50"] and lat["ma20"]>lat["ma50"]:
                out.append(("Golden Cross ✨","A major bullish event: the short-term trend just crossed above the long-term trend — often treated as a strong buy signal.","bull","High"))
            elif prev["ma20"]>prev["ma50"] and lat["ma20"]<lat["ma50"]:
                out.append(("Death Cross 💀","A major bearish signal: the short-term trend crossed below the long-term trend — the downtrend may be accelerating.","bear","High"))

        if pd.notna(lat["macd"]) and pd.notna(lat["macd_s"]):
            if lat["macd"]>lat["macd_s"] and prev["macd"]<=prev["macd_s"]:
                out.append(("MACD Bullish Crossover","Momentum just flipped positive — more buyers than sellers are entering the market right now.","bull","High"))
            elif lat["macd"]<lat["macd_s"] and prev["macd"]>=prev["macd_s"]:
                out.append(("MACD Bearish Crossover","Momentum just turned negative — selling pressure is increasing.","bear","High"))
            elif lat["macd"]>0:
                out.append(("MACD Bullish","Overall momentum is positive — buyers appear to be in control.","bull","Medium"))
            else:
                out.append(("MACD Bearish","Overall momentum is negative — sellers appear to be in control.","bear","Medium"))

        if "volume" in dfc.columns:
            avg = dfc["volume"].rolling(20).mean().iloc[-1]
            if pd.notna(avg) and avg>0:
                r = lat["volume"]/avg
                if r>=2:
                    d_ = "bull" if lat["close"]>prev["close"] else "bear"
                    out.append(("Volume Spike 🔊",f"Trading volume is {r:.1f}x above normal today — unusually strong interest. High-volume moves tend to carry more conviction.",d_,"High"))
                elif r<0.5:
                    out.append(("Low Volume","Very few traders are active in this stock. Low-volume moves can be unreliable and easy to reverse.","neutral","Low"))

        if info:
            sf  = (info.get("sf",0) or 0)*100
            dtc = info.get("dtc",0) or 0
            if sf>=20:
                out.append(("High Short Interest 🎯",f"{sf:.1f}% of shares are sold short. If the stock rises, short sellers are forced to buy back shares — potentially accelerating the move (short squeeze).","bull","High"))
            if dtc>=5:
                out.append(("High Days-to-Cover",f"It would take ~{dtc:.0f} days at average trading volume to close all short positions. This adds fuel for a potential squeeze.","bull","Medium"))

        if pd.notna(lat["bb_p"]):
            if lat["bb_p"]<0:
                out.append(("Near Lower Bollinger Band","The stock is near the bottom edge of its typical price range — historically this can precede a bounce.","bull","Medium"))
            elif lat["bb_p"]>1:
                out.append(("Near Upper Bollinger Band","The stock is at the top of its normal range — it may be stretched to the upside and could face resistance.","bear","Medium"))
    except: pass
    return out

def get_risk_level(df, info):
    """Determine risk level for a stock based on volatility and fundamentals."""
    try:
        if df is None or len(df)<10: return "Unknown"
        beta = info.get("beta",1) or 1
        vol  = df["close"].pct_change().std()*100
        sf   = (info.get("sf",0) or 0)*100
        mc   = info.get("mktcap",0) or 0
        risk_score = 0
        if beta>2: risk_score+=3
        elif beta>1.5: risk_score+=2
        elif beta>1: risk_score+=1
        if vol>4: risk_score+=3
        elif vol>2: risk_score+=2
        elif vol>1: risk_score+=1
        if sf>20: risk_score+=2
        elif sf>10: risk_score+=1
        if mc<500e6: risk_score+=2
        elif mc<2e9: risk_score+=1
        if risk_score>=6: return "Very High"
        if risk_score>=4: return "High"
        if risk_score>=2: return "Medium"
        return "Low"
    except: return "Unknown"

# ── UI COMPONENTS ─────────────────────────────────────────────────────────────
def score_badge_html(sc):
    c  = "#4ade80" if sc>=65 else "#fbbf24" if sc>=40 else "#f87171"
    bg = "#052e16" if sc>=65 else "#1a1100" if sc>=40 else "#450a0a"
    lbl= "Strong" if sc>=65 else "Moderate" if sc>=40 else "Weak"
    return f'<div style="background:{bg};border:1px solid {c};border-radius:10px;padding:10px 14px;text-align:center;display:inline-block;min-width:90px;"><div style="font-family:\'Space Mono\',monospace;font-size:24px;font-weight:700;color:{c};">{sc}</div><div style="font-size:10px;color:{c};text-transform:uppercase;letter-spacing:1px;">{lbl}</div></div>'

def risk_badge_html(risk):
    mapping = {"Low":"#4ade80","Low-Medium":"#86efac","Medium":"#fbbf24","Medium-High":"#fb923c","High":"#f87171","Very High":"#ef4444","Unknown":"#94a3b8"}
    c = mapping.get(risk,"#94a3b8")
    return f'<span style="color:{c};font-weight:700;font-size:12px;">⚡ Risk: {risk}</span>'

def render_insight_row(label, text, sentiment, confidence):
    cls = "insight-bull" if sentiment=="bull" else "insight-bear" if sentiment=="bear" else ""
    bc  = "badge-bull" if sentiment=="bull" else "badge-bear" if sentiment=="bear" else "badge-neutral"
    bl  = "Bullish" if sentiment=="bull" else "Bearish" if sentiment=="bear" else "Neutral"
    st.markdown(f"""<div class="insight-row {cls}">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
            <span style="font-weight:700;font-size:13px;color:#e2e8f0;">{label}</span>
            <span class="badge {bc}">{bl}</span>
            <span style="font-size:11px;color:#475569;">Confidence: {confidence}</span>
        </div>
        <div style="font-size:13px;color:#64748b;line-height:1.6;">{text}</div>
    </div>""", unsafe_allow_html=True)

def render_lock(name="This Feature"):
    st.markdown(f"""<div class="lock-box">
        <div style="font-size:36px;margin-bottom:12px;">🔒</div>
        <div style="font-size:20px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">{name} — Premium Only</div>
        <div style="font-size:14px;color:#475569;margin-bottom:4px;">Upgrade to unlock advanced analytics, all 17+ categories, and deeper signals.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Upgrade to Premium →", type="primary", key=f"lock_{name}"):
        nav("pricing")

def render_stock_card(ticker, quote, sc, insigs, hot=False, risk=""):
    if not quote: return
    pct   = quote.get("chg_pct",0)
    price = quote.get("price",0)
    cc    = "#4ade80" if pct>=0 else "#f87171"
    arr   = "▲" if pct>=0 else "▼"
    sc_c  = "#4ade80" if sc>=65 else "#fbbf24" if sc>=40 else "#f87171"
    sc_bg = "#052e16" if sc>=65 else "#1a1100" if sc>=40 else "#450a0a"
    hot_b = '<span class="badge badge-hot" style="margin-right:6px;">🔥 HOT</span>' if hot else ""
    sigs  = "".join([f'<span class="badge badge-{"bull" if s=="bull" else "bear" if s=="bear" else "neutral"}" style="margin-right:4px;font-size:10px;">{l[:16]}</span>' for l,_,s,_ in insigs[:2]])
    risk_c= "#4ade80" if risk=="Low" else "#86efac" if risk=="Low-Medium" else "#fbbf24" if risk=="Medium" else "#fb923c" if risk=="Medium-High" else "#f87171"

    st.markdown(f"""<div class="sw-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
            <div>
                {hot_b}<span class="ticker-sym">{ticker}</span>
                <div style="font-size:11px;color:#475569;margin-top:3px;">{quote.get('name','')[:26]}</div>
                {f'<div style="font-size:11px;color:{risk_c};margin-top:2px;">⚡ {risk} Risk</div>' if risk else ''}
            </div>
            <div style="text-align:right;">
                <div style="font-family:\'Space Mono\',monospace;font-size:20px;font-weight:700;color:#f1f5f9;">${price:,.2f}</div>
                <div style="font-size:13px;font-weight:700;color:{cc};">{arr} {abs(pct):.2f}%</div>
            </div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div style="flex:1;">{sigs}</div>
            <div style="background:{sc_bg};border:1px solid {sc_c};border-radius:8px;padding:4px 12px;font-family:\'Space Mono\',monospace;font-size:17px;font-weight:700;color:{sc_c};">{sc}</div>
        </div>
    </div>""", unsafe_allow_html=True)

def render_topbar(active=""):
    c1,c2,c3 = st.columns([2,6,3])
    with c1:
        if st.button("📈 StockWins", key="logo_btn"):
            nav("landing" if not is_authed() else "dashboard")
    with c2:
        if is_authed():
            nav_items = [("Dashboard","dashboard"),("Discover","discover"),("Watchlist","watchlist"),
                         ("Screener","screener"),("BI Analytics","bi_dashboard"),("Pricing","pricing")]
            cols = st.columns(len(nav_items))
            for col,(lbl,pg) in zip(cols,nav_items):
                with col:
                    if st.button(lbl, key=f"nav_{pg}",
                                 type="primary" if active==pg else "secondary"):
                        nav(pg)
    with c3:
        if is_authed():
            cc1,cc2,cc3 = st.columns([2,1,1])
            role_icon = "👑" if is_premium() else "🆓"
            with cc1:
                st.markdown(f'<div style="font-size:12px;color:#475569;padding-top:10px;">{role_icon} {st.session_state.user["name"]}</div>', unsafe_allow_html=True)
            with cc2:
                if st.button("⚙️", key="settings_btn", help="Settings"):
                    nav("settings")
            with cc3:
                if st.button("Out", key="logout_btn"):
                    logout()
        else:
            cc1,cc2 = st.columns(2)
            with cc1:
                if st.button("Login", key="nav_login"): nav("login")
            with cc2:
                if st.button("Sign Up", key="nav_signup", type="primary"): nav("signup")
    st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LANDING
# ═══════════════════════════════════════════════════════════════════════════════
def page_landing():
    # Minimal topbar for landing
    tc1,_,tc2 = st.columns([2,5,3])
    with tc1:
        st.markdown('<div class="sw-logo">Stock<span>Wins</span></div>', unsafe_allow_html=True)
    with tc2:
        lc1,lc2 = st.columns(2)
        with lc1:
            if st.button("Login", key="land_login"): nav("login")
        with lc2:
            if st.button("Sign Up", key="land_signup", type="primary"): nav("signup")
    st.divider()

    # Hero
    st.markdown("""<div class="hero">
        <div class="hero-eyebrow">Smart Stock Discovery Platform</div>
        <div class="hero-title">Find Your Next Big Trade<br><span class="accent">Before The Crowd Does</span></div>
        <div class="hero-sub">Real-time signals, plain-English insights, social sentiment, BI dashboards, and short squeeze detection — all in one premium platform built for serious traders.</div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("🚀 Start Free — No Card", type="primary", use_container_width=True): nav("signup")
    with c2:
        if st.button("📊 View Dashboard", use_container_width=True): nav("login")
    with c3:
        if st.button("💰 See Pricing", use_container_width=True): nav("pricing")

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats
    for col,v,l in zip(st.columns(4),["17+","5,000+","Real-Time","$0"],["Stock Categories","Stocks Covered","Sentiment Data","To Get Started"]):
        col.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#3b82f6;">{v}</div><div class="stat-lbl">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Features
    st.markdown('<div class="section-hd">Everything You Need to Trade Smarter</div>', unsafe_allow_html=True)
    feats = [
        ("📡","Live Sentiment Signals","Track what thousands of traders are saying in real time — know when the crowd turns bullish or bearish before it moves the price."),
        ("💬","Plain-English Insights","Every RSI, MACD, and moving average signal is translated into clear, beginner-friendly language you can actually act on."),
        ("💥","Short Squeeze Scanner","Automatically identify high short-interest stocks that could explode when shorts are forced to cover their positions."),
        ("📊","BI-Style Dashboards","Professional sector heatmaps, index trackers, volume leaders, and momentum leaderboards — like a Bloomberg terminal, simplified."),
        ("🔊","Volume Surge Detection","Know the instant unusual trading activity hits a stock — often the earliest signal of a major move incoming."),
        ("🎯","Scoring Engine (0–100)","Every stock gets a StockWins Score combining RSI, trend, MACD, volume, social sentiment, and short squeeze potential."),
    ]
    for i in range(0,len(feats),3):
        cols = st.columns(3)
        for j,col in enumerate(cols):
            if i+j<len(feats):
                icon,title,desc = feats[i+j]
                col.markdown(f'<div class="sw-card"><div style="font-size:28px;margin-bottom:10px;">{icon}</div><div style="font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:6px;">{title}</div><div style="font-size:13px;color:#475569;line-height:1.6;">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # BI Analytics preview
    st.markdown('<div class="section-hd">BI Analytics & Market Intelligence</div>', unsafe_allow_html=True)
    bi_feats = [
        ("📈 Sector Comparisons","Compare all 10 S&P sectors by daily performance with visual heatmaps."),
        ("🏆 Leaderboards","Top gainers, losers, volume leaders, and most improved sentiment — updated continuously."),
        ("🧠 Trend Dashboards","Track which themes and sectors are gaining or losing momentum over time."),
        ("🔍 Screener Outputs","Run multi-factor screens and display results visually with charts and tables."),
        ("📡 Sentiment Dashboards","Track social media sentiment trends across individual stocks and sectors."),
        ("⚡ Volume Surge Alerts","Real-time alerts for stocks experiencing unusual volume spikes."),
    ]
    for i in range(0,len(bi_feats),3):
        cols = st.columns(3)
        for j,col in enumerate(cols):
            if i+j<len(bi_feats):
                title,desc = bi_feats[i+j]
                col.markdown(f'<div class="sw-card"><div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:6px;">{title}</div><div style="font-size:13px;color:#475569;">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Categories
    st.markdown('<div class="section-hd">17+ Curated Stock Categories</div>', unsafe_allow_html=True)
    cats = list(CATEGORIES.keys()) + ["📅 Earnings Watch","🌐 Sector Leaders","💰 Dividend Stocks"]
    st.markdown('<div style="line-height:2.8;">'+"".join([f'<span style="background:#111827;border:1px solid #1e2a3a;border-radius:20px;padding:6px 14px;margin:3px;font-size:13px;display:inline-block;">{c}</span>' for c in cats])+'</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # How it works
    st.markdown('<div class="section-hd">How It Works</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col,(n,t,d) in zip(cols,[("1","Sign Up Free","Create your account in 30 seconds — no credit card needed."),
        ("2","Browse Categories","Explore 17+ curated stock categories filtered by theme, momentum, and sentiment."),
        ("3","Read Plain Signals","Every stock comes with easy-to-understand insights — no finance degree required."),
        ("4","Upgrade for More","Unlock squeeze scanner, advanced screener, and full BI analytics with Premium.")]):
        col.markdown(f'<div class="sw-card" style="text-align:center;"><div style="font-family:\'Space Mono\',monospace;font-size:28px;font-weight:700;color:#3b82f6;margin-bottom:10px;">{n}</div><div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:6px;">{t}</div><div style="font-size:12px;color:#475569;">{d}</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Plain-English translation examples
    st.markdown('<div class="section-hd">Plain-English Translations — Examples</div>', unsafe_allow_html=True)
    examples = [
        ("RSI Overbought","📉 Bearish","This stock may have risen too quickly and could be due for a pullback."),
        ("RSI Oversold","📈 Bullish","This stock may have fallen too far too fast and could be due for a rebound."),
        ("Price Above Moving Average","📈 Bullish","The stock is trending upward and staying above its recent average price."),
        ("Volume Spike","🔊 Attention","More traders than usual are active in this stock — may signal stronger interest."),
        ("Breakout","🚀 Bullish","The stock is pushing above an important price level — can lead to further upside."),
        ("Golden Cross","✨ Strong Bullish","The short-term trend just crossed above the long-term trend — a major buy signal."),
    ]
    for i in range(0,len(examples),3):
        cols = st.columns(3)
        for j,col in enumerate(cols):
            if i+j<len(examples):
                tech,tag,plain = examples[i+j]
                col.markdown(f'<div class="sw-card"><div style="font-size:12px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">{tech}</div><div style="font-size:12px;color:#3b82f6;margin-bottom:8px;">{tag}</div><div style="font-size:13px;color:#94a3b8;font-style:italic;">"{plain}"</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div class="section-hd">What Traders Are Saying</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col,(stars,text,name) in zip(cols,[
        ("⭐⭐⭐⭐⭐","The plain-English explanations changed how I analyze stocks. I finally understand what these indicators mean for my trades.","Michael T., Active Trader"),
        ("⭐⭐⭐⭐⭐","The short squeeze scanner caught several huge movers early. The Premium subscription paid for itself in the first week.","Sarah K., Day Trader"),
        ("⭐⭐⭐⭐⭐","Combining StockTwits sentiment with technical signals is powerful. The BI dashboards feel like a Bloomberg terminal but actually simple.","David R., Swing Trader")]):
        col.markdown(f'<div class="sw-card"><div style="margin-bottom:8px;">{stars}</div><div style="font-size:13px;color:#475569;line-height:1.6;margin-bottom:12px;">"{text}"</div><div style="font-size:12px;font-weight:600;color:#3b82f6;">— {name}</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Pricing
    st.markdown('<div class="section-hd">Simple, Transparent Pricing</div>', unsafe_allow_html=True)
    p1,p2,p3 = st.columns([1,1.15,1])
    with p1:
        st.markdown("""<div class="pricing-card"><div style="font-size:16px;font-weight:700;color:#f1f5f9;">Free</div>
            <div class="pricing-price">$0</div><div style="font-size:12px;color:#475569;margin-bottom:16px;">forever</div>
            <hr style="border-color:#1e2a3a;">
            <div style="font-size:13px;color:#475569;line-height:2.2;margin-top:14px;">
            ✅ Market overview dashboard<br>✅ 5 stock categories<br>✅ StockTwits hot list<br>
            ✅ Basic RSI & MACD signals<br>✅ Plain-English insights<br>✅ Basic watchlist<br>
            ❌ Short squeeze scanner<br>❌ Advanced screener<br>❌ Full BI analytics<br>
            ❌ Premium categories<br>❌ Score breakdowns</div></div>""", unsafe_allow_html=True)
    with p2:
        st.markdown("""<div class="pricing-featured">
            <div style="background:#3b82f6;color:white;font-size:10px;font-weight:700;padding:3px 12px;border-radius:20px;display:inline-block;margin-bottom:10px;letter-spacing:1.5px;">⭐ MOST POPULAR</div>
            <div style="font-size:16px;font-weight:700;color:#f1f5f9;">Premium Monthly</div>
            <div class="pricing-price">$29</div><div style="font-size:12px;color:#475569;margin-bottom:16px;">per month · cancel anytime</div>
            <hr style="border-color:#1e2a3a;">
            <div style="font-size:13px;color:#475569;line-height:2.2;margin-top:14px;">
            ✅ Everything in Free<br>✅ All 17+ stock categories<br>✅ Short squeeze scanner<br>
            ✅ Advanced screener<br>✅ Full BI dashboards<br>✅ Score breakdowns<br>
            ✅ Volume surge alerts<br>✅ Breakout candidates<br>✅ Momentum scanner<br>
            ✅ Oversold bounce scanner<br>✅ Unlimited watchlist</div></div>""", unsafe_allow_html=True)
    with p3:
        st.markdown("""<div class="pricing-card">
            <div style="background:linear-gradient(90deg,#854d0e,#d97706);color:white;font-size:10px;font-weight:700;padding:3px 12px;border-radius:20px;display:inline-block;margin-bottom:4px;letter-spacing:1px;">BEST VALUE</div>
            <div style="font-size:16px;font-weight:700;color:#f1f5f9;">Annual Plan</div>
            <div class="pricing-price">$199</div><div style="font-size:12px;color:#475569;margin-bottom:16px;">per year · save 43%</div>
            <hr style="border-color:#1e2a3a;">
            <div style="font-size:13px;color:#475569;line-height:2.2;margin-top:14px;">
            ✅ Everything in Premium<br>✅ Priority support<br>✅ Early feature access<br>
            ✅ Export data to CSV<br>✅ Custom price alerts<br>✅ API access (Q3 2026)<br>
            ✅ Backtesting (coming)<br>✅ Portfolio tracker (coming)</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _,cc,_ = st.columns([1,1,1])
    with cc:
        if st.button("🚀 Start Free Today", type="primary", use_container_width=True): nav("signup")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # FAQ
    st.markdown('<div class="section-hd">Frequently Asked Questions</div>', unsafe_allow_html=True)
    for q,a in [
        ("Is this financial advice?","No. StockWins is an educational data analysis tool. All signals, scores, and insights are algorithmic outputs for informational purposes only. Always consult a licensed financial advisor before making investment decisions."),
        ("How is the StockWins Score calculated?","The 0–100 score combines RSI momentum (0–25 pts), price vs moving averages (0–20 pts), MACD momentum (0–15 pts), volume activity (0–15 pts), social sentiment from StockTwits (0–15 pts), and short squeeze potential (0–10 pts)."),
        ("Where does data come from?","We use Twelve Data for real-time and historical price data, Yahoo Finance for fundamental data (short interest, market cap, etc.), and StockTwits for live social sentiment signals."),
        ("What does the short squeeze scanner look for?","It scans a broad universe for stocks with high short float % and high days-to-cover — the two primary ingredients for a potential squeeze event. Educational, not advice."),
        ("Can I cancel my subscription?","Yes. Cancel anytime. Your premium access remains active through the end of your billing period."),
        ("Are there data delays?","Twelve Data free tier may have 15-minute delays. Yahoo Finance fundamental data is updated periodically. StockTwits data is near real-time."),
    ]:
        with st.expander(q):
            st.markdown(f'<div style="color:#475569;font-size:13px;line-height:1.7;">{a}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""<div class="footer">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;margin-bottom:16px;">
            <div><div class="sw-logo" style="margin-bottom:6px;">Stock<span>Wins</span></div><div style="font-size:12px;color:#475569;">Smart Stock Analysis & Discovery Platform</div></div>
            <div style="font-size:12px;color:#475569;line-height:2;">Privacy Policy · Terms of Service · Risk Disclaimer · Contact Us</div>
        </div>
        <div class="disclaimer">
        ⚠️ <strong>Risk Disclaimer:</strong> Trading stocks and securities involves substantial risk of financial loss. StockWins provides algorithmic, data-driven educational content only. Nothing on this platform constitutes financial, investment, legal, or tax advice. All signals and scores are generated by automated algorithms and may be inaccurate or delayed. Past performance does not guarantee future results. Always conduct your own due diligence and consult with a licensed financial professional before any investment decision. We are not liable for any losses incurred from use of this platform.
        </div>
        <div style="font-size:11px;color:#1e2a3a;margin-top:12px;text-align:right;">© 2026 StockWins. All rights reserved.</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
def page_login():
    render_topbar()
    _,cc,_ = st.columns([1,2,1])
    with cc:
        st.markdown('<div style="text-align:center;margin-bottom:28px;"><div style="font-size:26px;font-weight:800;color:#f1f5f9;">Welcome Back 👋</div><div style="font-size:14px;color:#475569;margin-top:6px;">Sign in to your StockWins account</div></div>', unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email address", placeholder="you@example.com")
            pw    = st.text_input("Password", type="password", placeholder="••••••••")
            sub   = st.form_submit_button("Sign In →", type="primary", use_container_width=True)
            if sub:
                if login(email, pw): nav("dashboard")
                else: st.error("Invalid email or password.")
        st.markdown("""<div style="background:#0d1220;border:1px solid #1e2a3a;border-radius:8px;padding:14px;margin-top:12px;font-size:12px;color:#475569;">
            <span style="color:#3b82f6;font-weight:600;">Demo accounts:</span><br>
            Free: demo@stockwins.com / demo123<br>
            Premium: premium@stockwins.com / premium1</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Don't have an account? Create one free →", use_container_width=True): nav("signup")
        if st.button("Forgot password?", use_container_width=True): nav("forgot_password")
        if st.button("← Back to Home", use_container_width=True): nav("landing")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SIGNUP
# ═══════════════════════════════════════════════════════════════════════════════
def page_signup():
    render_topbar()
    _,cc,_ = st.columns([1,2,1])
    with cc:
        st.markdown('<div style="text-align:center;margin-bottom:28px;"><div style="font-size:26px;font-weight:800;color:#f1f5f9;">Create Your Account 🚀</div><div style="font-size:14px;color:#475569;margin-top:6px;">Free forever. No credit card required.</div></div>', unsafe_allow_html=True)
        with st.form("signup_form"):
            name  = st.text_input("Full name", placeholder="Jane Doe")
            email = st.text_input("Email address", placeholder="you@example.com")
            pw    = st.text_input("Password", type="password", placeholder="Min 6 characters")
            pw2   = st.text_input("Confirm password", type="password", placeholder="Repeat password")
            agree = st.checkbox("I agree to the Terms of Service and understand this is not financial advice.")
            sub   = st.form_submit_button("Create Free Account →", type="primary", use_container_width=True)
            if sub:
                if not all([name,email,pw,pw2]):  st.error("Please fill in all fields.")
                elif pw!=pw2:                      st.error("Passwords don't match.")
                elif len(pw)<6:                    st.error("Password must be at least 6 characters.")
                elif not agree:                    st.error("Please agree to the Terms of Service.")
                else:
                    ok,msg = signup(email,pw,name)
                    if ok:
                        st.success(f"✅ Welcome, {name}! Redirecting to your dashboard...")
                        time.sleep(0.8); nav("verify_email")
                    else: st.error(msg)
        if st.button("Already have an account? Sign In", use_container_width=True): nav("login")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EMAIL VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def page_verify_email():
    render_topbar()
    _,cc,_ = st.columns([1,2,1])
    with cc:
        st.markdown("""<div class="sw-card" style="text-align:center;padding:48px 32px;">
            <div style="font-size:48px;margin-bottom:16px;">📧</div>
            <div style="font-size:22px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">Check Your Email</div>
            <div style="font-size:14px;color:#475569;line-height:1.7;margin-bottom:24px;">
            We've sent a verification link to your email address.<br>
            Click the link to verify your account and unlock all features.<br><br>
            <span style="color:#94a3b8;font-size:12px;">(In this demo, verification is simulated)</span>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("✅ I've Verified My Email — Continue to Dashboard", type="primary", use_container_width=True):
            # Mark as verified in demo
            email = st.session_state.user["email"] if is_authed() else ""
            if email and email in st.session_state.users_db:
                st.session_state.users_db[email]["verified"] = True
            nav("dashboard")
        if st.button("Resend Verification Email", use_container_width=True):
            st.info("Verification email resent! (simulated in demo)")
        if st.button("Skip for now — Go to Dashboard", use_container_width=True):
            nav("dashboard")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FORGOT PASSWORD
# ═══════════════════════════════════════════════════════════════════════════════
def page_forgot_password():
    render_topbar()
    _,cc,_ = st.columns([1,2,1])
    with cc:
        st.markdown('<div style="text-align:center;margin-bottom:28px;"><div style="font-size:22px;font-weight:800;color:#f1f5f9;">Reset Your Password 🔑</div><div style="font-size:14px;color:#475569;margin-top:6px;">Enter your email to receive a reset link.</div></div>', unsafe_allow_html=True)
        with st.form("forgot_form"):
            email = st.text_input("Email address", placeholder="you@example.com")
            sub   = st.form_submit_button("Send Reset Link →", type="primary", use_container_width=True)
            if sub:
                if email in st.session_state.users_db:
                    st.success("✅ Reset link sent! Check your email. (Simulated in demo)")
                    time.sleep(1)
                    nav("login")
                else:
                    st.error("No account found with that email address.")
        if st.button("← Back to Login", use_container_width=True): nav("login")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    render_topbar("dashboard")
    api = get_key()
    if not api:
        _render_api_key_setup()
        return

    # Verification banner
    db_user = get_user_db()
    if not db_user.get("verified", True):
        st.markdown('<div style="background:#1a2744;border:1px solid #3b82f6;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:#60a5fa;">📧 Please verify your email address to unlock all features. <a href="#" style="color:#93c5fd;">Resend verification →</a></div>', unsafe_allow_html=True)

    # ── Market Overview ──────────────────────────────────────────────────────
    st.markdown('<div class="section-hd">📊 Market Overview</div>', unsafe_allow_html=True)

    with st.spinner("Loading market data..."):
        idx  = index_data()
        secs = sector_perf()

    # Index widgets
    cols = st.columns(len(idx))
    for col,(name,d) in zip(cols,idx.items()):
        c = "#4ade80" if d["pct"]>=0 else "#f87171"
        a = "▲" if d["pct"]>=0 else "▼"
        col.markdown(f'<div class="stat-box"><div style="font-size:11px;color:#475569;margin-bottom:4px;">{name}</div><div class="stat-val">{d["price"]:,.2f}</div><div style="font-size:12px;font-weight:700;color:{c};">{a} {abs(d["pct"]):.2f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs: Sector | Movers | Sentiment ────────────────────────────────────
    t1,t2,t3 = st.tabs(["🗺️ Sector Heatmap","📈 Top Movers","📡 Market Sentiment"])

    with t1:
        sec_cols = st.columns(len(secs))
        for col,(sec,chg) in zip(sec_cols,secs.items()):
            cls = "heat-pos" if chg>0.15 else "heat-neg" if chg<-0.15 else "heat-neu"
            a   = "▲" if chg>=0 else "▼"
            col.markdown(f'<div class="{cls}"><div style="font-size:10px;">{sec}</div><div>{a}{abs(chg):.2f}%</div></div>', unsafe_allow_html=True)

    with t2:
        with st.spinner("Fetching top movers..."):
            movers = get_bi_movers()
        if movers:
            gainers = sorted(movers, key=lambda x:x["pct"], reverse=True)[:5]
            losers  = sorted(movers, key=lambda x:x["pct"])[:5]
            vol_ldrs= sorted(movers, key=lambda x:x["vol_ratio"], reverse=True)[:5]

            mc1,mc2,mc3 = st.columns(3)
            with mc1:
                st.markdown('<div style="font-size:13px;font-weight:700;color:#4ade80;margin-bottom:8px;">🟢 Top Gainers</div>', unsafe_allow_html=True)
                for m in gainers:
                    st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:13px;">{m["ticker"]}</span><span style="color:#4ade80;font-weight:700;">▲ {m["pct"]:.2f}%</span></div>', unsafe_allow_html=True)
            with mc2:
                st.markdown('<div style="font-size:13px;font-weight:700;color:#f87171;margin-bottom:8px;">🔴 Top Losers</div>', unsafe_allow_html=True)
                for m in losers:
                    st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:13px;">{m["ticker"]}</span><span style="color:#f87171;font-weight:700;">▼ {abs(m["pct"]):.2f}%</span></div>', unsafe_allow_html=True)
            with mc3:
                st.markdown('<div style="font-size:13px;font-weight:700;color:#60a5fa;margin-bottom:8px;">🔊 Volume Leaders</div>', unsafe_allow_html=True)
                for m in vol_ldrs:
                    st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:13px;">{m["ticker"]}</span><span style="color:#60a5fa;font-weight:700;">{m["vol_ratio"]:.1f}x avg vol</span></div>', unsafe_allow_html=True)

    with t3:
        hot = st_hot()
        sc1,sc2 = st.columns(2)
        with sc1:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">🔥 StockTwits Hot Right Now</div>', unsafe_allow_html=True)
            hot_html = "".join([f'<span style="background:#431407;border:1px solid #9a3412;color:#fb923c;border-radius:20px;padding:5px 12px;margin:3px;font-family:\'Space Mono\',monospace;font-size:12px;display:inline-block;">{t}</span>' for t in hot[:10]])
            st.markdown(f'<div style="line-height:2.5;">{hot_html}</div>', unsafe_allow_html=True)
        with sc2:
            with st.spinner("Loading social sentiment..."):
                discussed = get_st_most_discussed()
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">👥 Most Watchlisted on StockTwits</div>', unsafe_allow_html=True)
            for item in discussed[:5]:
                bull_c = "#4ade80" if item["bull"]>=60 else "#f87171" if item["bull"]<40 else "#94a3b8"
                st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:13px;">{item["ticker"]}</span><span style="font-size:12px;color:#475569;">{item["watchlists"]:,} watching</span><span style="color:{bull_c};font-weight:700;font-size:12px;">{item["bull"]}% bull</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stock Categories ─────────────────────────────────────────────────────
    st.markdown('<div class="section-hd">📈 Stock Categories</div>', unsafe_allow_html=True)
    avail = FREE_CATS if not is_premium() else list(CATEGORIES.keys())
    sel   = st.selectbox("Choose a category to explore", avail, key="dash_cat_sel")

    if sel in PREMIUM_CATS and not is_premium():
        render_lock(sel)
    else:
        render_category(sel, api)


# ═══════════════════════════════════════════════════════════════════════════════
# SHARED: RENDER CATEGORY
# ═══════════════════════════════════════════════════════════════════════════════
def render_category(cat, api, limit=15):
    tickers = list(CATEGORIES.get(cat,[]))
    hot     = st_hot()

    if cat == "🔥 StockTwits Hot":        tickers = hot
    elif cat == "💥 Short Squeeze":       page_squeeze(api); return
    elif cat in PREMIUM_CATS:
        universe = list(set(CATEGORIES["💻 Tech"]+CATEGORIES["🤖 AI"]+CATEGORIES["⚡ EV"]+CATEGORIES["🧬 Biotech"]+CATEGORIES["📊 S&P 500"]+hot[:8]))
        tickers  = universe[:25]

    if not tickers: st.info("No tickers available."); return
    st.caption(f"Analyzing top {min(len(tickers),limit)} stocks · Updates every 10 min")

    scored = []
    prog   = st.progress(0, text=f"Loading {cat}...")
    scan   = min(len(tickers), limit)

    for i,ticker in enumerate(tickers[:scan]):
        prog.progress((i+1)/scan, text=f"Analyzing {ticker}...")
        q    = td_quote(ticker, api)
        df   = td_ohlcv(ticker, api, 60)
        info = yf_info(ticker)
        sent = st_sentiment(ticker)
        sc,_ = score_stock(df, info, sent)
        ig   = insights(df, info)
        risk = get_risk_level(df, info)
        if q:
            scored.append({"t":ticker,"q":q,"sc":sc,"ig":ig,"hot":ticker in hot,"df":df,"info":info,"sent":sent,"risk":risk})

    prog.empty()

    # Dynamic filters
    if cat=="📈 Momentum":        scored=[s for s in scored if s["sc"]>=55]
    elif cat=="📉 Oversold Bounce":
        def is_os(s):
            if s["df"] is None or len(s["df"])<14: return False
            try: r=ta.momentum.RSIIndicator(s["df"]["close"].copy(),14).rsi().iloc[-1]; return pd.notna(r) and r<35
            except: return False
        scored=[s for s in scored if is_os(s)]
    elif cat=="🔊 High Volume":
        def vr(s):
            if s["df"] is None or len(s["df"])<20: return 0
            avg=s["df"]["volume"].rolling(20).mean().iloc[-1]; return s["df"]["volume"].iloc[-1]/avg if avg>0 else 0
        scored=sorted(scored,key=vr,reverse=True)
    elif cat=="🚀 Breakouts":
        def is_bo(s):
            if s["df"] is None or len(s["df"])<50: return False
            try:
                ma50=s["df"]["close"].rolling(50).mean()
                return s["df"]["close"].iloc[-1]>ma50.iloc[-1] and s["df"]["close"].iloc[-2]<=ma50.iloc[-2]
            except: return False
        scored=[s for s in scored if is_bo(s)]

    scored.sort(key=lambda x:x["sc"],reverse=True)
    scored=scored[:12]

    if not scored:
        st.info(f"No stocks currently meeting the criteria for {cat}. Markets change — check back soon.")
        return

    for i in range(0,len(scored),3):
        cols=st.columns(3)
        for j,col in enumerate(cols):
            if i+j<len(scored):
                s=scored[i+j]
                with col:
                    render_stock_card(s["t"],s["q"],s["sc"],s["ig"],s["hot"],s["risk"])
                    ca,cb=st.columns(2)
                    with ca:
                        if st.button("📊 Details",key=f"d_{s['t']}_{cat}",use_container_width=True):
                            st.session_state.detail_ticker=s["t"]
                            st.session_state.detail_data=s
                            nav("stock_detail")
                    with cb:
                        wl=st.session_state.watchlist
                        in_wl=s["t"] in wl
                        if st.button("✅ Watching" if in_wl else "➕ Watch",key=f"w_{s['t']}_{cat}",use_container_width=True):
                            if in_wl: wl.remove(s["t"])
                            else:     wl.append(s["t"])
                            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SHORT SQUEEZE SCANNER
# ═══════════════════════════════════════════════════════════════════════════════
def page_squeeze(api):
    st.markdown('<div class="section-hd">💥 Short Squeeze Scanner</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight-row insight-bull">
        <strong>How Short Squeezes Work:</strong> When a large % of a stock's float is sold short (traders betting price falls) and the stock starts rising, those traders are forced to buy shares to limit losses. This forced buying accelerates the move — that's a short squeeze. High short float + high days-to-cover = highest squeeze potential.
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: min_sf  = st.slider("Min Short Float %",10,40,20)
    with c2: min_dtc = st.slider("Min Days to Cover",1,10,3)
    with c3: sort_by = st.selectbox("Sort By",["SW Score","Short Float %","Days to Cover"])

    universe = list(set(CATEGORIES["💻 Tech"]+CATEGORIES["🤖 AI"]+CATEGORIES["⚡ EV"]+
                        CATEGORIES["🧬 Biotech"]+CATEGORIES["🎭 Meme / Social"]+
                        CATEGORIES["🔬 Small Cap"]+st_hot()))[:40]

    if st.button("🔍 Run Squeeze Scan", type="primary"):
        results = []
        prog = st.progress(0,"Scanning for squeeze candidates...")
        for i,t in enumerate(universe):
            prog.progress((i+1)/len(universe),f"Checking {t}...")
            try:
                info=yf_info(t)
                sf=(info.get("sf",0) or 0)*100
                dtc=info.get("dtc",0) or 0
                if sf>=min_sf and dtc>=min_dtc:
                    q=td_quote(t,api)
                    df=td_ohlcv(t,api,60)
                    sent=st_sentiment(t)
                    sc,_=score_stock(df,info,sent)
                    mc=info.get("mktcap",0)
                    results.append({
                        "Ticker":t,"Price":f"${q['price']:,.2f}" if q else "N/A",
                        "Short Float %":f"{sf:.1f}%","Days to Cover":f"{dtc:.1f}",
                        "Mkt Cap":f"${mc/1e9:.2f}B" if mc else "N/A",
                        "SW Score":sc,"Bullish Sent.":f"{sent.get('bull',50)}%",
                        "_sc":sc,"_sf":sf,"_dtc":dtc,"_t":t
                    })
            except: continue
        prog.empty()

        if not results: st.info(f"No stocks found with >{min_sf}% short float and >{min_dtc} days to cover."); return

        sort_map = {"SW Score":"_sc","Short Float %":"_sf","Days to Cover":"_dtc"}
        results  = sorted(results, key=lambda x:x[sort_map[sort_by]], reverse=True)
        st.success(f"🔥 Found {len(results)} potential squeeze candidates!")

        df_out = pd.DataFrame([{k:v for k,v in r.items() if not k.startswith("_")} for r in results])
        st.dataframe(df_out, use_container_width=True, hide_index=True)

        # Top 3 detail cards
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin:20px 0 10px;">Top 3 Candidates</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for col,r in zip(cols, results[:3]):
            sc_c = "#4ade80" if r["_sc"]>=65 else "#fbbf24" if r["_sc"]>=40 else "#f87171"
            col.markdown(f"""<div class="sw-card-blue">
                <span class="ticker-sym">{r['_t']}</span>
                <div style="margin:14px 0 6px;"><div style="font-size:10px;color:#475569;">SHORT FLOAT</div>
                <div style="font-family:'Space Mono',monospace;font-size:22px;font-weight:700;color:#f87171;">{r['Short Float %']}</div></div>
                <div style="margin:6px 0;"><div style="font-size:10px;color:#475569;">DAYS TO COVER</div>
                <div style="font-family:'Space Mono',monospace;font-size:18px;font-weight:700;color:#fbbf24;">{r['Days to Cover']}</div></div>
                <div style="margin:6px 0;"><div style="font-size:10px;color:#475569;">SW SCORE</div>
                <div style="font-family:'Space Mono',monospace;font-size:20px;font-weight:700;color:{sc_c};">{r['_sc']}/100</div></div>
                <div style="font-size:11px;color:#475569;margin-top:8px;">Bullish Sentiment: {r['Bullish Sent.']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="disclaimer">⚠️ Short squeeze data from Yahoo Finance may be delayed. High short interest does not guarantee a squeeze. For educational analysis only.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: STOCK DETAIL
# ═══════════════════════════════════════════════════════════════════════════════
def page_detail():
    render_topbar()
    ticker = st.session_state.get("detail_ticker")
    data   = st.session_state.get("detail_data",{})
    api    = get_key()

    if st.button("← Back", key="back_from_detail"):
        nav(st.session_state.get("prev_page","dashboard"))

    if not ticker: st.warning("No stock selected."); return

    q    = data.get("q") or td_quote(ticker, api)
    df   = data.get("df") or td_ohlcv(ticker, api, 90)
    info = data.get("info") or yf_info(ticker)
    sent = data.get("sent") or st_sentiment(ticker)
    sc, bd = score_stock(df, info, sent)
    ig     = insights(df, info)
    hot    = ticker in st_hot()
    risk   = get_risk_level(df, info)

    if not q:
        st.error(f"Could not load data for {ticker}. Check API key or rate limits.")
        return

    pct   = q.get("chg_pct",0)
    price = q.get("price",0)
    cc    = "#4ade80" if pct>=0 else "#f87171"
    arr   = "▲" if pct>=0 else "▼"

    # ── Header ──
    h1,h2,h3 = st.columns([3,2,2])
    with h1:
        hot_b = '<span class="badge badge-hot" style="margin-right:8px;">🔥 HOT</span>' if hot else ""
        risk_c = "#4ade80" if risk in ("Low","Low-Medium") else "#fbbf24" if risk=="Medium" else "#fb923c" if risk=="Medium-High" else "#f87171"
        st.markdown(f"""<div style="padding:8px 0;">
            {hot_b}<span class="ticker-sym" style="font-size:26px;">{ticker}</span>
            <div style="font-size:15px;color:#64748b;margin-top:4px;">{q.get('name','')}</div>
            <div style="font-size:12px;color:#334155;margin-top:2px;">{info.get('sector','N/A')} · {info.get('industry','N/A')}</div>
            <div style="font-size:12px;color:{risk_c};margin-top:4px;font-weight:700;">⚡ Risk Level: {risk}</div>
        </div>""", unsafe_allow_html=True)
    with h2:
        st.markdown(f"""<div style="text-align:right;padding:8px 0;">
            <div class="price-lg">${price:,.2f}</div>
            <div style="font-size:17px;font-weight:700;color:{cc};">{arr} {abs(pct):.2f}% today</div>
            <div style="font-size:12px;color:#334155;">Prev. close: ${q.get('prev',0):,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with h3:
        st.markdown(score_badge_html(sc), unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;color:#475569;margin-top:6px;text-align:center;">StockWins Score</div>', unsafe_allow_html=True)

    st.divider()

    # ── Stats Grid ──
    mc   = info.get("mktcap",0)
    mc_s = f"${mc/1e12:.2f}T" if mc>=1e12 else f"${mc/1e9:.2f}B" if mc>=1e9 else f"${mc/1e6:.0f}M" if mc>=1e6 else "N/A"
    sf   = (info.get("sf",0) or 0)*100
    stat_items = [
        ("Open",f"${q.get('open',0):,.2f}"),("Day High",f"${q.get('high',0):,.2f}"),
        ("Day Low",f"${q.get('low',0):,.2f}"),("Volume",f"{q.get('volume',0)/1e6:.2f}M"),
        ("Mkt Cap",mc_s),("52W High",f"${info.get('hi52',0):,.2f}"),
        ("52W Low",f"${info.get('lo52',0):,.2f}"),("Beta",f"{info.get('beta','N/A')}"),
        ("P/E Ratio",f"{info.get('pe','N/A')}"),("Short Float",f"{sf:.1f}%"),
    ]
    scols = st.columns(5)
    for i,(lbl,val) in enumerate(stat_items):
        with scols[i%5]:
            st.markdown(f'<div class="stat-box" style="margin-bottom:8px;"><div class="stat-lbl">{lbl}</div><div class="stat-val" style="font-size:15px;">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart + Insights ──
    cc_col, ci_col = st.columns([3,2])
    with cc_col:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">📈 Price History</div>', unsafe_allow_html=True)
        if df is not None and len(df)>1:
            cdf = df[["datetime","close"]].copy().rename(columns={"datetime":"Date","close":"Price"}).set_index("Date")
            st.line_chart(cdf, color="#3b82f6")
        else:
            st.info("Chart unavailable — API may be rate-limited. Try again shortly.")

        # Score breakdown
        if bd:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin:16px 0 8px;">Score Breakdown</div>', unsafe_allow_html=True)
            if is_premium():
                for comp,pts in bd.items():
                    c_ = "#4ade80" if pts>=12 else "#fbbf24" if pts>=6 else "#f87171"
                    st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <div style="width:80px;font-size:11px;color:#475569;">{comp}</div>
                        <div style="flex:1;background:#1e2a3a;border-radius:4px;height:6px;"><div style="background:{c_};width:{pts}%;height:6px;border-radius:4px;"></div></div>
                        <div style="font-family:'Space Mono',monospace;font-size:11px;color:{c_};width:28px;text-align:right;">{pts}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="background:#0d1220;border:1px solid #d97706;border-radius:8px;padding:12px;font-size:12px;color:#d97706;">🔒 Score breakdown is Premium only. <span style="cursor:pointer;text-decoration:underline;">Upgrade →</span></div>', unsafe_allow_html=True)

    with ci_col:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">💡 Plain-English Insights</div>', unsafe_allow_html=True)
        for lbl,txt,s_,conf in ig[:6]:
            render_insight_row(lbl, txt, s_, conf)
        if not ig:
            st.info("Insights require price data. Check API key.")

        # Sentiment bar
        st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin:14px 0 8px;">📡 StockTwits Sentiment</div>', unsafe_allow_html=True)
        bull = sent.get("bull",50)
        st.markdown(f"""<div class="sw-card">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="color:#4ade80;font-weight:700;font-size:13px;">🟢 Bullish {bull}%</span>
                <span style="color:#f87171;font-weight:700;font-size:13px;">🔴 Bearish {100-bull}%</span>
            </div>
            <div style="background:#1e2a3a;border-radius:6px;height:10px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,#4ade80,#16a34a);width:{bull}%;height:10px;"></div>
            </div>
            <div style="font-size:11px;color:#475569;margin-top:8px;">👥 {sent.get('wl',0):,} watching · {sent.get('msgs',0)} recent posts</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Why Flagged ──
    st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">🎯 Why This Stock Is On Your Radar</div>', unsafe_allow_html=True)
    reasons = []
    if sc>=70:  reasons.append(("Strong overall StockWins signal","bull"))
    if sent.get("bull",50)>=65: reasons.append(("Strong bullish social sentiment on StockTwits","bull"))
    if sf>=20:  reasons.append((f"{sf:.0f}% short float — elevated squeeze potential","bull"))
    if hot:     reasons.append(("Currently trending on StockTwits Hot list","bull"))
    for lbl,_,s_,_ in ig[:4]: reasons.append((lbl, s_))
    rc = st.columns(2)
    for i,(r,s_) in enumerate(reasons[:6]):
        em = "🟢" if s_=="bull" else "🔴" if s_=="bear" else "⚪"
        with rc[i%2]:
            st.markdown(f'<div style="background:#0d1220;border:1px solid #1e2a3a;border-radius:8px;padding:10px 14px;margin-bottom:6px;font-size:13px;color:#64748b;">{em} {r}</div>', unsafe_allow_html=True)

    # ── Related Stocks ──
    st.markdown("<br>", unsafe_allow_html=True)
    sector = info.get("sector","N/A")
    st.markdown(f'<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">🔗 Related Stocks — {sector}</div>', unsafe_allow_html=True)
    # Find stocks in same sector from our universe
    related = []
    all_tickers = list(set([t for cat_tickers in CATEGORIES.values() for t in cat_tickers]))
    for rt in all_tickers[:50]:
        if rt == ticker: continue
        ri = yf_info(rt)
        if ri.get("sector") == sector and ri.get("sector") != "N/A":
            related.append(rt)
        if len(related)>=5: break

    if related:
        rel_cols = st.columns(len(related))
        for col,rt in zip(rel_cols,related):
            rq = td_quote(rt, api)
            if rq:
                rc_ = "#4ade80" if rq["chg_pct"]>=0 else "#f87171"
                col.markdown(f'<div class="stat-box" style="cursor:pointer;"><div class="ticker-sym" style="font-size:13px;">{rt}</div><div style="font-size:13px;font-weight:700;color:#f1f5f9;">${rq["price"]:,.2f}</div><div style="font-size:12px;color:{rc_};">{"▲" if rq["chg_pct"]>=0 else "▼"}{abs(rq["chg_pct"]):.2f}%</div></div>', unsafe_allow_html=True)
                if col.button("View", key=f"rel_{rt}", use_container_width=True):
                    st.session_state.detail_ticker = rt
                    st.session_state.detail_data = {}
                    st.rerun()
    else:
        st.caption("No related stocks found in our universe.")

    # ── Company Description ──
    if info.get("desc"):
        with st.expander(f"About {q.get('name',ticker)}"):
            st.markdown(f'<div style="font-size:13px;color:#475569;line-height:1.7;">{info["desc"]}</div>', unsafe_allow_html=True)

    # ── Watchlist + Alert ──
    st.markdown("<br>", unsafe_allow_html=True)
    wl    = st.session_state.watchlist
    in_wl = ticker in wl
    wb1,wb2,_ = st.columns([1,1,2])
    with wb1:
        if st.button("✅ Remove Watchlist" if in_wl else "➕ Add to Watchlist", type="primary", use_container_width=True):
            if in_wl: wl.remove(ticker)
            else:     wl.append(ticker)
            st.rerun()
    with wb2:
        if st.button("🔔 Set Price Alert", use_container_width=True):
            st.session_state.alert_ticker  = ticker
            st.session_state.alert_price   = price
            nav("settings")

    st.markdown('<div class="disclaimer">⚠️ This analysis is for educational and informational purposes only. The StockWins Score is a data-based metric, not a buy or sell recommendation. Trading involves risk. Always do your own research and consult a licensed financial advisor.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BI DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_bi_dashboard():
    render_topbar("bi_dashboard")
    st.markdown('<div class="section-hd">📊 BI Analytics Dashboard</div>', unsafe_allow_html=True)
    st.caption("Business intelligence analytics across the market — updated every 10 minutes")

    if not is_premium():
        render_lock("Full BI Analytics Dashboard")
        st.markdown('<div style="font-size:13px;color:#475569;margin-top:12px;">Free users can access a preview of BI features below.</div>', unsafe_allow_html=True)
        st.divider()

    with st.spinner("Loading BI data..."):
        movers   = get_bi_movers()
        secs     = sector_perf()
        idx      = index_data()
        hot      = st_hot()
        discussed= get_st_most_discussed()

    # ── Summary Widgets ──────────────────────────────────────────────────────
    sw1,sw2,sw3,sw4,sw5 = st.columns(5)
    gainers = sorted(movers, key=lambda x:x["pct"], reverse=True)
    losers  = sorted(movers, key=lambda x:x["pct"])
    vol_ldrs= sorted(movers, key=lambda x:x["vol_ratio"], reverse=True)

    top_g = gainers[0] if gainers else {}
    top_l = losers[0] if losers else {}
    top_v = vol_ldrs[0] if vol_ldrs else {}
    bull_sec = max(secs, key=secs.get) if secs else "N/A"
    bear_sec = min(secs, key=secs.get) if secs else "N/A"

    for col,(label,value,subval,color) in zip([sw1,sw2,sw3,sw4,sw5],[
        ("Top Gainer", top_g.get("ticker","—"), f"+{top_g.get('pct',0):.2f}%", "#4ade80"),
        ("Top Loser",  top_l.get("ticker","—"), f"{top_l.get('pct',0):.2f}%",  "#f87171"),
        ("Volume King",top_v.get("ticker","—"), f"{top_v.get('vol_ratio',0):.1f}x vol","#60a5fa"),
        ("Best Sector",bull_sec, f"+{secs.get(bull_sec,0):.2f}%","#4ade80"),
        ("Weak Sector", bear_sec,f"{secs.get(bear_sec,0):.2f}%", "#f87171"),
    ]):
        col.markdown(f'<div class="stat-box"><div class="stat-lbl">{label}</div><div style="font-family:\'Space Mono\',monospace;font-size:16px;font-weight:700;color:{color};">{value}</div><div style="font-size:12px;color:{color};">{subval}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tabs = st.tabs(["📈 Leaderboards","🗺️ Sector Analysis","📡 Social Sentiment","🔊 Volume Surge","💡 Market Summary"])

    # LEADERBOARDS
    with tabs[0]:
        lc1,lc2,lc3 = st.columns(3)
        with lc1:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#4ade80;margin-bottom:10px;">🏆 Top Gainers</div>', unsafe_allow_html=True)
            for m in gainers[:10]:
                st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:12px;">{m["ticker"]}</span><span style="color:#94a3b8;font-size:11px;">${m["price"]:,.2f}</span><span style="color:#4ade80;font-weight:700;">▲{m["pct"]:.2f}%</span></div>', unsafe_allow_html=True)
        with lc2:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f87171;margin-bottom:10px;">📉 Top Losers</div>', unsafe_allow_html=True)
            for m in losers[:10]:
                st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:12px;">{m["ticker"]}</span><span style="color:#94a3b8;font-size:11px;">${m["price"]:,.2f}</span><span style="color:#f87171;font-weight:700;">▼{abs(m["pct"]):.2f}%</span></div>', unsafe_allow_html=True)
        with lc3:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#60a5fa;margin-bottom:10px;">🔊 Volume Leaders</div>', unsafe_allow_html=True)
            for m in vol_ldrs[:10]:
                vr_c = "#f87171" if m["vol_ratio"]>=3 else "#fbbf24" if m["vol_ratio"]>=2 else "#60a5fa"
                st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:12px;">{m["ticker"]}</span><span style="color:#94a3b8;font-size:11px;">{m["volume"]/1e6:.1f}M</span><span style="color:{vr_c};font-weight:700;">{m["vol_ratio"]:.1f}x</span></div>', unsafe_allow_html=True)

    # SECTOR ANALYSIS
    with tabs[1]:
        st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:12px;">Sector Performance Today</div>', unsafe_allow_html=True)
        sec_sorted = sorted(secs.items(), key=lambda x:x[1], reverse=True)
        for sec,chg in sec_sorted:
            c_  = "#4ade80" if chg>0 else "#f87171"
            bar_w = min(abs(chg)*10, 100)
            a_  = "▲" if chg>=0 else "▼"
            st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <div style="width:120px;font-size:12px;color:#94a3b8;">{sec}</div>
                <div style="flex:1;background:#1e2a3a;border-radius:4px;height:20px;position:relative;overflow:hidden;">
                    <div style="background:{"#052e16" if chg>=0 else "#450a0a"};width:{bar_w}%;height:20px;display:flex;align-items:center;padding-left:8px;">
                        <span style="color:{c_};font-size:12px;font-weight:700;">{a_}{abs(chg):.2f}%</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # SOCIAL SENTIMENT
    with tabs[2]:
        sc1,sc2 = st.columns(2)
        with sc1:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">🔥 Trending on StockTwits</div>', unsafe_allow_html=True)
            for i,t in enumerate(hot[:8],1):
                s = st_sentiment(t)
                bull_c = "#4ade80" if s["bull"]>=60 else "#f87171" if s["bull"]<40 else "#94a3b8"
                st.markdown(f'<div class="mover-row"><span style="color:#475569;font-size:11px;">#{i}</span><span class="ticker-sym" style="font-size:12px;">{t}</span><span style="color:{bull_c};font-weight:700;font-size:12px;">{s["bull"]}% bull</span><span style="color:#475569;font-size:11px;">{s["wl"]:,} watching</span></div>', unsafe_allow_html=True)
        with sc2:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">👥 Most Watchlisted</div>', unsafe_allow_html=True)
            for item in discussed:
                bull_c = "#4ade80" if item["bull"]>=60 else "#f87171" if item["bull"]<40 else "#94a3b8"
                st.markdown(f'<div class="mover-row"><span class="ticker-sym" style="font-size:12px;">{item["ticker"]}</span><span style="color:#475569;font-size:11px;">{item["watchlists"]:,}</span><span style="color:{bull_c};font-weight:700;font-size:12px;">{item["bull"]}% bull</span></div>', unsafe_allow_html=True)

    # VOLUME SURGE
    with tabs[3]:
        st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">🔊 Volume Surge Detector</div>', unsafe_allow_html=True)
        st.caption("Stocks trading at significantly above-average volume today")
        surge = [m for m in movers if m["vol_ratio"]>=1.5]
        surge.sort(key=lambda x:x["vol_ratio"],reverse=True)
        if surge:
            surge_data = pd.DataFrame([{"Ticker":m["ticker"],"Price":f"${m['price']:,.2f}","Day Change":f"{m['pct']:+.2f}%","Volume":f"{m['volume']/1e6:.2f}M","Vol Ratio":f"{m['vol_ratio']:.1f}x avg"} for m in surge])
            st.dataframe(surge_data, use_container_width=True, hide_index=True)
        else:
            st.info("No significant volume surges detected right now.")

        st.markdown('<div class="insight-row" style="margin-top:12px;"><strong>What is a Volume Surge?</strong><div style="font-size:13px;color:#64748b;margin-top:4px;">When a stock\'s trading volume significantly exceeds its recent average, it can signal that something important is happening — earnings news, institutional buying or selling, social media buzz, or a major price breakout. Higher volume generally means more conviction behind the move.</div></div>', unsafe_allow_html=True)

    # MARKET SUMMARY
    with tabs[4]:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:16px;">📋 Market Intelligence Summary</div>', unsafe_allow_html=True)
        bullish_secs = [s for s,c in secs.items() if c>0.5]
        bearish_secs = [s for s,c in secs.items() if c<-0.5]
        avg_pct      = sum(m["pct"] for m in movers)/len(movers) if movers else 0
        sentiment    = "Bullish" if avg_pct>0.3 else "Bearish" if avg_pct<-0.3 else "Neutral"
        s_color      = "#4ade80" if avg_pct>0 else "#f87171"

        sm_cols = st.columns(2)
        with sm_cols[0]:
            st.markdown(f"""<div class="sw-card">
                <div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:12px;">Market Overview</div>
                <div class="mover-row"><span style="color:#94a3b8;">Overall Sentiment</span><span style="color:{s_color};font-weight:700;">{sentiment}</span></div>
                <div class="mover-row"><span style="color:#94a3b8;">Avg Stock Change</span><span style="color:{s_color};font-weight:700;">{avg_pct:+.2f}%</span></div>
                <div class="mover-row"><span style="color:#94a3b8;">Bullish Sectors</span><span style="color:#4ade80;font-weight:700;">{len(bullish_secs)}/10</span></div>
                <div class="mover-row"><span style="color:#94a3b8;">Bearish Sectors</span><span style="color:#f87171;font-weight:700;">{len(bearish_secs)}/10</span></div>
                <div class="mover-row"><span style="color:#94a3b8;">Volume Surges</span><span style="color:#60a5fa;font-weight:700;">{len([m for m in movers if m["vol_ratio"]>=2])} stocks</span></div>
            </div>""", unsafe_allow_html=True)
        with sm_cols[1]:
            st.markdown(f"""<div class="sw-card">
                <div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:12px;">Key Highlights</div>
                <div style="font-size:13px;color:#64748b;line-height:2;">
                🟢 <strong style="color:#94a3b8;">Strongest sectors:</strong> {', '.join(bullish_secs[:3]) if bullish_secs else 'None'}<br>
                🔴 <strong style="color:#94a3b8;">Weakest sectors:</strong> {', '.join(bearish_secs[:3]) if bearish_secs else 'None'}<br>
                🔥 <strong style="color:#94a3b8;">Social buzz:</strong> {', '.join(hot[:5])}<br>
                🔊 <strong style="color:#94a3b8;">Volume leader:</strong> {top_v.get('ticker','—')} ({top_v.get('vol_ratio',0):.1f}x avg)<br>
                📈 <strong style="color:#94a3b8;">Biggest gainer:</strong> {top_g.get('ticker','—')} (+{top_g.get('pct',0):.2f}%)
                </div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DISCOVER
# ═══════════════════════════════════════════════════════════════════════════════
def page_discover():
    render_topbar("discover")
    api = get_key()
    st.markdown('<div class="section-hd">🔭 Discover Stocks</div>', unsafe_allow_html=True)

    avail = FREE_CATS if not is_premium() else list(CATEGORIES.keys())
    fc, mc = st.columns([1,4])

    with fc:
        st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:8px;">🔎 Filters</div>', unsafe_allow_html=True)
        sel  = st.selectbox("Category", avail, label_visibility="collapsed")
        st.markdown('<div style="font-size:11px;color:#475569;margin:8px 0 4px;">SORT BY</div>', unsafe_allow_html=True)
        sort = st.radio("Sort", ["SW Score","Price Change","Volume"],label_visibility="collapsed")
        st.markdown('<div style="font-size:11px;color:#475569;margin:8px 0 4px;">MIN SCORE</div>', unsafe_allow_html=True)
        min_sc = st.slider("Min Score",0,80,0,label_visibility="collapsed")
        if not is_premium():
            st.markdown('<div style="background:#0d1220;border:1px solid #d97706;border-radius:8px;padding:12px;font-size:12px;color:#d97706;margin-top:12px;">🔒 Premium unlocks all 17+ categories, squeeze scanner, and advanced screener.</div>', unsafe_allow_html=True)
            if st.button("Upgrade →"): nav("pricing")

    with mc:
        if sel in PREMIUM_CATS and not is_premium():
            render_lock(sel)
        else:
            render_category(sel, api, limit=12)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: WATCHLIST
# ═══════════════════════════════════════════════════════════════════════════════
def page_watchlist():
    render_topbar("watchlist")
    api = get_key()
    st.markdown('<div class="section-hd">⭐ My Watchlist</div>', unsafe_allow_html=True)

    wl = st.session_state.watchlist
    if not wl:
        st.markdown('<div class="sw-card" style="text-align:center;padding:48px;"><div style="font-size:36px;margin-bottom:12px;">📋</div><div style="font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:8px;">Your watchlist is empty</div><div style="font-size:13px;color:#475569;">Browse stock categories and click ➕ Watch to track stocks here.</div></div>', unsafe_allow_html=True)
        if st.button("Browse Stocks →", type="primary"): nav("dashboard")
        return

    st.caption(f"{len(wl)} stocks in your watchlist")

    rows = []
    prog = st.progress(0,"Loading watchlist...")
    for i,t in enumerate(wl):
        prog.progress((i+1)/len(wl),f"Loading {t}...")
        q    = td_quote(t, api)
        df   = td_ohlcv(t, api, 30)
        info = yf_info(t)
        sent = st_sentiment(t)
        sc,_ = score_stock(df, info, sent)
        risk = get_risk_level(df, info)
        if q:
            rows.append({
                "Ticker":      t,
                "Name":        q.get("name","")[:22],
                "Price":       f"${q['price']:,.2f}",
                "Change":      f"{q['chg_pct']:+.2f}%",
                "SW Score":    sc,
                "Risk Level":  risk,
                "Short Float": f"{(info.get('sf',0) or 0)*100:.1f}%",
                "Bullish Sent":f"{sent.get('bull',50)}%",
                "Sector":      info.get("sector","N/A"),
            })
    prog.empty()

    if rows:
        # Color the Change column
        df_wl = pd.DataFrame(rows)
        st.dataframe(df_wl, use_container_width=True, hide_index=True)

    # Watchlist analytics
    if rows and is_premium():
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:10px;">📊 Watchlist Analytics</div>', unsafe_allow_html=True)
        wc1,wc2,wc3,wc4 = st.columns(4)
        avg_sc   = sum(r["SW Score"] for r in rows)/len(rows) if rows else 0
        pos_stocks = sum(1 for r in rows if "+" in r["Change"])
        high_risk  = sum(1 for r in rows if r["Risk Level"] in ("High","Very High"))
        avg_bull   = sum(int(r["Bullish Sent"].replace("%","")) for r in rows)/len(rows) if rows else 0
        for col,(v,l) in zip([wc1,wc2,wc3,wc4],[
            (f"{avg_sc:.0f}","Avg SW Score"),(f"{pos_stocks}/{len(rows)}","In the Green"),
            (f"{high_risk}","High Risk Stocks"),(f"{avg_bull:.0f}%","Avg Bull Sentiment")
        ]):
            col.markdown(f'<div class="stat-box"><div class="stat-val">{v}</div><div class="stat-lbl">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,_,_ = st.columns([1,1,2])
    with c1:
        if st.button("🗑️ Clear Watchlist"):
            st.session_state.watchlist = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SCREENER
# ═══════════════════════════════════════════════════════════════════════════════
def page_screener():
    render_topbar("screener")
    st.markdown('<div class="section-hd">🔍 Advanced Stock Screener</div>', unsafe_allow_html=True)

    if not is_premium():
        render_lock("Advanced Stock Screener")
        return

    api = get_key()
    st.markdown('<div style="font-size:13px;color:#475569;margin-bottom:16px;">Build custom multi-factor screens across all stock categories. Results are ranked by StockWins Score.</div>', unsafe_allow_html=True)

    with st.expander("⚙️ Screener Filters", expanded=True):
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            min_sc    = st.slider("Min SW Score",0,100,40)
            min_rsi   = st.slider("Min RSI",0,100,20)
        with c2:
            max_rsi   = st.slider("Max RSI",0,100,80)
            min_sf    = st.slider("Min Short Float %",0,50,0)
        with c3:
            req_bull  = st.checkbox("MACD Bullish only")
            req_above = st.checkbox("Above 20-day MA only")
            req_vol   = st.checkbox("Volume spike >1.5x")
            req_hot   = st.checkbox("StockTwits trending only")
        with c4:
            sel_cats  = st.multiselect("Categories", list(CATEGORIES.keys()), default=["💻 Tech","🤖 AI"])
            max_risk  = st.selectbox("Max Risk Level",["Any","Low","Low-Medium","Medium","Medium-High","High"])

    # Save screener
    sc1,sc2 = st.columns([3,1])
    with sc1:
        scr_name = st.text_input("Save this screener as...", placeholder="My Growth Screen", label_visibility="collapsed")
    with sc2:
        if st.button("💾 Save Screener") and scr_name:
            st.session_state.saved_screeners.append({"name":scr_name,"cats":sel_cats,"min_sc":min_sc})
            st.success("Screener saved!")

    if st.session_state.saved_screeners:
        st.caption(f"Saved screeners: {', '.join([s['name'] for s in st.session_state.saved_screeners])}")

    if st.button("🔍 Run Screener", type="primary", use_container_width=True):
        universe = list(set([t for c in sel_cats for t in (CATEGORIES.get(c,[]) or st_hot())]))[:35]
        hot_list = st_hot() if req_hot else []
        results  = []
        prog     = st.progress(0,"Screening stocks...")
        risk_order = ["Low","Low-Medium","Medium","Medium-High","High","Very High","Unknown"]
        max_risk_idx = risk_order.index(max_risk) if max_risk!="Any" else 99

        for i,t in enumerate(universe):
            prog.progress((i+1)/len(universe),f"Screening {t}...")
            if req_hot and t not in hot_list: continue
            q    = td_quote(t, api)
            df   = td_ohlcv(t, api, 60)
            info = yf_info(t)
            sent = st_sentiment(t)
            sc,_ = score_stock(df, info, sent)
            risk = get_risk_level(df, info)

            if df is None or len(df)<20: continue
            try:
                rsi   = ta.momentum.RSIIndicator(df["close"].copy(),14).rsi().iloc[-1]
                ma20  = df["close"].rolling(20).mean().iloc[-1]
                macd_ = ta.trend.MACD(df["close"].copy())
                mv    = macd_.macd().iloc[-1]
                ms    = macd_.macd_signal().iloc[-1]
                price = df["close"].iloc[-1]
                avg_v = df["volume"].rolling(20).mean().iloc[-1]
                cur_v = df["volume"].iloc[-1]
                sf    = (info.get("sf",0) or 0)*100

                if sc<min_sc: continue
                if pd.notna(rsi) and (rsi<min_rsi or rsi>max_rsi): continue
                if sf<min_sf: continue
                if req_bull and pd.notna(mv) and mv<ms: continue
                if req_above and pd.notna(ma20) and price<ma20: continue
                if req_vol and pd.notna(avg_v) and avg_v>0 and cur_v<avg_v*1.5: continue
                if max_risk!="Any" and risk in risk_order and risk_order.index(risk)>max_risk_idx: continue

                results.append({
                    "Ticker":      t,
                    "Price":       f"${price:,.2f}" if q else "N/A",
                    "RSI":         round(rsi,1) if pd.notna(rsi) else "N/A",
                    "SW Score":    sc,
                    "Risk":        risk,
                    "Short Float": f"{sf:.1f}%",
                    "MACD":        "Bullish" if (pd.notna(mv) and mv>ms) else "Bearish",
                    "vs MA20":     "Above" if price>ma20 else "Below",
                    "Vol Ratio":   f"{cur_v/avg_v:.1f}x" if pd.notna(avg_v) and avg_v>0 else "N/A",
                    "Bull Sent.":  f"{sent.get('bull',50)}%",
                })
            except: continue

        prog.empty()
        if results:
            st.success(f"✅ {len(results)} stocks passed your filters!")
            df_r = pd.DataFrame(results).sort_values("SW Score",ascending=False)
            st.dataframe(df_r, use_container_width=True, hide_index=True)
        else:
            st.info("No stocks matched all your criteria. Try relaxing the filters.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
def page_settings():
    render_topbar()
    st.markdown('<div class="section-hd">⚙️ Account Settings</div>', unsafe_allow_html=True)

    tabs = st.tabs(["👤 Profile","🔐 Security","🔔 Alerts & Notifications","📊 Subscription","🔑 API Keys"])

    db_user = get_user_db()
    email   = st.session_state.user["email"] if is_authed() else ""

    # PROFILE
    with tabs[0]:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:16px;">Profile Information</div>', unsafe_allow_html=True)
        with st.form("profile_form"):
            new_name  = st.text_input("Display Name", value=st.session_state.user.get("name",""))
            disp_email= st.text_input("Email Address", value=email, disabled=True)
            st.caption("Email address cannot be changed.")
            verified  = db_user.get("verified", False)
            if not verified:
                st.warning("⚠️ Your email is not verified. Please check your inbox.")
            else:
                st.markdown('<span style="color:#4ade80;font-size:12px;">✅ Email verified</span>', unsafe_allow_html=True)
            sub = st.form_submit_button("Save Changes", type="primary")
            if sub and new_name:
                st.session_state.user["name"] = new_name
                if email in st.session_state.users_db:
                    st.session_state.users_db[email]["name"] = new_name
                st.success("✅ Profile updated!")

    # SECURITY
    with tabs[1]:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:16px;">Change Password</div>', unsafe_allow_html=True)
        with st.form("pw_form"):
            cur_pw  = st.text_input("Current Password", type="password")
            new_pw  = st.text_input("New Password", type="password", placeholder="Min 6 characters")
            new_pw2 = st.text_input("Confirm New Password", type="password")
            sub     = st.form_submit_button("Update Password", type="primary")
            if sub:
                if not all([cur_pw, new_pw, new_pw2]):
                    st.error("Please fill in all fields.")
                elif hp(cur_pw) != db_user.get("pw",""):
                    st.error("Current password is incorrect.")
                elif new_pw != new_pw2:
                    st.error("New passwords don't match.")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    st.session_state.users_db[email]["pw"] = hp(new_pw)
                    st.success("✅ Password updated successfully!")

        st.divider()
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f87171;margin-bottom:8px;">Danger Zone</div>', unsafe_allow_html=True)
        if st.button("🚪 Log Out of All Sessions"):
            logout()

    # ALERTS
    with tabs[2]:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:16px;">Price Alerts</div>', unsafe_allow_html=True)

        # Add alert
        with st.form("alert_form"):
            ac1,ac2,ac3 = st.columns(3)
            with ac1: a_ticker = st.text_input("Ticker",value=st.session_state.get("alert_ticker",""),placeholder="AAPL").upper()
            with ac2: a_price  = st.number_input("Alert Price ($)",value=float(st.session_state.get("alert_price",100)),min_value=0.01)
            with ac3: a_type   = st.selectbox("Type",["Price Above","Price Below","% Move Up","% Move Down"])
            sub = st.form_submit_button("➕ Add Alert", type="primary")
            if sub and a_ticker:
                st.session_state.alerts.append({"ticker":a_ticker,"price":a_price,"type":a_type,"active":True})
                st.success(f"✅ Alert set: {a_ticker} {a_type} ${a_price:.2f}")

        # Display alerts
        if st.session_state.alerts:
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f1f5f9;margin:16px 0 8px;">Your Active Alerts</div>', unsafe_allow_html=True)
            for i,alert in enumerate(st.session_state.alerts):
                ac1,ac2 = st.columns([4,1])
                with ac1:
                    st.markdown(f'<div class="sw-card" style="padding:12px 16px;margin-bottom:6px;"><span class="ticker-sym" style="font-size:13px;">{alert["ticker"]}</span> <span style="color:#94a3b8;font-size:12px;">{alert["type"]} ${alert["price"]:.2f}</span></div>', unsafe_allow_html=True)
                with ac2:
                    if st.button("🗑️",key=f"del_alert_{i}"):
                        st.session_state.alerts.pop(i); st.rerun()
        else:
            st.info("No active alerts. Add one above.")

        st.divider()
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:12px;">Notification Preferences</div>', unsafe_allow_html=True)
        n1 = st.checkbox("Email notifications for price alerts",    value=db_user.get("notif_email",True))
        n2 = st.checkbox("Volume surge alerts for watchlist stocks", value=db_user.get("notif_vol",False))
        n3 = st.checkbox("Daily market summary email",              value=False)
        n4 = st.checkbox("New short squeeze candidates",            value=False)
        if st.button("Save Notification Settings", type="primary"):
            if email in st.session_state.users_db:
                st.session_state.users_db[email]["notif_email"] = n1
                st.session_state.users_db[email]["notif_vol"]   = n2
            st.success("✅ Notification settings saved!")

    # SUBSCRIPTION
    with tabs[3]:
        role = st.session_state.role
        role_label = {"free":"Free","premium":"Premium Monthly","admin":"Admin"}.get(role,"Free")
        role_color = "#d97706" if is_premium() else "#3b82f6"
        st.markdown(f"""<div class="sw-card-blue">
            <div style="font-size:16px;font-weight:800;color:#f1f5f9;margin-bottom:4px;">Current Plan: <span style="color:{role_color};">{role_label}</span></div>
            <div style="font-size:13px;color:#475569;margin-bottom:16px;">Member since {datetime.now().strftime('%B %Y')}</div>
            {"<div style='font-size:13px;color:#4ade80;'>✅ Full access to all features, categories, and analytics.</div>" if is_premium() else "<div style='font-size:13px;color:#94a3b8;'>Limited access. Upgrade to unlock all features.</div>"}
        </div>""", unsafe_allow_html=True)

        if not is_premium():
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:12px;">Upgrade Your Plan</div>', unsafe_allow_html=True)
            uc1,uc2 = st.columns(2)
            with uc1:
                st.markdown("""<div class="pricing-featured" style="text-align:center;"><div style="font-size:15px;font-weight:700;color:#f1f5f9;">Premium Monthly</div><div class="pricing-price">$29</div><div style="font-size:12px;color:#475569;">per month</div></div>""", unsafe_allow_html=True)
                if st.button("🚀 Upgrade Monthly →", type="primary", use_container_width=True):
                    st.info("💳 Payment processing coming soon!")
            with uc2:
                st.markdown("""<div class="pricing-card" style="text-align:center;"><div style="font-size:15px;font-weight:700;color:#f1f5f9;">Annual Plan</div><div class="pricing-price">$199</div><div style="font-size:12px;color:#475569;">per year · save 43%</div></div>""", unsafe_allow_html=True)
                if st.button("💰 Upgrade Annual →", use_container_width=True):
                    st.info("💳 Payment processing coming soon!")
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⚠️ Cancel Subscription"):
                st.warning("To cancel, please contact support at support@stockwins.com")

    # API KEYS
    with tabs[4]:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:16px;">API Key Management</div>', unsafe_allow_html=True)
        try:
            _ = st.secrets["TWELVE_DATA_API_KEY"]
            st.markdown('<div class="sw-card-green"><div style="font-size:13px;font-weight:700;color:#4ade80;">✅ Twelve Data API Key — Configured via Streamlit Secrets</div><div style="font-size:12px;color:#475569;margin-top:4px;">Your API key is securely stored server-side. It is never exposed to the frontend.</div></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div style="font-size:13px;color:#475569;margin-bottom:8px;">Enter your Twelve Data API key to enable live market data. Get a free key at <a href="https://twelvedata.com" style="color:#3b82f6;">twelvedata.com</a></div>', unsafe_allow_html=True)
            k = st.text_input("Twelve Data API Key", type="password", placeholder="Your API key here")
            if st.button("Save Key", type="primary"):
                if k:
                    st.session_state["api_key_input"] = k
                    st.success("✅ API key saved for this session!")
                    st.info("💡 For permanent setup, add TWELVE_DATA_API_KEY to your Streamlit Cloud Secrets.")

        st.divider()
        st.markdown("""<div class="sw-card">
            <div style="font-size:13px;font-weight:700;color:#f1f5f9;margin-bottom:8px;">🔒 Security & Privacy</div>
            <div style="font-size:13px;color:#475569;line-height:1.7;">
            • API keys are stored server-side only and never exposed in frontend code<br>
            • We use Streamlit's built-in secrets management for secure key storage<br>
            • All external API calls are made server-side through secure backend functions<br>
            • We do not store or log your API key beyond the current session<br>
            • You can revoke access at any time by clearing your API key
            </div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PRICING
# ═══════════════════════════════════════════════════════════════════════════════
def page_pricing():
    render_topbar("pricing")
    st.markdown('<div class="section-hd">💰 Plans & Pricing</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:14px;color:#475569;margin-bottom:28px;">Choose the plan that fits your trading style. Cancel anytime.</div>', unsafe_allow_html=True)

    p1,p2,p3 = st.columns([1,1.15,1])
    with p1:
        st.markdown("""<div class="pricing-card"><div style="font-size:16px;font-weight:700;color:#f1f5f9;">Free</div>
            <div class="pricing-price">$0</div><div style="font-size:12px;color:#475569;margin-bottom:16px;">forever</div>
            <hr style="border-color:#1e2a3a;">
            <div style="font-size:13px;color:#475569;line-height:2.2;margin-top:14px;">
            ✅ Market overview dashboard<br>✅ 5 stock categories<br>✅ StockTwits hot list<br>
            ✅ Basic RSI & MACD signals<br>✅ Plain-English insights<br>✅ Basic watchlist (10 stocks)<br>
            ✅ Basic BI analytics (preview)<br>❌ Short squeeze scanner<br>
            ❌ Advanced screener<br>❌ Full BI dashboard<br>❌ Premium categories<br>
            ❌ Score breakdowns<br>❌ Watchlist analytics<br>❌ Saved screeners</div></div>""", unsafe_allow_html=True)
        if not is_authed():
            if st.button("Get Started Free", use_container_width=True): nav("signup")
        elif not is_premium():
            st.markdown('<div style="text-align:center;font-size:12px;color:#4ade80;margin-top:12px;">✅ Your current plan</div>', unsafe_allow_html=True)
    with p2:
        st.markdown("""<div class="pricing-featured">
            <div style="background:#3b82f6;color:white;font-size:10px;font-weight:700;padding:3px 12px;border-radius:20px;display:inline-block;margin-bottom:10px;letter-spacing:1.5px;">⭐ MOST POPULAR</div>
            <div style="font-size:16px;font-weight:700;color:#f1f5f9;">Premium Monthly</div>
            <div class="pricing-price">$29</div><div style="font-size:12px;color:#475569;margin-bottom:16px;">per month · cancel anytime</div>
            <hr style="border-color:#1e2a3a;">
            <div style="font-size:13px;color:#475569;line-height:2.2;margin-top:14px;">
            ✅ Everything in Free<br>✅ All 17+ stock categories<br>✅ Short squeeze scanner<br>
            ✅ Advanced multi-factor screener<br>✅ Full BI analytics dashboard<br>
            ✅ Score breakdowns (per component)<br>✅ Volume surge alerts<br>
            ✅ Breakout candidates<br>✅ Momentum scanner<br>✅ Oversold bounce scanner<br>
            ✅ Unlimited watchlist<br>✅ Watchlist analytics<br>✅ Saved screeners</div></div>""", unsafe_allow_html=True)
        if st.button("🚀 Start Premium →", type="primary", use_container_width=True):
            st.info("💳 Payment processing coming soon! Contact support@stockwins.com to upgrade manually.")
    with p3:
        st.markdown("""<div class="pricing-card">
            <div style="background:linear-gradient(90deg,#854d0e,#d97706);color:white;font-size:10px;font-weight:700;padding:3px 12px;border-radius:20px;display:inline-block;margin-bottom:4px;letter-spacing:1px;">BEST VALUE</div>
            <div style="font-size:16px;font-weight:700;color:#f1f5f9;">Annual Plan</div>
            <div class="pricing-price">$199</div><div style="font-size:12px;color:#475569;margin-bottom:16px;">per year · save 43%</div>
            <hr style="border-color:#1e2a3a;">
            <div style="font-size:13px;color:#475569;line-height:2.2;margin-top:14px;">
            ✅ Everything in Premium<br>✅ Priority support<br>✅ Early feature access<br>
            ✅ Export data to CSV<br>✅ Custom price alerts<br>✅ API access (Q3 2026)<br>
            ✅ Backtesting module (coming)<br>✅ Portfolio tracker (coming)<br>
            ✅ Multi-device sync</div></div>""", unsafe_allow_html=True)
        if st.button("Get Annual Plan →", use_container_width=True):
            st.info("💳 Payment processing coming soon!")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Feature table
    st.markdown('<div class="section-hd">Full Feature Comparison</div>', unsafe_allow_html=True)
    comp = {
        "Feature":["Market Overview Dashboard","Stock Categories","StockTwits Hot Stocks",
                   "Basic Signals (RSI, MACD, MA)","Plain-English Insights","Watchlist",
                   "Sector Heatmap","Top Gainers/Losers","Short Squeeze Scanner",
                   "Breakout Candidates","Momentum Scanner","Oversold Bounce Scanner",
                   "High Volume Alerts","Score Breakdowns","Advanced Screener",
                   "Full BI Analytics","Saved Screeners","Watchlist Analytics",
                   "Export Data (CSV)","Custom Alerts","API Access"],
        "Free":   ["✅","5 cats","✅","✅","✅","10 stocks","✅","Preview",
                   "❌","❌","❌","❌","❌","❌","❌","Preview","❌","❌","❌","❌","❌"],
        "Premium":["✅","17+ cats","✅","✅","✅","Unlimited","✅","✅",
                   "✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","❌","❌","❌"],
        "Annual": ["✅","17+ cats","✅","✅","✅","Unlimited","✅","✅",
                   "✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","Q3 2026"],
    }
    st.dataframe(pd.DataFrame(comp), use_container_width=True, hide_index=True)

    st.markdown('<div class="disclaimer">⚠️ StockWins is an educational data analysis tool. Subscriptions provide access to data features only. Nothing on this platform constitutes financial advice. Trading involves risk. All signals are algorithmic outputs for educational purposes only. Always consult a licensed financial advisor.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _render_api_key_setup():
    st.markdown('<div class="section-hd">🔑 API Key Required</div>', unsafe_allow_html=True)
    with st.expander("Enter your Twelve Data API Key to enable live data", expanded=True):
        st.markdown('<div style="font-size:13px;color:#475569;margin-bottom:12px;">StockWins uses <a href="https://twelvedata.com" style="color:#3b82f6;">Twelve Data</a> for live market data. Get your free API key (800 credits/day) at <strong>twelvedata.com</strong> — no credit card needed.</div>', unsafe_allow_html=True)
        k = st.text_input("API Key", type="password", placeholder="Paste your Twelve Data API key here")
        if k:
            st.session_state["api_key_input"] = k
            st.rerun()
        st.caption("For permanent setup, add TWELVE_DATA_API_KEY to Streamlit Cloud Secrets (Settings > Secrets).")


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sw-logo" style="margin-bottom:16px;">Stock<span>Wins</span></div>', unsafe_allow_html=True)

    if is_authed():
        role_icon = "👑 Premium" if is_premium() else "🆓 Free"
        st.markdown(f'<div style="font-size:12px;color:#475569;">Signed in as</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;font-weight:600;color:#f1f5f9;">{st.session_state.user["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:12px;color:#3b82f6;margin-bottom:12px;">{role_icon}</div>', unsafe_allow_html=True)
    else:
        st.info("Sign in for the full dashboard.")

    st.divider()

    # API Key
    try:
        _ = st.secrets["TWELVE_DATA_API_KEY"]
        st.markdown('<div style="font-size:12px;color:#4ade80;">✅ API Key configured</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="font-size:11px;font-weight:700;color:#475569;margin-bottom:6px;">TWELVE DATA API KEY</div>', unsafe_allow_html=True)
        k = st.text_input("Key",type="password",label_visibility="collapsed",placeholder="Paste key here")
        if k: st.session_state["api_key_input"] = k
        if not st.session_state.get("api_key_input"):
            st.caption("⚠️ Required. Free key at twelvedata.com")

    st.divider()

    if is_authed():
        st.markdown('<div style="font-size:11px;font-weight:700;color:#475569;margin-bottom:8px;">NAVIGATION</div>', unsafe_allow_html=True)
        nav_items = [("📊 Dashboard","dashboard"),("🔭 Discover","discover"),
                     ("⭐ Watchlist","watchlist"),("🔍 Screener","screener"),
                     ("📈 BI Analytics","bi_dashboard"),("💰 Pricing","pricing"),
                     ("⚙️ Settings","settings")]
        for lbl,pg in nav_items:
            if st.button(lbl, key=f"side_{pg}", use_container_width=True):
                nav(pg)
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()

    st.markdown('<div style="font-size:11px;color:#1e2a3a;margin-top:12px;">📈 StockWins v1.0</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#1e2a3a;">⚠️ Educational use only</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#1e2a3a;">© 2026 StockWins</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
page = st.session_state.page
guard_pages = {"dashboard","discover","watchlist","screener","bi_dashboard","stock_detail","settings"}

if page in guard_pages and not is_authed():
    page_login()
elif page == "landing":          page_landing()
elif page == "login":            page_login()
elif page == "signup":           page_signup()
elif page == "verify_email":     page_verify_email()
elif page == "forgot_password":  page_forgot_password()
elif page == "pricing":          page_pricing()
elif page == "dashboard":        page_dashboard()
elif page == "discover":         page_discover()
elif page == "watchlist":        page_watchlist()
elif page == "screener":         page_screener()
elif page == "bi_dashboard":     page_bi_dashboard()
elif page == "stock_detail":     page_detail()
elif page == "settings":         page_settings()
else:                            page_landing()
