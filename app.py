# ═══════════════════════════════════════════════════════════════════════
# STOCKWINS v3.0 — Premium Stock Intelligence Platform
# Design: Fintech SaaS Terminal · Data: Yahoo Finance + StockTwits
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st
import requests
import pandas as pd
import ta
import yfinance as yf
import hashlib
import time
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="StockWins | Spot Market Opportunities",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# CSS — Premium dark fintech SaaS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #060a12 !important; color: #c9d3e0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { display:none !important; }
#MainMenu,footer,[data-testid="stDecoration"]{display:none !important;}
div.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stVerticalBlock"]{gap:0 !important;}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#080d18 !important;
    border-right:1px solid #111c2e !important;
    min-width:210px !important; max-width:210px !important;
}
[data-testid="stSidebar"]>div{padding:0 !important;}

/* Buttons */
.stButton>button{
    background:#0e1525 !important; border:1px solid #1a2840 !important;
    color:#7a8fa8 !important; border-radius:6px !important;
    font-family:'Inter',sans-serif !important; font-size:13px !important;
    font-weight:500 !important; padding:7px 16px !important;
    transition:all 0.15s !important; width:100%;
}
.stButton>button:hover{border-color:#2563eb !important;color:#60a5fa !important;background:#0f1d35 !important;}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#2563eb,#1d4ed8) !important;
    border-color:#2563eb !important; color:#fff !important; font-weight:700 !important;
}
.stButton>button[kind="primary"]:hover{background:linear-gradient(135deg,#3b82f6,#2563eb) !important;}

/* Inputs */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,
.stSelectbox>div>div,.stNumberInput>div>div>input{
    background:#0e1525 !important; border:1px solid #1a2840 !important;
    color:#c9d3e0 !important; border-radius:6px !important;
    font-family:'Inter',sans-serif !important; font-size:13px !important;
}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
    border-color:#2563eb !important; box-shadow:0 0 0 2px rgba(37,99,235,.15) !important;
}
.stMultiSelect>div{background:#0e1525 !important;border-color:#1a2840 !important;}
[data-testid="stCheckbox"]>label{color:#7a8fa8 !important;font-size:13px !important;}
[data-testid="stRadio"]>div>label{color:#7a8fa8 !important;font-size:13px !important;}
.stSlider>div{color:#4a6080 !important;}
.stProgress>div>div{background:#111c2e !important;height:4px !important;}
.stProgress>div>div>div{background:#2563eb !important;}
.streamlit-expanderHeader{
    background:#0e1525 !important; border:1px solid #1a2840 !important;
    border-radius:6px !important; color:#7a8fa8 !important; font-size:13px !important;
}
.streamlit-expanderContent{background:#0a1020 !important;border:1px solid #1a2840 !important;border-top:none !important;}
[data-testid="stDataFrame"]{border:1px solid #1a2840 !important;border-radius:8px !important;overflow:hidden;}
[data-testid="stDataFrame"] th{background:#0e1525 !important;color:#4a6080 !important;font-size:11px !important;text-transform:uppercase;}
[data-testid="stDataFrame"] td{background:#080d18 !important;color:#c9d3e0 !important;font-size:13px !important;}
hr{border-color:#111c2e !important;margin:0 !important;}
[data-testid="stTabs"]>div{border-color:#111c2e !important;}
[data-testid="stTab"]{font-size:13px !important;color:#506070 !important;}

/* ── Custom Components ── */
.sw-logo{
    font-family:'JetBrains Mono',monospace;
    font-size:18px;font-weight:700;color:#e2e8f0;letter-spacing:-0.5px;
}
.sw-logo .w{color:#f59e0b;}

/* NAV */
.nav-sec{
    font-size:10px;font-weight:700;color:#1e2d42;letter-spacing:1.5px;
    text-transform:uppercase;padding:18px 16px 5px;
}
.nav-item-wrap{position:relative;}
.nav-label{
    position:absolute;top:0;left:0;right:0;bottom:0;
    display:flex;align-items:center;gap:10px;
    padding:9px 16px;font-size:13px;font-weight:500;
    color:#506070;pointer-events:none;
    border-left:2px solid transparent;
}
.nav-label.active{color:#f59e0b;border-left-color:#f59e0b;background:rgba(245,158,11,.05);}
.nav-label .icon{font-size:14px;width:16px;text-align:center;}

/* TOP BAR */
.topbar{
    background:#080d18;border-bottom:1px solid #111c2e;
    padding:0 24px;display:flex;align-items:center;
    justify-content:space-between;min-height:52px;
}
.topbar-nav{display:flex;align-items:center;gap:2px;}
.topbar-link{
    font-size:13px;font-weight:500;color:#506070;
    padding:6px 12px;border-radius:6px;cursor:pointer;
    transition:color .15s;
}
.topbar-link:hover{color:#c9d3e0;}
.topbar-link.active{color:#60a5fa;background:#0f1d35;}

/* CARDS */
.sw-card{
    background:#0d1525;border:1px solid #111c2e;
    border-radius:8px;padding:16px;margin-bottom:8px;
}
.sw-card:hover{border-color:#1a2840;}
.card-blue{background:linear-gradient(135deg,#060f2e,#0d1525);border-color:#1e3a8a;}
.card-gold{background:linear-gradient(135deg,#120d00,#0d1525);border-color:#854d0e;}
.card-green{background:linear-gradient(135deg,#002010,#0d1525);border-color:#14532d;}
.card-red{background:linear-gradient(135deg,#1c0000,#0d1525);border-color:#7f1d1d;}

/* INDEX CARD */
.idx{background:#0d1525;border:1px solid #111c2e;border-radius:8px;padding:14px 16px;}
.idx-name{font-size:10px;color:#4a6080;text-transform:uppercase;letter-spacing:.5px;}
.idx-price{font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;color:#e2e8f0;margin-top:2px;}
.idx-chg{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;margin-top:2px;}
.g{color:#22c55e;} .r{color:#ef4444;} .n{color:#64748b;}

/* STOCK ROW */
.sr{
    background:#0d1525;border:1px solid #111c2e;border-radius:8px;
    padding:12px 16px;margin-bottom:5px;
    display:flex;align-items:center;justify-content:space-between;
    transition:border-color .15s;
}
.sr:hover{border-color:#1e3a8a;}
.sr-tick{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:#60a5fa;}
.sr-name{font-size:11px;color:#2a3a50;margin-top:2px;}
.sr-why{font-size:11px;color:#3a5a70;margin-top:3px;font-style:italic;}
.sr-price{font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:700;color:#e2e8f0;}

/* BADGES */
.b{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;margin-right:3px;}
.b-bull{background:#052e16;color:#4ade80;border:1px solid #166534;}
.b-bear{background:#1c0000;color:#f87171;border:1px solid #7f1d1d;}
.b-neu{background:#0e1525;color:#64748b;border:1px solid #1e2a3a;}
.b-hot{background:#1c0800;color:#f97316;border:1px solid #92400e;}
.b-prem{background:#1c1000;color:#f59e0b;border:1px solid #854d0e;}
.b-new{background:#06163a;color:#60a5fa;border:1px solid #1e3a8a;}

/* SCORE */
.sc-pill{display:inline-block;padding:3px 10px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;}
.sc-hi{background:#052e16;color:#4ade80;border:1px solid #166534;}
.sc-md{background:#1c1000;color:#fbbf24;border:1px solid #854d0e;}
.sc-lo{background:#1c0000;color:#f87171;border:1px solid #7f1d1d;}

/* INSIGHT */
.ins{background:#0a1020;border-left:2px solid #2563eb;border-radius:0 6px 6px 0;padding:10px 14px;margin:4px 0;}
.ins-bull{border-left-color:#22c55e;}
.ins-bear{border-left-color:#ef4444;}

/* STAT */
.stat{background:#0d1525;border:1px solid #111c2e;border-radius:8px;padding:12px 14px;text-align:center;}
.stat-v{font-family:'JetBrains Mono',monospace;font-size:19px;font-weight:700;color:#e2e8f0;}
.stat-l{font-size:10px;color:#2a3a50;text-transform:uppercase;letter-spacing:.5px;margin-top:3px;}

/* HEATMAP */
.hm{border-radius:5px;padding:7px 3px;text-align:center;font-size:11px;font-weight:700;}
.hm-hi{background:#052e16;color:#4ade80;}
.hm-lo{background:#1c0000;color:#f87171;}
.hm-neu{background:#0e1525;color:#506070;}

/* MOVER ROW */
.mv{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #0e1525;font-size:13px;}
.mv:last-child{border-bottom:none;}

/* LOCK */
.lock{background:rgba(6,10,18,.95);border:1px solid #854d0e;border-radius:10px;padding:36px 24px;text-align:center;}

/* PRICING */
.pc{background:#0d1525;border:1px solid #111c2e;border-radius:10px;padding:28px 22px;}
.pc-feat{background:linear-gradient(160deg,#06163a,#0d1525);border:2px solid #2563eb;border-radius:10px;padding:28px 22px;position:relative;}
.pc-price{font-family:'JetBrains Mono',monospace;font-size:38px;font-weight:700;color:#e2e8f0;}

/* HERO */
.hero-wrap{
    background:radial-gradient(ellipse at 30% 50%,#061430 0%,#060a12 65%);
    border-bottom:1px solid #111c2e;
    padding:60px 48px 48px;
    display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;
}
.hero-eyebrow{font-size:11px;font-weight:700;color:#2563eb;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;}
.hero-h1{font-size:44px;font-weight:900;color:#f1f5f9;line-height:1.1;letter-spacing:-1.5px;margin-bottom:6px;}
.hero-h1 .hi{color:#2563eb;}
.hero-sub{font-size:15px;color:#4a6080;line-height:1.7;margin-bottom:28px;max-width:440px;}
.stats-bar{
    background:#0a1020;border-bottom:1px solid #111c2e;
    padding:18px 48px;display:flex;gap:48px;align-items:center;
}
.stats-val{font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:700;color:#e2e8f0;}
.stats-lbl{font-size:11px;color:#2a3a50;margin-top:1px;}
.stats-icon{font-size:20px;margin-right:10px;}

/* SEC HEADER */
.sec{
    font-size:15px;font-weight:700;color:#c9d3e0;
    display:flex;align-items:center;gap:8px;
    padding-bottom:10px;border-bottom:1px solid #111c2e;margin-bottom:12px;
}
.sec .cnt{font-size:10px;color:#2563eb;background:#06163a;border:1px solid #1e3a8a;padding:2px 8px;border-radius:20px;margin-left:auto;}

/* DEMO PANEL */
.demo-wrap{
    background:#0d1525;border:1px solid #1a2840;border-radius:12px;
    overflow:hidden;box-shadow:0 0 80px rgba(37,99,235,.06);
}
.demo-header{background:#080d18;border-bottom:1px solid #111c2e;padding:10px 14px;display:flex;align-items:center;gap:6px;}
.demo-dot{width:9px;height:9px;border-radius:50%;display:inline-block;}

/* ADMIN */
.admin-stat{background:#0a1020;border:1px solid #111c2e;border-radius:8px;padding:16px;text-align:center;}
.role-badge-owner{background:#1c0800;color:#f59e0b;border:1px solid #854d0e;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;}
.role-badge-admin{background:#06163a;color:#60a5fa;border:1px solid #1e3a8a;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;}
.role-badge-premium{background:#120d00;color:#a78bfa;border:1px solid #4c1d95;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;}
.role-badge-free{background:#0e1525;color:#506070;border:1px solid #1a2840;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;}

/* DISC */
.disc{background:#0a1020;border-left:2px solid #854d0e;border-radius:0 6px 6px 0;padding:12px 16px;font-size:11px;color:#2a3a50;line-height:1.7;margin-top:16px;}

/* Content padding */
.pg{padding:20px 24px;}
.pg-sm{padding:12px 24px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────
CATEGORIES = {
    "🔥 Trending Now":        [],
    "📡 Social Buzz":         ["GME","AMC","BBIG","MULN","FFIE","ATER","SPCE","HOOD","CLOV","MSTR","PLTR","SNDL","BBAI","SOUN","ASTS"],
    "💥 Squeeze Radar":       [],
    "📈 Momentum Movers":     [],
    "🔄 Reversal Candidates": [],
    "💻 Tech":                ["AAPL","MSFT","GOOGL","META","AMZN","NVDA","AMD","INTC","QCOM","AVGO","CRM","ORCL","ADBE","NOW","SNOW","UBER","SHOP","SQ","PYPL","NET","DDOG","MDB","OKTA","ZS","CRWD"],
    "🤖 AI":                  ["NVDA","AMD","PLTR","MSFT","GOOGL","IBM","SOUN","BBAI","AI","ASTS","IONQ","QUBT","RGTI","SMCI","DELL","HPE","ARM","ALAB","MRVL"],
    "⚡ EV":                  ["TSLA","RIVN","LCID","NIO","LI","XPEV","F","GM","CHPT","BLNK","ACHR","JOBY","LILM"],
    "🧬 Biotech":             ["MRNA","BNTX","NVAX","VRTX","REGN","BIIB","GILD","AMGN","SRPT","EDIT","CRSP","BEAM","NTLA"],
    "📊 S&P 500":             ["AAPL","MSFT","AMZN","GOOGL","META","TSLA","NVDA","JPM","JNJ","V","PG","MA","UNH","HD","XOM","CVX","LLY","ABBV","MRK","PFE","BAC","WMT","KO","DIS","NFLX"],
    "💹 NASDAQ":              ["AAPL","MSFT","AMZN","NVDA","META","GOOGL","TSLA","AVGO","COST","AMD","CSCO","ADBE","QCOM","AMGN","INTU","ISRG","REGN","VRTX","PANW","LRCX"],
    "🏦 Russell 1000":        ["IWB","AAPL","MSFT","AMZN","NVDA","META","GOOGL","TSLA","JPM","JNJ","V","PG","MA","UNH","HD"],
    "🔬 Small Cap":           ["FFIE","MULN","NKLA","GOEV","WKHS","HCDI","ATER","SPCE","SOUN","BBAI","ASTS","IONQ","QUBT","RGTI","MNMD","ACHR"],
    "🎭 Meme / Social":       ["GME","AMC","BBIG","MULN","FFIE","ATER","SPCE","HOOD","CLOV","WKHS"],
}

PREMIUM_CATS   = {"💥 Squeeze Radar","📈 Momentum Movers","🔄 Reversal Candidates"}
FREE_CATS      = [c for c in CATEGORIES if c not in PREMIUM_CATS]
SECTOR_ETFS    = {"Technology":"XLK","Healthcare":"XLV","Financials":"XLF","Energy":"XLE",
                  "Cons Disc":"XLY","Industrials":"XLI","Materials":"XLB","Utilities":"XLU",
                  "Real Estate":"XLRE","Comm Svcs":"XLC"}
INDEXES        = {"NASDAQ":"^IXIC","S&P 500":"^GSPC","DOW":"^DJI","VIX":"^VIX","Russell":"^RUT"}
BI_UNIVERSE    = ["AAPL","MSFT","NVDA","AMD","TSLA","META","AMZN","GOOGL","PLTR","MSTR",
                  "GME","AMC","RIVN","MRNA","BNTX","SMCI","ARM","SOUN","ASTS","IONQ",
                  "JPM","BAC","XOM","LLY","ABBV","VRTX","CRSP","AVGO","QCOM","IBM"]
ROLE_HIERARCHY = ["owner","admin","premium","free","guest"]

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────
def init():
    now = datetime.now().strftime("%Y-%m-%d")
    d = {
        "page":"landing","user":None,"role":"guest",
        "watchlist":[],"saved_screeners":[],"alerts":[],
        "detail_ticker":None,"detail_data":{},
        "discover_cat":"💻 Tech","admin_tab":"Overview",
        "hero_panel":0,
        "users_db":{
            "owner@stockwins.com":   {"pw":_hp("owner123"),  "name":"Owner",       "role":"owner",   "verified":True, "joined":now,"alerts":[],"plan":"Annual"},
            "admin@stockwins.com":   {"pw":_hp("admin123"),  "name":"Admin",        "role":"admin",   "verified":True, "joined":now,"alerts":[],"plan":"Annual"},
            "demo@stockwins.com":    {"pw":_hp("demo123"),   "name":"Demo User",    "role":"free",    "verified":True, "joined":now,"alerts":[],"plan":"Free"},
            "premium@stockwins.com": {"pw":_hp("premium1"),  "name":"Alex Rivera",  "role":"premium", "verified":True, "joined":now,"alerts":[],"plan":"Monthly"},
        },
        "site_stats":{
            "total_signups":1847,"premium_users":312,"daily_active":634,
            "conversion_rate":16.9,"most_viewed":"🔥 Trending Now",
            "top_watchlisted":["NVDA","TSLA","AAPL","AMD","MSTR"],
        },
        "api_override":"",  # admin can set a Twelve Data key via admin panel
    }
    for k,v in d.items():
        if k not in st.session_state: st.session_state[k]=v

def _hp(pw): return hashlib.sha256(pw.encode()).hexdigest()

init()

# ─────────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────────
def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()

def login(email,pw):
    db=st.session_state.users_db
    if email in db and db[email]["pw"]==hp(pw):
        st.session_state.user={"email":email,"name":db[email]["name"]}
        st.session_state.role=db[email]["role"]
        return True
    return False

def signup(email,pw,name):
    db=st.session_state.users_db
    if email in db: return False,"Account already exists."
    db[email]={"pw":hp(pw),"name":name,"role":"free","verified":False,
               "joined":datetime.now().strftime("%Y-%m-%d"),"alerts":[],"plan":"Free"}
    st.session_state.users_db=db
    st.session_state.site_stats["total_signups"]+=1
    st.session_state.user={"email":email,"name":name}
    st.session_state.role="free"
    return True,"Welcome!"

def logout():
    st.session_state.user=None; st.session_state.role="guest"; nav("landing")

def is_owner():   return st.session_state.role=="owner"
def is_admin():   return st.session_state.role in ("owner","admin")
def is_premium(): return st.session_state.role in ("owner","admin","premium")
def is_authed():  return st.session_state.user is not None
def nav(p):       st.session_state.page=p; st.rerun()
def get_db_user():
    if not is_authed(): return {}
    return st.session_state.users_db.get(st.session_state.user["email"],{})

def get_td_key():
    """API key — from Streamlit secrets, then admin override. NEVER shown to regular users."""
    try:    return st.secrets.get("TWELVE_DATA_API_KEY","") or st.session_state.api_override
    except: return st.session_state.api_override

# ─────────────────────────────────────────────────────────────────────
# DATA — Primary: yfinance (free, no key, always works)
#        Secondary: Twelve Data (admin-configured, better quality)
# ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def yf_quote(ticker):
    """Live quote via yfinance — free, no API key needed."""
    try:
        tk = yf.Ticker(ticker)
        h  = tk.history(period="2d",interval="1d")
        i  = tk.info
        if len(h)<1: return None
        price = round(float(h["Close"].iloc[-1]),2)
        prev  = round(float(h["Close"].iloc[-2]),2) if len(h)>=2 else price
        return {
            "price":price,"prev":prev,"open":round(float(h["Open"].iloc[-1]),2),
            "high":round(float(h["High"].iloc[-1]),2),"low":round(float(h["Low"].iloc[-1]),2),
            "volume":int(h["Volume"].iloc[-1]),
            "pct":round(((price-prev)/prev)*100,2) if prev else 0,
            "chg":round(price-prev,2),
            "name":i.get("shortName",i.get("longName",ticker))[:30],
        }
    except: return None

@st.cache_data(ttl=600)
def yf_ohlcv(ticker,n=60):
    """OHLCV history via yfinance — free."""
    try:
        h = yf.Ticker(ticker).history(period=f"{min(n+10,120)}d")
        if len(h)<5: return None
        df = h.tail(n).reset_index()
        df.columns=[c.lower() for c in df.columns]
        df=df.rename(columns={"date":"datetime"})
        return df[["datetime","open","high","low","close","volume"]].copy()
    except: return None

@st.cache_data(ttl=3600)
def yf_fundamentals(ticker):
    try:
        i=yf.Ticker(ticker).info
        return {"mktcap":i.get("marketCap",0),"sf":i.get("shortPercentOfFloat",0),
                "dtc":i.get("shortRatio",0),"avgvol":i.get("averageVolume",0),
                "sector":i.get("sector","N/A"),"industry":i.get("industry","N/A"),
                "pe":i.get("trailingPE",None),"hi52":i.get("fiftyTwoWeekHigh",0),
                "lo52":i.get("fiftyTwoWeekLow",0),"beta":i.get("beta",None),
                "desc":(i.get("longBusinessSummary","")[:280]+"...") if i.get("longBusinessSummary") else ""}
    except: return {}

@st.cache_data(ttl=600)
def td_quote_api(ticker,key):
    if not key: return None
    try:
        d=requests.get(f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={key}",timeout=8).json()
        if "close" not in d: return None
        return {"price":float(d.get("close",0)),"open":float(d.get("open",0)),
                "high":float(d.get("high",0)),"low":float(d.get("low",0)),
                "volume":int(d.get("volume",0)),"prev":float(d.get("previous_close",0)),
                "chg":float(d.get("change",0)),"pct":float(d.get("percent_change",0)),
                "name":d.get("name",ticker)}
    except: return None

def get_quote(ticker):
    """Unified quote: try Twelve Data first if key available, fallback to yfinance."""
    key = get_td_key()
    if key:
        q = td_quote_api(ticker, key)
        if q: return q
    return yf_quote(ticker)

@st.cache_data(ttl=600)
def td_ohlcv_api(ticker,key,n=60):
    if not key: return None
    try:
        d=requests.get(f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize={n}&apikey={key}",timeout=10).json()
        if "values" not in d: return None
        df=pd.DataFrame(d["values"])
        for c in ["open","high","low","close","volume"]: df[c]=df[c].astype(float)
        return df.iloc[::-1].reset_index(drop=True)
    except: return None

def get_ohlcv(ticker,n=60):
    key=get_td_key()
    if key:
        df=td_ohlcv_api(ticker,key,n)
        if df is not None: return df
    return yf_ohlcv(ticker,n)

@st.cache_data(ttl=900)
def st_hot():
    try:
        d=requests.get("https://api.stocktwits.com/api/2/trending/symbols.json",timeout=8).json()
        return [s["symbol"] for s in d.get("symbols",[])]
    except: return ["NVDA","TSLA","AAPL","AMD","MSTR","PLTR","META","MSFT","GME","AMC"]

@st.cache_data(ttl=900)
def st_sentiment(ticker):
    try:
        d=requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json",timeout=8).json()
        msgs=d.get("messages",[])
        bull=sum(1 for m in msgs if m.get("entities",{}).get("sentiment",{}) and m["entities"]["sentiment"].get("basic")=="Bullish")
        bear=sum(1 for m in msgs if m.get("entities",{}).get("sentiment",{}) and m["entities"]["sentiment"].get("basic")=="Bearish")
        tot=bull+bear
        return {"bull":round((bull/tot)*100) if tot else 50,"bear":round((bear/tot)*100) if tot else 50,
                "msgs":len(msgs),"wl":d.get("symbol",{}).get("watchlist_count",0)}
    except: return {"bull":50,"bear":50,"msgs":0,"wl":0}

@st.cache_data(ttl=300)
def get_indexes():
    out={}
    for n,t in INDEXES.items():
        try:
            h=yf.Ticker(t).history(period="5d")
            if len(h)>=2:
                p=h["Close"].iloc[-1]; pv=h["Close"].iloc[-2]
                trend=[round(float(v),2) for v in h["Close"].tail(5).values]
                out[n]={"price":round(p,2),"pct":round(((p-pv)/pv)*100,2),"trend":trend}
        except: out[n]={"price":0,"pct":0,"trend":[]}
    return out

@st.cache_data(ttl=900)
def get_sectors():
    out={}
    for s,e in SECTOR_ETFS.items():
        try:
            h=yf.Ticker(e).history(period="5d")
            if len(h)>=2: out[s]=round(((h["Close"].iloc[-1]-h["Close"].iloc[-2])/h["Close"].iloc[-2])*100,2)
        except: out[s]=0.0
    return out

@st.cache_data(ttl=600)
def get_bi_movers():
    out=[]
    for t in BI_UNIVERSE:
        try:
            h=yf.Ticker(t).history(period="5d")
            if len(h)>=2:
                p=h["Close"].iloc[-1]; pv=h["Close"].iloc[-2]
                v=h["Volume"].iloc[-1]; av=h["Volume"].mean()
                out.append({"t":t,"price":round(p,2),"pct":round(((p-pv)/pv)*100,2),"vol":int(v),"vr":round(v/av,1) if av>0 else 1})
        except: continue
    return out

# ─────────────────────────────────────────────────────────────────────
# SCORING ENGINE — 6 component scores → unified 0-100
# ─────────────────────────────────────────────────────────────────────
def compute_scores(df, info=None, sent=None):
    """Returns (total_score, component_scores_dict, opportunity_type, risk_level, confidence)."""
    if df is None or len(df)<14: return 0,{},"N/A","Unknown","Low"
    bd={}; total=0
    try:
        dfc=df.copy()
        dfc["rsi"]=ta.momentum.RSIIndicator(dfc["close"],14).rsi()
        dfc["ma20"]=dfc["close"].rolling(20).mean()
        dfc["ma50"]=dfc["close"].rolling(min(50,len(dfc))).mean()
        mac=ta.trend.MACD(dfc["close"])
        dfc["macd"]=mac.macd(); dfc["macd_s"]=mac.macd_signal()
        bb=ta.volatility.BollingerBands(dfc["close"])
        dfc["bb_p"]=bb.bollinger_pband()
        lat=dfc.iloc[-1]; rsi=lat["rsi"]; price=lat["close"]

        # Momentum Score (RSI-based, 0-25)
        if pd.notna(rsi):
            ms=25 if rsi<30 else 20 if rsi<40 else 18 if rsi<=55 else 12 if rsi<=70 else 4
            total+=ms; bd["Momentum"]=ms

        # Trend Score (MA-based, 0-20)
        if pd.notna(lat["ma20"]) and pd.notna(lat["ma50"]):
            ts=0
            if price>lat["ma20"]: ts+=8
            if price>lat["ma50"]: ts+=8
            if lat["ma20"]>lat["ma50"]: ts+=4
            total+=ts; bd["Trend"]=ts

        # MACD Score (0-15)
        if pd.notna(lat["macd"]) and pd.notna(lat["macd_s"]):
            ms2=15 if (lat["macd"]>lat["macd_s"] and lat["macd"]>0) else 9 if lat["macd"]>lat["macd_s"] else 4 if lat["macd"]>0 else 0
            total+=ms2; bd["MACD"]=ms2

        # Volume Score (0-15)
        if "volume" in dfc.columns:
            avg=dfc["volume"].rolling(20).mean().iloc[-1]
            if pd.notna(avg) and avg>0:
                r=lat["volume"]/avg
                vs=15 if r>=3 else 11 if r>=2 else 7 if r>=1.5 else 4 if r>=1 else 1
                total+=vs; bd["Volume"]=vs

        # Sentiment Score (0-15)
        if sent:
            bp=sent.get("bull",50)
            ss=15 if bp>=75 else 10 if bp>=60 else 6 if bp>=50 else 2
            total+=ss; bd["Sentiment"]=ss

        # Squeeze Score (0-10)
        if info:
            sf=(info.get("sf",0) or 0)*100; dt=info.get("dtc",0) or 0
            sq=10 if (sf>=20 and dt>=5) else 6 if sf>=15 else 2 if sf>=10 else 0
            total+=sq; bd["Squeeze"]=sq

    except: pass

    sc=min(int(total),100)

    # Opportunity type
    if bd.get("Squeeze",0)>=6 and bd.get("Momentum",0)>=15: op="Short Squeeze Setup"
    elif bd.get("Momentum",0)==25:   op="Oversold Bounce"
    elif bd.get("Trend",0)>=18:      op="Uptrend Continuation"
    elif bd.get("Volume",0)>=11:     op="Volume Surge"
    elif bd.get("MACD",0)==15:       op="MACD Momentum"
    else:                            op="Mixed Signals"

    # Risk level
    try:
        vol_std=df["close"].pct_change().std()*100
        beta=info.get("beta",1) or 1 if info else 1
        sf=(info.get("sf",0) or 0)*100 if info else 0
        mc=info.get("mktcap",0) or 0 if info else 0
        rs=0
        if beta>2: rs+=3
        elif beta>1.5: rs+=2
        elif beta>1: rs+=1
        if vol_std>4: rs+=3
        elif vol_std>2: rs+=2
        elif vol_std>1: rs+=1
        if sf>20: rs+=2
        elif sf>10: rs+=1
        if mc<500e6: rs+=2
        elif mc<2e9: rs+=1
        risk="Very High" if rs>=6 else "High" if rs>=4 else "Medium" if rs>=2 else "Low"
    except: risk="Unknown"

    confidence="High" if sc>=65 else "Medium" if sc>=40 else "Low"
    return sc,bd,op,risk,confidence

def get_insights(df,info=None):
    """Returns list of (label, plain_english_text, sentiment, confidence) tuples."""
    out=[]
    if df is None or len(df)<14: return out
    try:
        dfc=df.copy()
        dfc["rsi"]=ta.momentum.RSIIndicator(dfc["close"],14).rsi()
        dfc["ma20"]=dfc["close"].rolling(20).mean()
        dfc["ma50"]=dfc["close"].rolling(min(50,len(dfc))).mean()
        mac=ta.trend.MACD(dfc["close"])
        dfc["macd"]=mac.macd(); dfc["macd_s"]=mac.macd_signal()
        bb=ta.volatility.BollingerBands(dfc["close"])
        dfc["bb"]=bb.bollinger_pband()
        lat=dfc.iloc[-1]; prev=dfc.iloc[-2]
        rsi=lat["rsi"]; price=lat["close"]

        if pd.notna(rsi):
            if rsi<30:       out.append(("RSI Oversold","The stock has dropped hard and fast recently. Historically, extreme selloffs like this can lead to a bounce back as buyers step in.","bull","Medium"))
            elif rsi>70:     out.append(("RSI Overbought","The stock has surged quickly and is now in stretched territory. Be cautious — sharp rises can be followed by profit-taking.","bear","Medium"))
            elif 55<rsi<=70: out.append(("Strong Momentum","Momentum is healthy and moving in the right direction without being dangerously overbought yet.","bull","Medium"))
            else:            out.append(("Neutral Momentum","The stock is neither overbought nor oversold — no extreme pressure in either direction.","neu","Low"))

        if pd.notna(lat["ma20"]) and pd.notna(lat["ma50"]):
            if price>lat["ma20"] and price>lat["ma50"]:
                out.append(("Above Key Averages","The stock is trading above both its 20-day and 50-day average prices. This means buyers have been consistently in control — a healthy uptrend.","bull","High"))
            elif price<lat["ma20"] and price<lat["ma50"]:
                out.append(("Below Key Averages","The stock is trading below its recent averages. This tells us sellers have been winning — the trend is currently pointing down.","bear","High"))
            if prev["ma20"]<prev["ma50"] and lat["ma20"]>lat["ma50"]:
                out.append(("Golden Cross ✨","A major bullish event just happened: the short-term trend crossed above the long-term trend. Many traders treat this as a serious buy signal.","bull","High"))
            elif prev["ma20"]>prev["ma50"] and lat["ma20"]<lat["ma50"]:
                out.append(("Death Cross 💀","A serious bearish signal: the short-term trend just crossed below the long-term trend. This often signals that a downtrend is gaining strength.","bear","High"))

        if pd.notna(lat["macd"]) and pd.notna(lat["macd_s"]):
            if lat["macd"]>lat["macd_s"] and prev["macd"]<=prev["macd_s"]:
                out.append(("MACD Bullish Crossover","Momentum just flipped positive. This means buying pressure is building — often a good signal for upside continuation.","bull","High"))
            elif lat["macd"]<lat["macd_s"] and prev["macd"]>=prev["macd_s"]:
                out.append(("MACD Bearish Crossover","Momentum just turned negative. Selling pressure is increasing — this can signal further downside ahead.","bear","High"))
            elif lat["macd"]>0: out.append(("MACD Positive","The overall momentum signal favors buyers right now.","bull","Medium"))
            else:               out.append(("MACD Negative","The overall momentum signal currently favors sellers.","bear","Medium"))

        if "volume" in dfc.columns:
            avg=dfc["volume"].rolling(20).mean().iloc[-1]
            if pd.notna(avg) and avg>0:
                r=lat["volume"]/avg
                if r>=2:
                    d_="bull" if lat["close"]>prev["close"] else "bear"
                    out.append(("Volume Spike 🔊",f"Today's trading volume is {r:.1f}× higher than normal. When a price move happens on unusually high volume, it tends to be more reliable and sustained.",d_,"High"))
                elif r<0.5:
                    out.append(("Low Volume Warning","Very few traders are active in this stock today. Moves on low volume are unreliable and easier to reverse.","neu","Low"))

        if info:
            sf=(info.get("sf",0) or 0)*100; dtc=info.get("dtc",0) or 0
            if sf>=20:
                out.append(("High Short Interest 🎯",f"{sf:.1f}% of available shares are currently sold short — traders betting the price falls. If the stock rises instead, those traders are forced to buy back shares, which can accelerate a big upward move (squeeze).","bull","High"))
            if dtc>=5:
                out.append(("High Days-to-Cover",f"It would take approximately {dtc:.0f} days of average trading volume to close all short positions. This creates a 'fuel tank' for a potential squeeze.","bull","Medium"))

        if pd.notna(lat["bb"]):
            if lat["bb"]<0:   out.append(("Near Lower Band","The stock is at the bottom of its typical price range — this has historically led to bounces.","bull","Medium"))
            elif lat["bb"]>1: out.append(("Near Upper Band","The stock is stretched to the top of its normal price range and may face resistance.","bear","Medium"))
    except: pass
    return out

def get_why_text(ticker, insights_list, score, sent, info):
    """One-line plain-English reason for why a stock is on the list."""
    sf=(info.get("sf",0) or 0)*100 if info else 0
    if sf>=20 and score>=50: return f"High short float ({sf:.0f}%) + rising momentum = squeeze candidate"
    for lbl,txt,s,_ in insights_list:
        if "Golden Cross" in lbl: return "Short-term trend just crossed above long-term — major bullish event"
        if "Oversold" in lbl:     return "May have dropped too far too fast — bounce setup forming"
        if "Volume Spike" in lbl: return f"Unusual trading activity detected — {(info or {}).get('avgvol',0)/1e6:.1f}M avg vs today"
        if "Bullish Cross" in lbl: return "MACD just turned positive — buyers gaining control"
    bull=sent.get("bull",50) if sent else 50
    if bull>=70: return f"{bull}% of traders on StockTwits are bullish right now"
    if score>=70: return "Strong multi-factor signal across momentum, volume, and trend"
    return "Flagged by StockWins scoring engine — review insights below"

# ─────────────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────
def sc_pill(sc):
    cls="sc-hi" if sc>=65 else "sc-md" if sc>=40 else "sc-lo"
    return f'<span class="sc-pill {cls}">{sc}</span>'

def risk_color(r):
    return {"Low":"#22c55e","Low-Medium":"#4ade80","Medium":"#fbbf24","Medium-High":"#fb923c","High":"#ef4444","Very High":"#dc2626"}.get(r,"#64748b")

def render_ins(label,text,sentiment,confidence):
    cls="ins-bull" if sentiment=="bull" else "ins-bear" if sentiment=="bear" else ""
    bc="b-bull" if sentiment=="bull" else "b-bear" if sentiment=="bear" else "b-neu"
    bl="Bullish" if sentiment=="bull" else "Bearish" if sentiment=="bear" else "Neutral"
    st.markdown(f"""<div class="ins {cls}">
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:12px;font-weight:700;color:#c9d3e0;">{label}</span>
            <span class="b {bc}">{bl}</span>
            <span style="font-size:10px;color:#2a3a50;margin-left:auto;">{confidence} confidence</span>
        </div>
        <div style="font-size:12px;color:#3a5068;line-height:1.55;">{text}</div>
    </div>""", unsafe_allow_html=True)

def render_lock(name="This Feature"):
    st.markdown(f"""<div class="lock">
        <div style="font-size:30px;margin-bottom:10px;">🔒</div>
        <div style="font-size:17px;font-weight:800;color:#e2e8f0;margin-bottom:6px;">{name} — Premium Only</div>
        <div style="font-size:13px;color:#3a5068;margin-bottom:16px;">Upgrade to unlock all premium categories, short squeeze scanner, advanced screener, and full BI analytics.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if st.button("🚀 Go Premium →",type="primary",key=f"lock_{name}"): nav("pricing")

def render_stock_row(ticker, q, sc, insigs, info=None, sent=None, hot=False, op="", risk=""):
    if not q: return
    pct=q.get("pct",0); price=q.get("price",0)
    cc="#22c55e" if pct>=0 else "#ef4444"
    ar="▲" if pct>=0 else "▼"
    rc=risk_color(risk)
    hot_b='<span class="b b-hot">🔥 HOT</span>' if hot else ""
    op_b=f'<span class="b b-new">{op}</span>' if op else ""
    sigs="".join([f'<span class="b b-{"bull" if s=="bull" else "bear" if s=="bear" else "neu"}">{l[:15]}</span>'
                  for l,_,s,_ in insigs[:2]])
    why=get_why_text(ticker,insigs,sc,sent,info)

    st.markdown(f"""<div class="sr">
        <div style="flex:2.5;">
            <div style="display:flex;align-items:center;gap:6px;">
                <span class="sr-tick">{ticker}</span>{hot_b}{op_b}
            </div>
            <div class="sr-name">{q.get('name','')[:28]}</div>
            <div class="sr-why">→ {why}</div>
            <div style="margin-top:5px;">{sigs}</div>
        </div>
        <div style="text-align:center;min-width:80px;">
            <div style="font-size:10px;color:#2a3a50;margin-bottom:2px;">RISK</div>
            <div style="font-size:11px;font-weight:700;color:{rc};">{risk}</div>
        </div>
        <div style="text-align:right;min-width:110px;">
            <div class="sr-price">${price:,.2f}</div>
            <div style="font-size:12px;font-weight:700;color:{cc};font-family:'JetBrains Mono',monospace;">{ar}{abs(pct):.2f}%</div>
            <div style="margin-top:4px;">{sc_pill(sc)}</div>
        </div>
    </div>""", unsafe_allow_html=True)

def render_topbar(active=""):
    c1,c2,c3=st.columns([2,7,3])
    with c1:
        st.markdown(f'<div style="padding:6px 0;"><span class="sw-logo">Stock<span class="w">W</span>ins</span></div>',unsafe_allow_html=True)
        if st.button("Home",key="logo_home",label_visibility="collapsed"):
            nav("landing" if not is_authed() else "dashboard")
    with c2:
        if is_authed():
            pages=[("Dashboard","dashboard"),("Discover","discover"),
                   ("Watchlist","watchlist"),("Screener","screener"),
                   ("BI Analytics","bi_dashboard"),("Pricing","pricing")]
            if is_admin(): pages.append(("🛠 Admin","admin"))
            ncols=st.columns(len(pages))
            for col,(lbl,pg) in zip(ncols,pages):
                with col:
                    if st.button(lbl,key=f"top_{pg}"):nav(pg)
    with c3:
        if is_authed():
            cc1,cc2,cc3=st.columns([3,1,1])
            role_icon={"owner":"👑","admin":"🛡","premium":"⭐","free":"👤"}.get(st.session_state.role,"👤")
            with cc1: st.markdown(f'<div style="font-size:12px;color:#4a6080;padding-top:9px;">{role_icon} {st.session_state.user["name"]}</div>',unsafe_allow_html=True)
            with cc2:
                if st.button("⚙",key="top_set",help="Settings"):nav("settings")
            with cc3:
                if st.button("↩",key="top_out",help="Logout"):logout()
        else:
            lc1,lc2=st.columns(2)
            with lc1:
                if st.button("Login",key="top_login"):nav("login")
            with lc2:
                if st.button("Sign Up",key="top_signup",type="primary"):nav("signup")
    st.divider()

def render_sidebar():
    with st.sidebar:
        st.markdown("""<div style="padding:18px 16px 10px;">
            <div class="sw-logo">Stock<span class="w">W</span>ins</div>
            <div style="font-size:10px;color:#1e2d42;margin-top:2px;">Market Intelligence Platform</div>
        </div>""", unsafe_allow_html=True)
        st.divider()

        if is_authed():
            cur=st.session_state.page
            st.markdown('<div class="nav-sec">Market</div>',unsafe_allow_html=True)
            for icon,label,pg,kw in [
                ("📊","Market Overview","dashboard","dashboard"),
                ("🔥","Trending Now","discover","discover_trending"),
                ("📡","Social Buzz","discover","discover_social"),
                ("💥","Squeeze Radar","discover","discover_squeeze"),
                ("📈","Momentum Movers","discover","discover_momentum"),
                ("🔄","Reversal Candidates","discover","discover_reversal"),
            ]:
                active="active" if cur==pg and st.session_state.get("discover_cat","")==label else ("active" if cur==pg and pg=="dashboard" else "")
                st.markdown(f'<div class="nav-item-wrap"><div class="nav-label {active}"><span class="icon">{icon}</span>{label}</div></div>',unsafe_allow_html=True)
                if st.button(label,key=f"sb_{kw}",label_visibility="collapsed",use_container_width=True):
                    if pg=="discover": st.session_state.discover_cat=label
                    nav(pg)

            st.markdown('<div class="nav-sec">Tools</div>',unsafe_allow_html=True)
            for icon,label,pg in [("🔍","Smart Screener","screener"),("📊","BI Analytics","bi_dashboard"),("⭐","Watchlist","watchlist"),("💰","Pricing","pricing")]:
                active="active" if cur==pg else ""
                st.markdown(f'<div class="nav-item-wrap"><div class="nav-label {active}"><span class="icon">{icon}</span>{label}</div></div>',unsafe_allow_html=True)
                if st.button(label,key=f"sb_{pg}",label_visibility="collapsed",use_container_width=True): nav(pg)

            if is_admin():
                st.markdown('<div class="nav-sec">Admin</div>',unsafe_allow_html=True)
                active="active" if cur=="admin" else ""
                st.markdown(f'<div class="nav-item-wrap"><div class="nav-label {active}"><span class="icon">🛠️</span>Admin Panel</div></div>',unsafe_allow_html=True)
                if st.button("Admin Panel",key="sb_admin",label_visibility="collapsed",use_container_width=True): nav("admin")

        else:
            st.markdown('<div style="padding:12px 16px;">',unsafe_allow_html=True)
            st.info("Sign in for the full dashboard.")
            if st.button("Login →",key="sb_login",use_container_width=True): nav("login")
            if st.button("Sign Up Free →",key="sb_signup",use_container_width=True,type="primary"): nav("signup")
            st.markdown('</div>',unsafe_allow_html=True)
            st.markdown("""<div style="padding:12px 16px;background:#080d18;margin:8px;border-radius:8px;border:1px solid #111c2e;">
                <div style="font-size:11px;font-weight:700;color:#1e2d42;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;">What You Get Free</div>
                <div style="font-size:12px;color:#2a3a50;line-height:2;">✅ Market overview<br>✅ 5+ stock categories<br>✅ Social sentiment<br>✅ Plain-English insights<br>✅ Watchlist</div>
            </div>""",unsafe_allow_html=True)

        st.divider()
        st.markdown(f'<div style="padding:6px 16px;font-size:10px;color:#111c2e;">© 2026 StockWins · Educational use only</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# DEMO SVG PANELS for hero rotation
# ─────────────────────────────────────────────────────────────────────
DEMO_PANELS = [
    # Panel 1: Market Overview
    """<div style="background:#0d1525;border:1px solid #1a2840;border-radius:10px;overflow:hidden;box-shadow:0 0 60px rgba(37,99,235,.08);">
      <div style="background:#080d18;border-bottom:1px solid #111c2e;padding:9px 14px;display:flex;align-items:center;gap:6px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#ef4444;"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#fbbf24;"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;"></div>
        <span style="font-size:11px;color:#2a3a50;margin-left:8px;font-family:'JetBrains Mono',monospace;">Market Overview</span>
      </div>
      <div style="padding:14px;">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;">
          <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:10px;">
            <div style="font-size:9px;color:#3a5068;">NASDAQ</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:700;color:#e2e8f0;">18,965</div>
            <div style="font-size:11px;font-weight:700;color:#22c55e;">▲ 2.99%</div>
          </div>
          <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:10px;">
            <div style="font-size:9px;color:#3a5068;">S&P 500</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:700;color:#e2e8f0;">5,318</div>
            <div style="font-size:11px;font-weight:700;color:#22c55e;">▲ 1.25%</div>
          </div>
          <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:10px;">
            <div style="font-size:9px;color:#3a5068;">VIX</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:700;color:#e2e8f0;">18.40</div>
            <div style="font-size:11px;font-weight:700;color:#ef4444;">▼ 3.92%</div>
          </div>
        </div>
        <div style="font-size:10px;color:#3a5068;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px;">StockTwits Hot Stocks</div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:9px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">AAPL</span><div style="font-size:10px;color:#2a3a50;">Trending on StockTwits</div><div style="margin-top:4px;"><span style="background:#052e16;color:#4ade80;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;">RSI Oversold</span><span style="background:#1c0800;color:#f97316;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;margin-left:3px;">🔥 HOT</span></div></div>
          <div style="text-align:right;"><div style="font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:#e2e8f0;">$182.50</div><div style="font-size:11px;font-weight:700;color:#22c55e;">▲ 1.99%</div><div style="font-size:10px;color:#2563eb;background:#06163a;border:1px solid #1e3a8a;padding:1px 8px;border-radius:3px;margin-top:3px;">72</div></div>
        </div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:9px 12px;display:flex;justify-content:space-between;align-items:center;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">NVDA</span><div style="font-size:10px;color:#2a3a50;">AI momentum leader</div><div style="margin-top:4px;"><span style="background:#052e16;color:#4ade80;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;">Golden Cross ✨</span></div></div>
          <div style="text-align:right;"><div style="font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:#e2e8f0;">$875.40</div><div style="font-size:11px;font-weight:700;color:#22c55e;">▲ 3.21%</div><div style="font-size:10px;color:#4ade80;background:#052e16;padding:1px 8px;border-radius:3px;margin-top:3px;">88</div></div>
        </div>
      </div>
    </div>""",

    # Panel 2: Short Squeeze
    """<div style="background:#0d1525;border:1px solid #1a2840;border-radius:10px;overflow:hidden;box-shadow:0 0 60px rgba(37,99,235,.08);">
      <div style="background:#080d18;border-bottom:1px solid #111c2e;padding:9px 14px;display:flex;align-items:center;gap:6px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#ef4444;"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#fbbf24;"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;"></div>
        <span style="font-size:11px;color:#2a3a50;margin-left:8px;font-family:'JetBrains Mono',monospace;">Short Squeeze Radar</span>
        <span style="background:#1c1000;color:#f59e0b;font-size:9px;font-weight:700;padding:2px 8px;border-radius:20px;margin-left:auto;">⭐ PREMIUM</span>
      </div>
      <div style="padding:14px;">
        <div style="font-size:10px;color:#3a5068;margin-bottom:8px;">Short float ≥ 20% · Days-to-cover ≥ 3</div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:9px 12px;margin-bottom:5px;display:flex;justify-content:space-between;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">AMC</span><div style="font-size:10px;color:#2a3a50;">Short interest drove past resistance</div><div style="margin-top:4px;"><span style="background:#052e16;color:#4ade80;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;">High Short Float</span></div></div>
          <div style="text-align:right;"><div style="font-size:9px;color:#2a3a50;">Short Float</div><div style="font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;color:#ef4444;">28.4%</div><div style="font-size:9px;color:#2a3a50;margin-top:2px;">Days: 6.2</div></div>
        </div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:9px 12px;margin-bottom:5px;display:flex;justify-content:space-between;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">CVNA</span><div style="font-size:10px;color:#2a3a50;">Breaking higher post-squeeze setup</div><div style="margin-top:4px;"><span style="background:#052e16;color:#4ade80;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;">Volume Spike</span></div></div>
          <div style="text-align:right;"><div style="font-size:9px;color:#2a3a50;">SW Score</div><div style="font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;color:#4ade80;">82</div><div style="font-size:9px;color:#4ade80;">▲ +19.35%</div></div>
        </div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:9px 12px;display:flex;justify-content:space-between;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">MSTR</span><div style="font-size:10px;color:#2a3a50;">Bitcoin correlation, high short squeeze risk</div></div>
          <div style="text-align:right;"><div style="font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:#e2e8f0;">$11,601</div><div style="font-size:11px;font-weight:700;color:#22c55e;">▲ 185.84%</div></div>
        </div>
      </div>
    </div>""",

    # Panel 3: Momentum
    """<div style="background:#0d1525;border:1px solid #1a2840;border-radius:10px;overflow:hidden;box-shadow:0 0 60px rgba(37,99,235,.08);">
      <div style="background:#080d18;border-bottom:1px solid #111c2e;padding:9px 14px;display:flex;align-items:center;gap:6px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#ef4444;"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#fbbf24;"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;"></div>
        <span style="font-size:11px;color:#2a3a50;margin-left:8px;font-family:'JetBrains Mono',monospace;">Momentum Movers</span>
      </div>
      <div style="padding:14px;">
        <div style="font-size:10px;color:#3a5068;margin-bottom:8px;display:flex;justify-content:space-between;"><span>Sector Performance Today</span><span>BI Analytics View</span></div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-bottom:10px;">
          <div style="background:#052e16;border-radius:4px;padding:6px 3px;text-align:center;font-size:10px;font-weight:700;color:#4ade80;">Tech<br>+2.1%</div>
          <div style="background:#052e16;border-radius:4px;padding:6px 3px;text-align:center;font-size:10px;font-weight:700;color:#4ade80;">AI<br>+3.4%</div>
          <div style="background:#1c0000;border-radius:4px;padding:6px 3px;text-align:center;font-size:10px;font-weight:700;color:#f87171;">Energy<br>-1.2%</div>
          <div style="background:#052e16;border-radius:4px;padding:6px 3px;text-align:center;font-size:10px;font-weight:700;color:#4ade80;">Finance<br>+0.8%</div>
          <div style="background:#1c0000;border-radius:4px;padding:6px 3px;text-align:center;font-size:10px;font-weight:700;color:#f87171;">Utilities<br>-0.5%</div>
        </div>
        <div style="font-size:10px;color:#3a5068;margin-bottom:6px;">Top Momentum Signals</div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:8px 12px;margin-bottom:5px;display:flex;justify-content:space-between;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">NVDA</span> <span style="background:#052e16;color:#4ade80;font-size:9px;font-weight:700;padding:2px 5px;border-radius:3px;">Golden Cross</span><div style="font-size:10px;color:#3a5068;margin-top:2px;">→ Short-term trend crossed above long-term</div></div>
          <div style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#22c55e;">▲ 3.21%</div>
        </div>
        <div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:8px 12px;display:flex;justify-content:space-between;">
          <div><span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#60a5fa;font-size:13px;">AMD</span> <span style="background:#052e16;color:#4ade80;font-size:9px;font-weight:700;padding:2px 5px;border-radius:3px;">MACD Crossover</span><div style="font-size:10px;color:#3a5068;margin-top:2px;">→ Momentum just flipped positive</div></div>
          <div style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#22c55e;">▲ 1.87%</div>
        </div>
      </div>
    </div>""",
]

# ─────────────────────────────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────────────────────────────
def page_landing():
    # Minimal top nav
    nc1,_,nc2=st.columns([2,5,3])
    with nc1:
        st.markdown('<div style="padding:10px 0 0 24px;"><span class="sw-logo">Stock<span class="w">W</span>ins</span></div>',unsafe_allow_html=True)
    with nc2:
        lc1,lc2,lc3=st.columns(3)
        with lc1:
            if st.button("Features",key="land_feat"): pass
        with lc2:
            if st.button("Login",key="land_log"): nav("login")
        with lc3:
            if st.button("Start Free",key="land_su",type="primary"): nav("signup")
    st.divider()

    # Hero (left text, right rotating demo)
    hl,hr=st.columns([5,5],gap="large")
    with hl:
        panel_idx=st.session_state.get("hero_panel",0)
        labels=["Market Overview","Squeeze Scanner","Momentum Movers"]
        st.markdown(f"""<div style="padding:48px 0 32px 48px;">
            <div class="hero-eyebrow">Smart Stock Discovery Platform</div>
            <div class="hero-h1">Spot Market Opportunities<br><span class="hi">Before They Get Crowded</span></div>
            <div style="height:8px;"></div>
            <div class="hero-sub">Discover trending stocks, social buzz, short squeeze candidates, and momentum shifts in one powerful dashboard. No API key required — just sign up and go.</div>
        </div>""",unsafe_allow_html=True)
        bc1,bc2,bc3=st.columns(3)
        with bc1:
            if st.button("Start Free",key="h_su",type="primary",use_container_width=True): nav("signup")
        with bc2:
            if st.button("Try Live Dashboard",key="h_dash",use_container_width=True): nav("login")
        with bc3:
            if st.button("View Pricing",key="h_price",use_container_width=True): nav("pricing")

        st.markdown("<br>",unsafe_allow_html=True)
        # Panel switcher dots
        dc1,dc2,dc3,_=st.columns([1,1,1,3])
        for col,i,lbl in [(dc1,0,"📊"),(dc2,1,"💥"),(dc3,2,"📈")]:
            with col:
                if st.button(f"{lbl} {labels[i]}",key=f"demo_btn_{i}",
                             type="primary" if panel_idx==i else "secondary",
                             use_container_width=True):
                    st.session_state.hero_panel=i
                    st.rerun()

    with hr:
        st.markdown(f'<div style="padding:32px 48px 24px 0;">{DEMO_PANELS[st.session_state.get("hero_panel",0)]}</div>',unsafe_allow_html=True)

    # Stats bar
    st.markdown("""<div class="stats-bar">
        <div style="display:flex;align-items:center;"><span class="stats-icon">📊</span><div><div class="stats-val">5,000+</div><div class="stats-lbl">US Stocks Covered</div></div></div>
        <div style="display:flex;align-items:center;"><span class="stats-icon">🔬</span><div><div class="stats-val">10+</div><div class="stats-lbl">Smart Stock Categories</div></div></div>
        <div style="display:flex;align-items:center;"><span class="stats-icon">💰</span><div><div class="stats-val">$0</div><div class="stats-lbl">To Get Started</div></div></div>
        <div style="display:flex;align-items:center;"><span class="stats-icon">⚡</span><div><div class="stats-val">Real-Time</div><div class="stats-lbl">Sentiment Data</div></div></div>
    </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # Features
    st.markdown('<div style="padding:0 48px;"><div class="sec">Why Traders Choose StockWins</div></div>',unsafe_allow_html=True)
    feats=[
        ("📡","Live Sentiment Signals","Track what thousands of traders are saying in real time — know when the crowd turns bullish before price reacts."),
        ("💬","Plain-English Insights","Every RSI, MACD, and moving average signal explained in clear, beginner-friendly language. No finance degree needed."),
        ("💥","Short Squeeze Scanner","Identify stocks with extreme short interest that could explode when bears are forced to cover."),
        ("📊","BI-Style Dashboards","Sector heatmaps, index trackers, volume leaders, and momentum leaderboards — Bloomberg simplified."),
        ("🔊","Volume Surge Detection","Know instantly when a stock experiences unusual trading activity — often the first signal of a major move."),
        ("🎯","0–100 Scoring Engine","Every stock ranked 0–100 combining momentum, trend, MACD, volume, sentiment, and squeeze potential."),
    ]
    st.markdown('<div style="padding:0 48px;">',unsafe_allow_html=True)
    for i in range(0,len(feats),3):
        cols=st.columns(3,gap="small")
        for j,col in enumerate(cols):
            if i+j<len(feats):
                ic,t,d=feats[i+j]
                col.markdown(f'<div class="sw-card card-blue" style="height:100%;"><div style="font-size:22px;margin-bottom:8px;">{ic}</div><div style="font-size:13px;font-weight:700;color:#c9d3e0;margin-bottom:5px;">{t}</div><div style="font-size:12px;color:#3a5068;line-height:1.6;">{d}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # Category tiles
    st.markdown('<div style="padding:0 48px;"><div class="sec">Curated Stock Categories</div>',unsafe_allow_html=True)
    cat_tiles=[
        ("🔥","Trending Now","StockTwits hot list","free"),
        ("📡","Social Buzz","Meme & social stocks","free"),
        ("💥","Squeeze Radar","High short interest","premium"),
        ("📈","Momentum Movers","Trending upward","premium"),
        ("💻","Tech Stocks","FAANG & beyond","free"),
        ("🤖","AI Stocks","Artificial intelligence plays","free"),
        ("⚡","EV Stocks","Electric vehicle sector","free"),
        ("🧬","Biotech","Biotech & pharma","free"),
        ("🔄","Reversals","Oversold setups","premium"),
        ("🔊","High Volume","Volume surges","premium"),
        ("📊","S&P 500","Index components","free"),
        ("🔬","Small Cap","High-risk, high-reward","free"),
    ]
    cat_cols=st.columns(4,gap="small")
    for i,col in enumerate(cat_cols*3):
        if i<len(cat_tiles):
            ic,t,sub,plan=cat_tiles[i]
            lock='<span style="float:right;background:#1c1000;color:#f59e0b;font-size:9px;font-weight:700;padding:1px 6px;border-radius:3px;">PRO</span>' if plan=="premium" else ""
            col.markdown(f'<div class="sw-card" style="padding:12px 14px;">{lock}<div style="font-size:18px;margin-bottom:4px;">{ic}</div><div style="font-size:12px;font-weight:700;color:#c9d3e0;">{t}</div><div style="font-size:11px;color:#2a3a50;">{sub}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # Plain-English section
    st.markdown('<div style="padding:0 48px;"><div class="sec">Plain-English Signal Translations — Examples</div>',unsafe_allow_html=True)
    examples=[
        ("RSI Oversold","bull","Stock may have fallen too far too fast — historically this can precede a bounce upward as buyers step in."),
        ("RSI Overbought","bear","Stock has risen quickly — be cautious, rapid rises can face short-term profit-taking."),
        ("Golden Cross ✨","bull","Short-term trend just crossed above long-term — many traders treat this as a serious buy signal."),
        ("Volume Spike 🔊","bull","More traders than usual are active — when a move happens on high volume it tends to be more reliable."),
        ("High Short Interest","bull","Many traders are betting the stock falls — if it rises instead, forced buying can accelerate the move dramatically."),
        ("Death Cross 💀","bear","Short-term trend crossed below long-term — often signals a downtrend is gaining strength."),
    ]
    for i in range(0,len(examples),3):
        cols=st.columns(3,gap="small")
        for j,col in enumerate(cols):
            if i+j<len(examples):
                l,s,t=examples[i+j]
                bc="b-bull" if s=="bull" else "b-bear"
                bl="Bullish Signal" if s=="bull" else "Bearish Signal"
                col.markdown(f'<div class="sw-card"><span class="b {bc}">{bl}</span><div style="font-size:13px;font-weight:700;color:#c9d3e0;margin:7px 0 4px;">{l}</div><div style="font-size:12px;color:#3a5068;font-style:italic;line-height:1.5;">"{t}"</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # How it works
    st.markdown('<div style="padding:0 48px;"><div class="sec">How It Works</div>',unsafe_allow_html=True)
    for col,(n,t,d) in zip(st.columns(3,gap="small"),[
        ("01","Discover Opportunities","Browse 10+ curated stock categories filtered by theme, momentum, social buzz, and technical setup."),
        ("02","Understand Why They Matter","Every stock comes with plain-English explanations — why it's here, what's improving, what the risk is."),
        ("03","Track and Act With Confidence","Add stocks to your watchlist, set alerts, and use the advanced screener to find exactly what you're looking for."),
    ]):
        col.markdown(f'<div class="sw-card card-blue" style="text-align:center;padding:24px 16px;"><div style="font-family:\'JetBrains Mono\',monospace;font-size:24px;font-weight:700;color:#1e3a8a;margin-bottom:8px;">{n}</div><div style="font-size:14px;font-weight:700;color:#c9d3e0;margin-bottom:6px;">{t}</div><div style="font-size:12px;color:#3a5068;line-height:1.6;">{d}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div style="padding:0 48px;"><div class="sec">What Traders Are Saying</div>',unsafe_allow_html=True)
    for col,(stars,txt,name) in zip(st.columns(3,gap="small"),[
        ("⭐⭐⭐⭐⭐","The plain-English explanations changed how I analyze stocks. I finally understand what these indicators mean for my trades.","Michael T., Active Trader"),
        ("⭐⭐⭐⭐⭐","The squeeze scanner flagged several huge movers early. No more API keys to set up — just sign in and it works.","Sarah K., Day Trader"),
        ("⭐⭐⭐⭐⭐","Combining social sentiment with technical signals in one clean dashboard is incredibly powerful.","David R., Swing Trader"),
    ]):
        col.markdown(f'<div class="sw-card"><div style="margin-bottom:6px;">{stars}</div><div style="font-size:12px;color:#3a5068;line-height:1.6;margin-bottom:10px;">"{txt}"</div><div style="font-size:11px;font-weight:600;color:#2563eb;">— {name}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br><br>",unsafe_allow_html=True)

    # Premium CTA
    st.markdown("""<div style="background:radial-gradient(ellipse at 70% 50%,#061430,#060a12);border-top:1px solid #111c2e;border-bottom:1px solid #111c2e;padding:56px 48px;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;">
            <div>
                <div style="font-size:10px;font-weight:700;color:#f59e0b;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">Premium Features</div>
                <div style="font-size:36px;font-weight:900;color:#f1f5f9;letter-spacing:-1px;margin-bottom:12px;">Upgrade for Deeper Insights &amp; Pro Features</div>
                <div style="font-size:14px;color:#3a5068;margin-bottom:20px;line-height:1.7;">Unlock the full power of StockWins to boost your trading strategy. From squeeze scanner to advanced multi-factor screener.</div>
            </div>
            <div style="background:#0d1525;border:1px solid #1a2840;border-radius:10px;overflow:hidden;">
                <div style="background:#06163a;padding:10px 16px;border-bottom:1px solid #111c2e;font-size:11px;font-weight:700;color:#60a5fa;text-align:center;letter-spacing:1px;">GET DAILY BEST SETUPS</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;">
                    <div style="padding:18px 16px;border-right:1px solid #111c2e;">
                        <div style="font-size:14px;font-weight:700;color:#c9d3e0;margin-bottom:10px;">Free</div>
                        <div style="font-size:12px;color:#3a5068;line-height:2.1;">✅ Seeding insights<br>✅ Basic watchlists<br>✅ 5 stock categories<br>✅ Basic signals<br>❌ Squeeze scanner<br>❌ Advanced screener<br>❌ Full BI analytics<br>❌ Priority signals</div>
                    </div>
                    <div style="padding:18px 16px;background:linear-gradient(160deg,#060f2e,#0d1525);">
                        <div style="font-size:14px;font-weight:700;color:#f59e0b;margin-bottom:10px;">Premium ⭐</div>
                        <div style="font-size:12px;color:#3a5068;line-height:2.1;">✅ Unlimited insights<br>✅ Unlimited watchlists<br>✅ 13+ categories<br>✅ All signals<br>✅ Squeeze scanner<br>✅ Advanced screener<br>✅ Full BI analytics<br>✅ Priority signals</div>
                    </div>
                </div>
            </div>
        </div>
    </div>""",unsafe_allow_html=True)
    cc1,cc2,_=st.columns([1,1,3])
    with cc1:
        if st.button("Get Started Free",key="prem_free",use_container_width=True): nav("signup")
    with cc2:
        if st.button("Go Premium →",key="prem_go",type="primary",use_container_width=True): nav("pricing")

    st.markdown("<br><br>",unsafe_allow_html=True)

    # FAQ
    st.markdown('<div style="padding:0 48px;"><div class="sec">Frequently Asked Questions</div>',unsafe_allow_html=True)
    for q,a in [
        ("Is this financial advice?","No. StockWins is an educational data analysis tool. All signals and scores are algorithmic outputs for informational purposes only. Always consult a licensed financial advisor before making investment decisions."),
        ("Do I need to enter an API key?","No. Regular users never need to enter any API key. All market data is fetched automatically from free data providers. The platform just works — sign up and start exploring."),
        ("What markets are covered?","We cover US equity markets including NASDAQ, NYSE, S&P 500, Russell 1000, and high-volume small caps. Data includes real-time prices, volume, fundamentals, and social sentiment."),
        ("How are stocks ranked and scored?","Each stock receives a 0–100 StockWins Score combining: RSI momentum (0–25), price trend vs moving averages (0–20), MACD signal (0–15), volume activity (0–15), social sentiment (0–15), and short squeeze potential (0–10)."),
        ("What is included in Premium?","Premium unlocks all 13+ stock categories, the short squeeze scanner, advanced multi-factor screener, full BI analytics dashboard, score breakdowns, watchlist analytics, and unlimited saved screeners."),
        ("Can I cancel anytime?","Yes. Premium is month-to-month. Cancel at any time and keep access through the end of your billing period."),
    ]:
        with st.expander(q):
            st.markdown(f'<div style="font-size:13px;color:#3a5068;line-height:1.7;">{a}</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # Footer
    st.markdown("""<div style="background:#060a12;border-top:1px solid #111c2e;padding:32px 48px;margin-top:32px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:12px;">
            <div class="sw-logo">Stock<span class="w">W</span>ins</div>
            <div style="font-size:12px;color:#1e2d42;display:flex;gap:20px;">
                <span>Privacy Policy</span><span>Terms of Service</span><span>Risk Disclaimer</span><span>Contact</span>
            </div>
        </div>
        <div class="disc">⚠️ <strong>Risk Disclaimer:</strong> Trading stocks and securities involves substantial risk of financial loss. StockWins provides algorithmic, data-driven educational content only. Nothing on this platform constitutes financial, investment, legal, or tax advice. All signals are generated by automated algorithms and may be inaccurate. Past performance does not guarantee future results. Always consult a licensed financial professional before making any investment decision. We are not responsible for any trading losses.</div>
        <div style="font-size:10px;color:#111c2e;margin-top:10px;text-align:right;">© 2026 StockWins. All rights reserved.</div>
    </div>""",unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: LOGIN / SIGNUP / AUTH
# ─────────────────────────────────────────────────────────────────────
def page_login():
    render_topbar()
    _,cc,_=st.columns([1,2,1])
    with cc:
        st.markdown('<div style="text-align:center;padding:32px 0 20px;"><div style="font-size:24px;font-weight:800;color:#e2e8f0;">Welcome Back 👋</div><div style="font-size:13px;color:#3a5068;margin-top:6px;">Sign in to your StockWins account</div></div>',unsafe_allow_html=True)
        with st.form("lf"):
            email=st.text_input("Email",placeholder="you@example.com")
            pw=st.text_input("Password",type="password",placeholder="••••••••")
            sub=st.form_submit_button("Sign In →",type="primary",use_container_width=True)
            if sub:
                if login(email,pw): nav("dashboard")
                else: st.error("Invalid email or password.")
        st.markdown("""<div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:12px 14px;margin-top:10px;font-size:12px;color:#3a5068;">
            <span style="color:#2563eb;font-weight:600;">Demo accounts (no sign-up needed):</span><br>
            Free: demo@stockwins.com / demo123<br>
            Premium: premium@stockwins.com / premium1<br>
            Admin: admin@stockwins.com / admin123</div>""",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("No account? Sign up free →",use_container_width=True): nav("signup")
        if st.button("Forgot password?",use_container_width=True): nav("forgot_pw")
        if st.button("← Back to Home",use_container_width=True): nav("landing")

def page_signup():
    render_topbar()
    _,cc,_=st.columns([1,2,1])
    with cc:
        st.markdown('<div style="text-align:center;padding:32px 0 20px;"><div style="font-size:24px;font-weight:800;color:#e2e8f0;">Create Your Account 🚀</div><div style="font-size:13px;color:#3a5068;margin-top:6px;">Free forever. No credit card. No API keys. Just sign up and go.</div></div>',unsafe_allow_html=True)
        with st.form("sf"):
            name=st.text_input("Full name",placeholder="Jane Doe")
            email=st.text_input("Email",placeholder="you@example.com")
            pw=st.text_input("Password",type="password",placeholder="Min 6 characters")
            pw2=st.text_input("Confirm password",type="password")
            agree=st.checkbox("I agree to the Terms of Service and understand this is not financial advice.")
            sub=st.form_submit_button("Create Free Account →",type="primary",use_container_width=True)
            if sub:
                if not all([name,email,pw,pw2]): st.error("Fill in all fields.")
                elif pw!=pw2: st.error("Passwords don't match.")
                elif len(pw)<6: st.error("Password must be 6+ characters.")
                elif not agree: st.error("Please agree to the Terms of Service.")
                else:
                    ok,msg=signup(email,pw,name)
                    if ok:
                        st.success(f"Welcome, {name}! Account created.")
                        time.sleep(0.5); nav("verify_email")
                    else: st.error(msg)
        if st.button("Already have an account? Sign In",use_container_width=True): nav("login")

def page_verify():
    render_topbar()
    _,cc,_=st.columns([1,2,1])
    with cc:
        st.markdown("""<div class="sw-card" style="text-align:center;padding:40px 28px;">
            <div style="font-size:40px;margin-bottom:14px;">📧</div>
            <div style="font-size:20px;font-weight:800;color:#e2e8f0;margin-bottom:8px;">Verify Your Email</div>
            <div style="font-size:13px;color:#3a5068;line-height:1.7;margin-bottom:20px;">
            We sent a verification link to your email address.<br>Click the link to complete your account setup.<br>
            <span style="font-size:11px;color:#1e2d42;">(Simulated in demo — click Continue below)</span>
            </div>
        </div>""",unsafe_allow_html=True)
        if st.button("✅ Email Verified — Continue to Dashboard",type="primary",use_container_width=True):
            email=st.session_state.user["email"] if is_authed() else ""
            if email in st.session_state.users_db:
                st.session_state.users_db[email]["verified"]=True
            nav("dashboard")
        if st.button("Resend verification email",use_container_width=True):
            st.info("Verification email resent! (simulated)")
        if st.button("Skip for now",use_container_width=True): nav("dashboard")

def page_forgot_pw():
    render_topbar()
    _,cc,_=st.columns([1,2,1])
    with cc:
        st.markdown('<div style="text-align:center;padding:28px 0 16px;"><div style="font-size:22px;font-weight:800;color:#e2e8f0;">Reset Password 🔑</div><div style="font-size:13px;color:#3a5068;margin-top:6px;">Enter your email to receive a reset link.</div></div>',unsafe_allow_html=True)
        with st.form("fpf"):
            email=st.text_input("Email",placeholder="you@example.com")
            sub=st.form_submit_button("Send Reset Link →",type="primary",use_container_width=True)
            if sub:
                if email in st.session_state.users_db:
                    st.success("✅ Reset link sent to your email. (Simulated in demo)")
                    time.sleep(1); nav("login")
                else: st.error("No account found with that email address.")
        if st.button("← Back to Login",use_container_width=True): nav("login")


# ─────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────
def page_dashboard():
    render_topbar("dashboard")
    st.markdown('<div class="pg">',unsafe_allow_html=True)

    # Verification banner
    db_user=get_db_user()
    if not db_user.get("verified",True):
        st.markdown('<div style="background:#06163a;border:1px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin-bottom:14px;font-size:13px;color:#60a5fa;">📧 Please verify your email to unlock all features. <a style="color:#93c5fd;cursor:pointer;">Resend →</a></div>',unsafe_allow_html=True)

    # ── Market Overview ────────────────────────────────────────────
    st.markdown('<div class="sec">📊 Market Overview <span class="cnt">Live</span></div>',unsafe_allow_html=True)
    with st.spinner("Loading market data..."):
        idx=get_indexes(); secs=get_sectors()

    # Index cards
    idx_cols=st.columns(len(idx))
    for col,(name,d) in zip(idx_cols,idx.items()):
        c="g" if d["pct"]>=0 else "r"
        ar="▲" if d["pct"]>=0 else "▼"
        # Mini trend bars
        trend=d.get("trend",[])
        bars=""
        if trend:
            mn,mx=min(trend),max(trend)
            rng=mx-mn if mx!=mn else 1
            bars=''.join([f'<div style="height:{int(12*(v-mn)/rng+4)}px;width:5px;background:{"#22c55e" if d["pct"]>=0 else "#ef4444"};border-radius:2px;display:inline-block;margin-right:1px;vertical-align:bottom;"></div>' for v in trend])
        col.markdown(f"""<div class="idx">
            <div class="idx-name">{name}</div>
            <div class="idx-price">{d['price']:,.2f}</div>
            <div class="idx-chg {c}">{ar} {abs(d['pct']):.2f}%</div>
            <div style="margin-top:8px;height:18px;display:flex;align-items:flex-end;">{bars}</div>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # ── Two-column: Sector Heatmap + Market Sentiment ────────────
    scol,mcol=st.columns([3,2],gap="small")
    with scol:
        st.markdown('<div class="sec" style="font-size:13px;">Sector Performance</div>',unsafe_allow_html=True)
        sec_cols=st.columns(5)
        for i,(sec,chg) in enumerate(secs.items()):
            with sec_cols[i%5]:
                cls="hm-hi" if chg>0.2 else "hm-lo" if chg<-0.2 else "hm-neu"
                ar="▲" if chg>=0 else "▼"
                st.markdown(f'<div class="hm {cls}" style="margin-bottom:4px;"><div style="font-size:9px;margin-bottom:2px;">{sec}</div>{ar}{abs(chg):.1f}%</div>',unsafe_allow_html=True)

    with mcol:
        st.markdown('<div class="sec" style="font-size:13px;">Market Sentiment</div>',unsafe_allow_html=True)
        with st.spinner("Loading..."):
            hot=st_hot()
        movers=get_bi_movers()
        gainers=[m for m in movers if m["pct"]>0]
        losers=[m for m in movers if m["pct"]<0]
        avg_pct=sum(m["pct"] for m in movers)/len(movers) if movers else 0
        sent_lbl="Risk-On 🟢" if avg_pct>0.3 else "Risk-Off 🔴" if avg_pct<-0.3 else "Neutral ⚪"
        sent_c="#22c55e" if avg_pct>0 else "#ef4444"
        st.markdown(f"""<div class="sw-card" style="padding:12px 14px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
                <span style="font-size:13px;font-weight:700;color:{sent_c};">{sent_lbl}</span>
                <span style="font-size:12px;color:#2a3a50;">Avg {avg_pct:+.2f}%</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;color:#3a5068;margin-bottom:8px;">
                <span>🟢 {len(gainers)} advancing</span>
                <span>🔴 {len(losers)} declining</span>
            </div>
            <div style="font-size:11px;color:#2a3a50;margin-bottom:4px;">🔥 StockTwits Trending:</div>
            <div style="line-height:2;">{" ".join([f'<span style="background:#1c0800;color:#f97316;font-size:10px;font-weight:700;padding:2px 7px;border-radius:3px;margin-right:3px;">{t}</span>' for t in hot[:6]])}</div>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # ── Two-column: StockTwits Hot | Squeeze Preview ─────────────
    left,right=st.columns(2,gap="small")

    with left:
        st.markdown('<div class="sec">📡 StockTwits Hot Stocks <span class="cnt">Free</span></div>',unsafe_allow_html=True)
        if hot:
            prog=st.progress(0,"Loading hot stocks...")
            for i,t in enumerate(hot[:6]):
                prog.progress((i+1)/6,f"Loading {t}...")
                q=get_quote(t)
                if q:
                    s=st_sentiment(t)
                    bull_c="#22c55e" if s["bull"]>=60 else "#ef4444" if s["bull"]<40 else "#94a3b8"
                    pct_c="g" if q["pct"]>=0 else "r"
                    ar="▲" if q["pct"]>=0 else "▼"
                    st.markdown(f"""<div class="sr">
                        <div style="flex:2.5;">
                            <span class="sr-tick">{t}</span><span class="b b-hot" style="margin-left:6px;">🔥</span>
                            <div class="sr-name">{q.get('name','')[:24]}</div>
                            <div class="sr-why">→ {s['bull']}% bullish on StockTwits · {s.get('wl',0):,} watching</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="sr-price">${q['price']:,.2f}</div>
                            <div class="idx-chg {pct_c}">{ar}{abs(q['pct']):.2f}%</div>
                        </div>
                    </div>""",unsafe_allow_html=True)
            prog.empty()

    with right:
        if is_premium():
            st.markdown('<div class="sec">💥 Short Squeeze Candidates <span class="cnt">Premium</span></div>',unsafe_allow_html=True)
            squeeze_preview_tickers=["GME","AMC","MULN","BBIG","FFIE"]
            prog=st.progress(0,"Loading squeeze candidates...")
            found=0
            for i,t in enumerate(squeeze_preview_tickers):
                prog.progress((i+1)/len(squeeze_preview_tickers),f"Checking {t}...")
                info=yf_fundamentals(t)
                sf=(info.get("sf",0) or 0)*100
                if sf>=10:
                    q=get_quote(t)
                    if q:
                        found+=1
                        pct_c="g" if q["pct"]>=0 else "r"
                        ar="▲" if q["pct"]>=0 else "▼"
                        st.markdown(f"""<div class="sr">
                            <div style="flex:2.5;">
                                <span class="sr-tick">{t}</span>
                                <div class="sr-name">{q.get('name','')[:24]}</div>
                                <div class="sr-why">→ Short float: <span style="color:#ef4444;font-weight:700;">{sf:.1f}%</span> · Days-to-cover: {info.get('dtc',0) or 0:.1f}</div>
                            </div>
                            <div style="text-align:right;">
                                <div class="sr-price">${q['price']:,.2f}</div>
                                <div class="idx-chg {pct_c}">{ar}{abs(q['pct']):.2f}%</div>
                            </div>
                        </div>""",unsafe_allow_html=True)
            prog.empty()
            if found==0:
                st.info("No squeeze candidates meeting threshold right now.")
        else:
            st.markdown('<div class="sec">💥 Short Squeeze Candidates <span class="cnt">Premium</span></div>',unsafe_allow_html=True)
            render_lock("Short Squeeze Scanner")

    st.markdown("<br>",unsafe_allow_html=True)

    # ── Category Explorer ─────────────────────────────────────────
    st.markdown('<div class="sec">📈 Explore Stock Categories</div>',unsafe_allow_html=True)
    avail=FREE_CATS if not is_premium() else list(CATEGORIES.keys())
    sel=st.selectbox("Select category",avail,key="dash_cat_sel",label_visibility="collapsed")
    if sel in PREMIUM_CATS and not is_premium():
        render_lock(sel)
    else:
        render_category_page(sel)

    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# CATEGORY RENDER — shared helper
# ─────────────────────────────────────────────────────────────────────
def render_category_page(cat, limit=12):
    tickers=list(CATEGORIES.get(cat,[]))
    hot=st_hot()

    if cat=="🔥 Trending Now":         tickers=hot
    elif cat=="💥 Squeeze Radar":      page_squeeze_scan(); return
    elif cat in PREMIUM_CATS:
        base=list(set(CATEGORIES["💻 Tech"]+CATEGORIES["🤖 AI"]+CATEGORIES["⚡ EV"]+CATEGORIES["📊 S&P 500"]+hot[:8]))
        tickers=base[:28]

    if not tickers: st.info("No tickers for this category."); return
    scan=min(len(tickers),limit)
    st.caption(f"Analyzing top {scan} stocks · Data via Yahoo Finance & StockTwits")

    scored=[]; prog=st.progress(0,f"Analyzing {cat}...")
    for i,ticker in enumerate(tickers[:scan]):
        prog.progress((i+1)/scan,f"Analyzing {ticker}...")
        q=get_quote(ticker); df=get_ohlcv(ticker,60)
        info=yf_fundamentals(ticker); sent=st_sentiment(ticker)
        sc,bd,op,risk,conf=compute_scores(df,info,sent)
        ig=get_insights(df,info)
        if q: scored.append({"t":ticker,"q":q,"sc":sc,"bd":bd,"ig":ig,"op":op,"risk":risk,"conf":conf,"hot":ticker in hot,"df":df,"info":info,"sent":sent})
    prog.empty()

    # Dynamic filters
    if cat=="📈 Momentum Movers":    scored=[s for s in scored if s["sc"]>=55]
    elif cat=="🔄 Reversal Candidates":
        def is_rev(s):
            if s["df"] is None or len(s["df"])<14: return False
            try: r=ta.momentum.RSIIndicator(s["df"]["close"].copy(),14).rsi().iloc[-1]; return pd.notna(r) and r<35
            except: return False
        scored=[s for s in scored if is_rev(s)]
    elif cat=="🔊 High Volume":
        def vr(s):
            if s["df"] is None or len(s["df"])<20: return 0
            avg=s["df"]["volume"].rolling(20).mean().iloc[-1]; return s["df"]["volume"].iloc[-1]/avg if avg>0 else 0
        scored=sorted(scored,key=vr,reverse=True)

    scored.sort(key=lambda x:x["sc"],reverse=True)
    scored=scored[:10]

    if not scored: st.info(f"No stocks currently meeting the criteria for {cat}."); return

    for s in scored:
        col_a,col_b=st.columns([5,2],gap="small")
        with col_a:
            render_stock_row(s["t"],s["q"],s["sc"],s["ig"],s["info"],s["sent"],s["hot"],s["op"],s["risk"])
        with col_b:
            bc1,bc2=st.columns(2,gap="small")
            with bc1:
                if st.button("📊",key=f"d_{s['t']}_{cat}",use_container_width=True,help="View details"):
                    st.session_state.detail_ticker=s["t"]
                    st.session_state.detail_data=s
                    nav("stock_detail")
            with bc2:
                wl=st.session_state.watchlist
                in_wl=s["t"] in wl
                if st.button("✅" if in_wl else "➕",key=f"w_{s['t']}_{cat}",use_container_width=True,help="Toggle watchlist"):
                    if in_wl: wl.remove(s["t"])
                    else:     wl.append(s["t"])
                    st.rerun()


# ─────────────────────────────────────────────────────────────────────
# PAGE: SQUEEZE SCAN
# ─────────────────────────────────────────────────────────────────────
def page_squeeze_scan():
    st.markdown('<div class="sec">💥 Short Squeeze Radar <span class="cnt">Premium</span></div>',unsafe_allow_html=True)
    st.markdown("""<div class="ins ins-bull" style="margin-bottom:12px;">
        <div class="ins-label" style="font-weight:700;color:#c9d3e0;margin-bottom:4px;">How Short Squeezes Work</div>
        <div style="font-size:12px;color:#3a5068;">When many traders are betting a stock will fall (short selling) and the stock rises instead, they're forced to buy shares to cut losses. This forced buying accelerates the move dramatically — that's a short squeeze. High short float + high days-to-cover = most fuel for a squeeze.</div>
    </div>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: min_sf=st.slider("Min Short Float %",5,40,15)
    with c2: min_dtc=st.slider("Min Days to Cover",1,10,3)
    universe=list(set(CATEGORIES["🎭 Meme / Social"]+CATEGORIES["🔬 Small Cap"]+CATEGORIES["⚡ EV"]+CATEGORIES["🧬 Biotech"]+st_hot()))[:35]
    if st.button("🔍 Scan for Squeeze Candidates",type="primary"):
        results=[]; prog=st.progress(0,"Scanning universe...")
        for i,t in enumerate(universe):
            prog.progress((i+1)/len(universe),f"Checking {t}...")
            try:
                info=yf_fundamentals(t); sf=(info.get("sf",0) or 0)*100; dtc=info.get("dtc",0) or 0
                if sf>=min_sf and dtc>=min_dtc:
                    q=get_quote(t); df=get_ohlcv(t,60); sent=st_sentiment(t)
                    sc,_,op,risk,_=compute_scores(df,info,sent)
                    mc=info.get("mktcap",0)
                    results.append({"Ticker":t,"Price":f"${q['price']:,.2f}" if q else "N/A",
                                    "Short Float":f"{sf:.1f}%","Days-to-Cover":f"{dtc:.1f}",
                                    "Mkt Cap":f"${mc/1e9:.2f}B" if mc else "N/A",
                                    "SW Score":sc,"Opportunity":op,"Risk":risk,
                                    "Bull Sent":f"{sent.get('bull',50)}%",
                                    "_sc":sc,"_sf":sf,"_t":t})
            except: continue
        prog.empty()
        if not results: st.info(f"No stocks found above {min_sf}% short float with {min_dtc}+ days to cover."); return
        results=sorted(results,key=lambda x:x["_sc"],reverse=True)
        st.success(f"🔥 Found {len(results)} potential squeeze candidates!")
        st.dataframe(pd.DataFrame([{k:v for k,v in r.items() if not k.startswith("_")} for r in results]),use_container_width=True,hide_index=True)
        st.markdown('<div style="font-size:13px;font-weight:700;color:#c9d3e0;margin:16px 0 10px;">Top 3 Detailed</div>',unsafe_allow_html=True)
        cols=st.columns(3,gap="small")
        for col,r in zip(cols,results[:3]):
            sc_c="#22c55e" if r["_sc"]>=65 else "#fbbf24" if r["_sc"]>=40 else "#ef4444"
            col.markdown(f"""<div class="sw-card card-blue">
                <span class="sr-tick">{r['_t']}</span>
                <div style="margin:12px 0 5px;"><div style="font-size:9px;color:#2a3a50;text-transform:uppercase;letter-spacing:.5px;">Short Float</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:#ef4444;">{r['Short Float']}</div></div>
                <div style="margin:5px 0;"><div style="font-size:9px;color:#2a3a50;text-transform:uppercase;letter-spacing:.5px;">Days to Cover</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:#fbbf24;">{r['Days-to-Cover']}</div></div>
                <div style="margin:5px 0;"><div style="font-size:9px;color:#2a3a50;text-transform:uppercase;letter-spacing:.5px;">SW Score</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:{sc_c};">{r['_sc']}/100</div></div>
                <div style="font-size:11px;color:#2a3a50;margin-top:8px;">{r['Opportunity']} · Risk: {r['Risk']}</div>
            </div>""",unsafe_allow_html=True)
    st.markdown('<div class="disc">⚠️ Short interest data via Yahoo Finance may be delayed. High short interest does not guarantee a squeeze. Educational analysis only.</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: STOCK DETAIL
# ─────────────────────────────────────────────────────────────────────
def page_detail():
    render_topbar()
    ticker=st.session_state.get("detail_ticker")
    data=st.session_state.get("detail_data",{})

    if st.button("← Back",key="back_det"): nav(st.session_state.get("prev_page","dashboard"))
    if not ticker: st.warning("No stock selected."); return

    q=data.get("q") or get_quote(ticker)
    df=data.get("df") or get_ohlcv(ticker,90)
    info=data.get("info") or yf_fundamentals(ticker)
    sent=data.get("sent") or st_sentiment(ticker)
    sc,bd,op,risk,conf=compute_scores(df,info,sent)
    ig=get_insights(df,info)
    hot=ticker in st_hot()

    if not q: st.error(f"Could not load data for {ticker}."); return

    pct=q.get("pct",0); price=q.get("price",0)
    cc="#22c55e" if pct>=0 else "#ef4444"
    ar="▲" if pct>=0 else "▼"
    rc=risk_color(risk)

    st.markdown('<div class="pg">',unsafe_allow_html=True)

    # Header
    h1,h2,h3=st.columns([3,2,2],gap="small")
    with h1:
        hot_b='<span class="b b-hot" style="margin-right:6px;">🔥 HOT</span>' if hot else ""
        st.markdown(f"""<div>
            {hot_b}<span style="font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:700;color:#60a5fa;">{ticker}</span>
            <div style="font-size:14px;color:#4a6080;margin-top:3px;">{q.get('name','')}</div>
            <div style="font-size:12px;color:#2a3a50;margin-top:2px;">{info.get('sector','N/A')} · {info.get('industry','N/A')}</div>
            <div style="margin-top:6px;display:flex;gap:6px;">
                <span class="b b-new">{op}</span>
                <span style="font-size:11px;font-weight:700;color:{rc};">⚡ {risk} Risk</span>
                <span style="font-size:11px;color:#2a3a50;">{conf} confidence</span>
            </div>
        </div>""",unsafe_allow_html=True)
    with h2:
        st.markdown(f"""<div style="text-align:right;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:700;color:#e2e8f0;">${price:,.2f}</div>
            <div style="font-size:16px;font-weight:700;color:{cc};">{ar} {abs(pct):.2f}% today</div>
            <div style="font-size:11px;color:#2a3a50;">Prev. ${q.get('prev',0):,.2f}</div>
        </div>""",unsafe_allow_html=True)
    with h3:
        sc_c="#22c55e" if sc>=65 else "#fbbf24" if sc>=40 else "#ef4444"
        sc_bg="#052e16" if sc>=65 else "#1c1000" if sc>=40 else "#1c0000"
        st.markdown(f"""<div style="background:{sc_bg};border:1px solid {sc_c};border-radius:10px;padding:14px;text-align:center;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:36px;font-weight:700;color:{sc_c};">{sc}</div>
            <div style="font-size:10px;color:{sc_c};text-transform:uppercase;letter-spacing:1px;margin-top:2px;">StockWins Score</div>
            <div style="font-size:11px;color:#2a3a50;margin-top:4px;">{op}</div>
        </div>""",unsafe_allow_html=True)

    st.divider()

    # Stats
    mc=info.get("mktcap",0)
    mc_s=f"${mc/1e12:.2f}T" if mc>=1e12 else f"${mc/1e9:.2f}B" if mc>=1e9 else f"${mc/1e6:.0f}M" if mc else "N/A"
    sf=(info.get("sf",0) or 0)*100
    items=[("Open",f"${q.get('open',0):,.2f}"),("Day High",f"${q.get('high',0):,.2f}"),
           ("Day Low",f"${q.get('low',0):,.2f}"),("Volume",f"{q.get('volume',0)/1e6:.2f}M"),
           ("Mkt Cap",mc_s),("52W High",f"${info.get('hi52',0):,.2f}"),
           ("52W Low",f"${info.get('lo52',0):,.2f}"),("Beta",f"{info.get('beta','N/A')}"),
           ("P/E",f"{info.get('pe','N/A')}"),("Short Float",f"{sf:.1f}%")]
    scols=st.columns(5)
    for i,(l,v) in enumerate(items):
        with scols[i%5]:
            st.markdown(f'<div class="stat" style="margin-bottom:8px;"><div class="stat-l">{l}</div><div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;font-weight:700;color:#e2e8f0;">{v}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    cc_col,ci_col=st.columns([3,2],gap="small")
    with cc_col:
        st.markdown('<div class="sec" style="font-size:13px;">📈 Price Chart</div>',unsafe_allow_html=True)
        if df is not None and len(df)>1:
            cdf=df[["datetime","close"]].copy().rename(columns={"datetime":"Date","close":"Price"}).set_index("Date")
            st.line_chart(cdf,color="#2563eb")
        else:
            st.info("Chart data unavailable.")

        # Score breakdown
        if bd:
            st.markdown('<div class="sec" style="font-size:13px;">Score Breakdown</div>',unsafe_allow_html=True)
            if is_premium():
                for comp,pts in bd.items():
                    c_="#22c55e" if pts>=12 else "#fbbf24" if pts>=6 else "#ef4444"
                    st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <div style="width:80px;font-size:11px;color:#3a5068;">{comp}</div>
                        <div style="flex:1;background:#111c2e;border-radius:3px;height:5px;"><div style="background:{c_};width:{pts}%;height:5px;border-radius:3px;"></div></div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{c_};width:24px;text-align:right;">{pts}</div>
                    </div>""",unsafe_allow_html=True)
            else:
                st.markdown('<div style="background:#0a1020;border:1px solid #854d0e;border-radius:6px;padding:10px;font-size:12px;color:#f59e0b;">🔒 Score breakdown is Premium only.</div>',unsafe_allow_html=True)

    with ci_col:
        st.markdown('<div class="sec" style="font-size:13px;">💡 Plain-English Insights</div>',unsafe_allow_html=True)
        for lbl,txt,s,conf in ig[:6]:
            render_ins(lbl,txt,s,conf)
        if not ig:
            st.info("No indicators available — check back shortly.")

        # Sentiment
        st.markdown('<div class="sec" style="font-size:13px;margin-top:12px;">📡 Social Sentiment</div>',unsafe_allow_html=True)
        bull=sent.get("bull",50)
        st.markdown(f"""<div class="sw-card" style="padding:12px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:7px;">
                <span style="font-size:12px;font-weight:700;color:#22c55e;">🟢 Bullish {bull}%</span>
                <span style="font-size:12px;font-weight:700;color:#ef4444;">🔴 Bearish {100-bull}%</span>
            </div>
            <div style="background:#111c2e;border-radius:5px;height:8px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,#22c55e,#16a34a);width:{bull}%;height:8px;"></div>
            </div>
            <div style="font-size:11px;color:#2a3a50;margin-top:7px;">👥 {sent.get('wl',0):,} watching · {sent.get('msgs',0)} recent posts</div>
        </div>""",unsafe_allow_html=True)

    # Why flagged
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="sec" style="font-size:13px;">🎯 Why This Stock Is On Your Radar</div>',unsafe_allow_html=True)
    reasons=[]
    if sc>=70: reasons.append(("Strong multi-factor signal — RSI, trend, MACD, and volume all align","bull"))
    if sent.get("bull",50)>=65: reasons.append((f"{sent['bull']}% of StockTwits traders are currently bullish on this stock","bull"))
    if sf>=20: reasons.append((f"{sf:.0f}% of shares are sold short — if price rises, forced buying can accelerate the move dramatically","bull"))
    if hot: reasons.append(("Currently trending on StockTwits — elevated social interest today","bull"))
    for lbl,_,s,_ in ig[:4]: reasons.append((lbl,s))
    rc2=st.columns(2)
    for i,(r,s) in enumerate(reasons[:6]):
        em="🟢" if s=="bull" else "🔴" if s=="bear" else "⚪"
        with rc2[i%2]:
            st.markdown(f'<div style="background:#0a1020;border:1px solid #111c2e;border-radius:6px;padding:9px 13px;margin-bottom:5px;font-size:12px;color:#3a5068;">{em} {r}</div>',unsafe_allow_html=True)

    # Related stocks
    sector=info.get("sector","N/A")
    if sector!="N/A":
        st.markdown(f'<div class="sec" style="font-size:13px;margin-top:12px;">🔗 Related — {sector}</div>',unsafe_allow_html=True)
        all_t=list(set([t for tl in CATEGORIES.values() for t in tl]))
        related=[rt for rt in all_t if rt!=ticker and yf_fundamentals(rt).get("sector")==sector][:5]
        if related:
            rcols=st.columns(len(related))
            for col,rt in zip(rcols,related):
                rq=get_quote(rt)
                if rq:
                    rc_="#22c55e" if rq["pct"]>=0 else "#ef4444"
                    col.markdown(f'<div class="stat" style="cursor:pointer;"><div style="font-family:\'JetBrains Mono\',monospace;font-size:12px;font-weight:700;color:#60a5fa;">{rt}</div><div style="font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:700;color:#e2e8f0;">${rq["price"]:,.2f}</div><div style="font-size:11px;font-weight:700;color:{rc_};">{"▲" if rq["pct"]>=0 else "▼"}{abs(rq["pct"]):.2f}%</div></div>',unsafe_allow_html=True)
                    if col.button("View",key=f"rel_{rt}",use_container_width=True):
                        st.session_state.detail_ticker=rt; st.session_state.detail_data={}; st.rerun()

    if info.get("desc"):
        with st.expander(f"About {q.get('name',ticker)}"):
            st.markdown(f'<div style="font-size:13px;color:#3a5068;line-height:1.7;">{info["desc"]}</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    wl=st.session_state.watchlist; in_wl=ticker in wl
    wb1,wb2,_=st.columns([1,1,2])
    with wb1:
        if st.button("✅ Remove from Watchlist" if in_wl else "➕ Add to Watchlist",type="primary",use_container_width=True):
            if in_wl: wl.remove(ticker)
            else:     wl.append(ticker)
            st.rerun()
    with wb2:
        if st.button("🔔 Set Alert",use_container_width=True):
            st.session_state.alerts.append({"ticker":ticker,"price":price,"type":"Price Alert","active":True})
            st.success(f"Alert set for {ticker} at ${price:,.2f}")

    st.markdown('<div class="disc">⚠️ This analysis is for educational purposes only. The StockWins Score is a data-based metric, not a buy/sell recommendation. Trading involves risk. Always consult a licensed financial advisor.</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: DISCOVER
# ─────────────────────────────────────────────────────────────────────
def page_discover():
    render_topbar("discover")
    st.markdown('<div class="pg">',unsafe_allow_html=True)
    avail=FREE_CATS if not is_premium() else list(CATEGORIES.keys())
    fc,mc=st.columns([1,4],gap="small")
    with fc:
        st.markdown('<div class="sec" style="font-size:12px;">Filter</div>',unsafe_allow_html=True)
        sel=st.selectbox("Category",avail,key="disc_cat",index=avail.index(st.session_state.get("discover_cat",avail[0])) if st.session_state.get("discover_cat") in avail else 0,label_visibility="collapsed")
        if not is_premium():
            st.markdown('<div class="sw-card card-gold" style="padding:10px 12px;margin-top:8px;"><div style="font-size:11px;font-weight:700;color:#f59e0b;margin-bottom:4px;">🔒 Premium Unlocks</div><div style="font-size:11px;color:#3a5068;line-height:1.8;">💥 Squeeze Radar<br>📈 Momentum Movers<br>🔄 Reversal Candidates<br>🔊 High Volume</div></div>',unsafe_allow_html=True)
            if st.button("Upgrade →",key="disc_up",type="primary",use_container_width=True): nav("pricing")
    with mc:
        if sel in PREMIUM_CATS and not is_premium(): render_lock(sel)
        else: render_category_page(sel)
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: WATCHLIST
# ─────────────────────────────────────────────────────────────────────
def page_watchlist():
    render_topbar("watchlist")
    st.markdown('<div class="pg">',unsafe_allow_html=True)
    st.markdown('<div class="sec">⭐ My Watchlist</div>',unsafe_allow_html=True)
    wl=st.session_state.watchlist
    if not wl:
        st.markdown('<div class="sw-card" style="text-align:center;padding:48px;"><div style="font-size:30px;margin-bottom:10px;">📋</div><div style="font-size:15px;font-weight:700;color:#e2e8f0;margin-bottom:6px;">Watchlist is empty</div><div style="font-size:13px;color:#3a5068;">Browse categories and click ➕ to add stocks here.</div></div>',unsafe_allow_html=True)
        if st.button("Browse Stocks →",type="primary"): nav("dashboard")
        return
    st.caption(f"{len(wl)} stocks in watchlist")
    rows=[]; prog=st.progress(0,"Loading watchlist...")
    for i,t in enumerate(wl):
        prog.progress((i+1)/len(wl),f"Loading {t}...")
        q=get_quote(t); df=get_ohlcv(t,30); info=yf_fundamentals(t); sent=st_sentiment(t)
        sc,_,op,risk,_=compute_scores(df,info,sent)
        if q:
            rows.append({"Ticker":t,"Name":q.get("name","")[:20],"Price":f"${q['price']:,.2f}",
                         "Change":f"{q['pct']:+.2f}%","SW Score":sc,"Opportunity":op,
                         "Risk":risk,"Short Float":f"{(info.get('sf',0) or 0)*100:.1f}%",
                         "Bull Sent":f"{sent.get('bull',50)}%","Sector":info.get("sector","N/A")})
    prog.empty()
    if rows:
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        if is_premium():
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown('<div class="sec" style="font-size:13px;">Watchlist Analytics</div>',unsafe_allow_html=True)
            wc=st.columns(4)
            avg_sc=sum(r["SW Score"] for r in rows)/len(rows)
            pos=sum(1 for r in rows if "+" in r["Change"])
            high_r=sum(1 for r in rows if r["Risk"] in ("High","Very High"))
            avg_b=sum(int(r["Bull Sent"].replace("%","")) for r in rows)/len(rows)
            for col,(v,l) in zip(wc,[(f"{avg_sc:.0f}","Avg SW Score"),(f"{pos}/{len(rows)}","In the Green"),(f"{high_r}","High Risk Stocks"),(f"{avg_b:.0f}%","Avg Bull Sent.")]):
                col.markdown(f'<div class="stat"><div class="stat-v">{v}</div><div class="stat-l">{l}</div></div>',unsafe_allow_html=True)
    c1,_,_=st.columns([1,1,2])
    with c1:
        if st.button("🗑️ Clear Watchlist",use_container_width=True):
            st.session_state.watchlist=[]; st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: SCREENER
# ─────────────────────────────────────────────────────────────────────
def page_screener():
    render_topbar("screener")
    st.markdown('<div class="pg">',unsafe_allow_html=True)
    st.markdown('<div class="sec">🔍 Smart Stock Screener</div>',unsafe_allow_html=True)
    if not is_premium(): render_lock("Advanced Stock Screener"); st.markdown('</div>',unsafe_allow_html=True); return
    with st.expander("⚙️ Screener Filters",expanded=True):
        c1,c2,c3,c4=st.columns(4)
        with c1: min_sc=st.slider("Min SW Score",0,100,40); min_rsi=st.slider("Min RSI",0,100,20)
        with c2: max_rsi=st.slider("Max RSI",0,100,80); min_sf=st.slider("Min Short Float %",0,50,0)
        with c3:
            req_bull=st.checkbox("MACD Bullish only"); req_above=st.checkbox("Above 20-day MA")
            req_vol=st.checkbox("Volume spike >1.5x"); req_hot=st.checkbox("StockTwits trending")
        with c4:
            sel_cats=st.multiselect("Categories",list(CATEGORIES.keys()),default=["💻 Tech","🤖 AI"])
            max_risk=st.selectbox("Max Risk",["Any","Low","Low-Medium","Medium","Medium-High","High"])
    sn,sb=st.columns([3,1])
    with sn: scr_name=st.text_input("Save as...",placeholder="My Growth Screen",label_visibility="collapsed")
    with sb:
        if st.button("💾 Save",use_container_width=True) and scr_name:
            st.session_state.saved_screeners.append({"name":scr_name,"cats":sel_cats,"min_sc":min_sc})
            st.success("Saved!")
    if st.session_state.saved_screeners:
        st.caption("Saved: "+", ".join([s["name"] for s in st.session_state.saved_screeners]))
    if st.button("🔍 Run Screener",type="primary",use_container_width=True):
        hot_list=st_hot() if req_hot else []
        universe=list(set([t for c in sel_cats for t in (CATEGORIES.get(c,[]) or st_hot())]))[:30]
        results=[]; prog=st.progress(0,"Screening...")
        risk_order=["Low","Low-Medium","Medium","Medium-High","High","Very High","Unknown"]
        max_idx=risk_order.index(max_risk) if max_risk!="Any" else 99
        for i,t in enumerate(universe):
            prog.progress((i+1)/len(universe),f"Screening {t}...")
            if req_hot and t not in hot_list: continue
            q=get_quote(t); df=get_ohlcv(t,60); info=yf_fundamentals(t); sent=st_sentiment(t)
            sc,_,op,risk,_=compute_scores(df,info,sent)
            if df is None or len(df)<20: continue
            try:
                rsi=ta.momentum.RSIIndicator(df["close"].copy(),14).rsi().iloc[-1]
                ma20=df["close"].rolling(20).mean().iloc[-1]
                mac=ta.trend.MACD(df["close"].copy())
                mv=mac.macd().iloc[-1]; ms=mac.macd_signal().iloc[-1]
                price=df["close"].iloc[-1]
                avg_v=df["volume"].rolling(20).mean().iloc[-1]; cur_v=df["volume"].iloc[-1]
                sf=(info.get("sf",0) or 0)*100
                if sc<min_sc: continue
                if pd.notna(rsi) and (rsi<min_rsi or rsi>max_rsi): continue
                if sf<min_sf: continue
                if req_bull and pd.notna(mv) and mv<ms: continue
                if req_above and pd.notna(ma20) and price<ma20: continue
                if req_vol and pd.notna(avg_v) and avg_v>0 and cur_v<avg_v*1.5: continue
                if max_risk!="Any" and risk in risk_order and risk_order.index(risk)>max_idx: continue
                results.append({"Ticker":t,"Price":f"${price:,.2f}" if q else "N/A",
                                "RSI":round(rsi,1) if pd.notna(rsi) else "N/A","SW Score":sc,
                                "Opportunity":op,"Risk":risk,"Short Float":f"{sf:.1f}%",
                                "MACD":"Bullish" if (pd.notna(mv) and mv>ms) else "Bearish",
                                "vs MA20":"Above" if price>ma20 else "Below",
                                "Vol Ratio":f"{cur_v/avg_v:.1f}x" if pd.notna(avg_v) and avg_v>0 else "N/A",
                                "Bull Sent":f"{sent.get('bull',50)}%"})
            except: continue
        prog.empty()
        if results:
            st.success(f"✅ {len(results)} stocks passed your filters!")
            st.dataframe(pd.DataFrame(results).sort_values("SW Score",ascending=False),use_container_width=True,hide_index=True)
        else:
            st.info("No stocks matched your criteria. Try relaxing the filters.")
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: BI ANALYTICS
# ─────────────────────────────────────────────────────────────────────
def page_bi():
    render_topbar("bi_dashboard")
    st.markdown('<div class="pg">',unsafe_allow_html=True)
    st.markdown('<div class="sec">📊 BI Analytics Dashboard</div>',unsafe_allow_html=True)
    with st.spinner("Loading analytics data..."):
        movers=get_bi_movers(); secs=get_sectors(); idx=get_indexes(); hot=st_hot()
    gainers=sorted(movers,key=lambda x:x["pct"],reverse=True)
    losers=sorted(movers,key=lambda x:x["pct"])
    vol_ldrs=sorted(movers,key=lambda x:x["vr"],reverse=True)
    # Summary widgets
    sw=st.columns(5)
    top_g=gainers[0] if gainers else {}; top_l=losers[0] if losers else {}; top_v=vol_ldrs[0] if vol_ldrs else {}
    bull_sec=max(secs,key=secs.get) if secs else "N/A"; bear_sec=min(secs,key=secs.get) if secs else "N/A"
    for col,(v,l,c) in zip(sw,[
        (top_g.get("t","—"),f"Top Gainer +{top_g.get('pct',0):.1f}%","#22c55e"),
        (top_l.get("t","—"),f"Top Loser {top_l.get('pct',0):.1f}%","#ef4444"),
        (top_v.get("t","—"),f"Volume King {top_v.get('vr',0):.1f}x","#60a5fa"),
        (bull_sec,f"Best Sector +{secs.get(bull_sec,0):.1f}%","#22c55e"),
        (bear_sec,f"Weak Sector {secs.get(bear_sec,0):.1f}%","#ef4444"),
    ]):
        col.markdown(f'<div class="stat"><div style="font-family:\'JetBrains Mono\',monospace;font-size:16px;font-weight:700;color:{c};">{v}</div><div class="stat-l">{l}</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    tabs=st.tabs(["📈 Leaderboards","🗺️ Sector Analysis","📡 Social","🔊 Volume Surge","📋 Summary"])
    with tabs[0]:
        lc1,lc2,lc3=st.columns(3,gap="small")
        with lc1:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#22c55e;margin-bottom:8px;">🏆 Top Gainers</div>',unsafe_allow_html=True)
            for m in gainers[:10]: st.markdown(f'<div class="mv"><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;font-size:12px;">{m["t"]}</span><span style="color:#3a5068;font-size:11px;">${m["price"]:,.2f}</span><span style="color:#22c55e;font-weight:700;font-size:12px;">▲{m["pct"]:.2f}%</span></div>',unsafe_allow_html=True)
        with lc2:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#ef4444;margin-bottom:8px;">📉 Top Losers</div>',unsafe_allow_html=True)
            for m in losers[:10]: st.markdown(f'<div class="mv"><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;font-size:12px;">{m["t"]}</span><span style="color:#3a5068;font-size:11px;">${m["price"]:,.2f}</span><span style="color:#ef4444;font-weight:700;font-size:12px;">▼{abs(m["pct"]):.2f}%</span></div>',unsafe_allow_html=True)
        with lc3:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#60a5fa;margin-bottom:8px;">🔊 Volume Leaders</div>',unsafe_allow_html=True)
            for m in vol_ldrs[:10]:
                c="#ef4444" if m["vr"]>=3 else "#fbbf24" if m["vr"]>=2 else "#60a5fa"
                st.markdown(f'<div class="mv"><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;font-size:12px;">{m["t"]}</span><span style="color:#3a5068;font-size:11px;">{m["vol"]/1e6:.1f}M shares</span><span style="font-weight:700;font-size:12px;color:{c};">{m["vr"]:.1f}x avg</span></div>',unsafe_allow_html=True)
    with tabs[1]:
        sec_sorted=sorted(secs.items(),key=lambda x:x[1],reverse=True)
        for sec,chg in sec_sorted:
            c="#22c55e" if chg>0 else "#ef4444"; bar=min(abs(chg)*8,100)
            st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;">
                <div style="width:100px;font-size:11px;color:#4a6080;">{sec}</div>
                <div style="flex:1;background:#111c2e;border-radius:3px;height:18px;position:relative;overflow:hidden;">
                    <div style="background:{"#052e16" if chg>=0 else "#1c0000"};width:{bar}%;height:18px;display:flex;align-items:center;padding-left:8px;">
                        <span style="color:{c};font-size:11px;font-weight:700;">{"▲" if chg>=0 else "▼"}{abs(chg):.2f}%</span>
                    </div>
                </div>
            </div>""",unsafe_allow_html=True)
    with tabs[2]:
        sc1,sc2=st.columns(2)
        with sc1:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#c9d3e0;margin-bottom:8px;">🔥 StockTwits Trending</div>',unsafe_allow_html=True)
            for i,t in enumerate(hot[:8],1):
                s=st_sentiment(t); bc="#22c55e" if s["bull"]>=60 else "#ef4444" if s["bull"]<40 else "#94a3b8"
                st.markdown(f'<div class="mv"><span style="color:#2a3a50;font-size:10px;">#{i}</span> <span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;font-size:12px;">{t}</span> <span style="color:#2a3a50;font-size:11px;">{s.get("wl",0):,} watching</span> <span style="color:{bc};font-weight:700;font-size:12px;">{s["bull"]}% bull</span></div>',unsafe_allow_html=True)
        with sc2:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#c9d3e0;margin-bottom:8px;">👥 Most Discussed</div>',unsafe_allow_html=True)
            targets=["NVDA","TSLA","AMD","AAPL","MSTR","PLTR","GME","META"]
            discussed=sorted([(t,st_sentiment(t)) for t in targets],key=lambda x:x[1].get("wl",0),reverse=True)
            for t,s in discussed[:6]:
                bc="#22c55e" if s["bull"]>=60 else "#ef4444" if s["bull"]<40 else "#94a3b8"
                st.markdown(f'<div class="mv"><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;font-size:12px;">{t}</span> <span style="color:#2a3a50;font-size:11px;">{s.get("wl",0):,}</span> <span style="color:{bc};font-weight:700;font-size:12px;">{s["bull"]}% bull</span></div>',unsafe_allow_html=True)
    with tabs[3]:
        surge=[m for m in movers if m["vr"]>=1.5]; surge.sort(key=lambda x:x["vr"],reverse=True)
        if surge:
            sd=pd.DataFrame([{"Ticker":m["t"],"Price":f"${m['price']:,.2f}","Day Change":f"{m['pct']:+.2f}%","Volume":f"{m['vol']/1e6:.2f}M","Vol Ratio":f"{m['vr']:.1f}x avg"} for m in surge])
            st.dataframe(sd,use_container_width=True,hide_index=True)
        else: st.info("No significant volume surges detected right now.")
        st.markdown('<div class="ins" style="margin-top:12px;"><div style="font-size:12px;font-weight:700;color:#c9d3e0;margin-bottom:4px;">What is a Volume Surge?</div><div style="font-size:12px;color:#3a5068;line-height:1.5;">When a stock trades at significantly above-average volume, it often signals something important — institutional buying/selling, news, social buzz, or a technical breakout. High-volume moves tend to be more reliable and sustained than low-volume ones.</div></div>',unsafe_allow_html=True)
    with tabs[4]:
        avg_pct=sum(m["pct"] for m in movers)/len(movers) if movers else 0
        bull_s=[s for s,c in secs.items() if c>0.5]; bear_s=[s for s,c in secs.items() if c<-0.5]
        sent_lbl="Bullish" if avg_pct>0.3 else "Bearish" if avg_pct<-0.3 else "Neutral"
        sc_,sc2_=st.columns(2)
        with sc_:
            st.markdown(f"""<div class="sw-card"><div style="font-size:13px;font-weight:700;color:#c9d3e0;margin-bottom:10px;">Market Overview</div>
                <div class="mv"><span style="color:#3a5068;">Overall Sentiment</span><span style="color:{"#22c55e" if avg_pct>0 else "#ef4444"};font-weight:700;">{sent_lbl}</span></div>
                <div class="mv"><span style="color:#3a5068;">Avg Stock Move</span><span style="color:{"#22c55e" if avg_pct>0 else "#ef4444"};font-weight:700;">{avg_pct:+.2f}%</span></div>
                <div class="mv"><span style="color:#3a5068;">Bullish Sectors</span><span style="color:#22c55e;font-weight:700;">{len(bull_s)}/10</span></div>
                <div class="mv"><span style="color:#3a5068;">Bearish Sectors</span><span style="color:#ef4444;font-weight:700;">{len(bear_s)}/10</span></div>
                <div class="mv"><span style="color:#3a5068;">Volume Surges</span><span style="color:#60a5fa;font-weight:700;">{len([m for m in movers if m["vr"]>=2])} stocks</span></div>
            </div>""",unsafe_allow_html=True)
        with sc2_:
            st.markdown(f"""<div class="sw-card"><div style="font-size:13px;font-weight:700;color:#c9d3e0;margin-bottom:10px;">Key Highlights</div>
                <div style="font-size:12px;color:#3a5068;line-height:2.2;">
                🟢 <b style="color:#4a6080;">Best sectors:</b> {', '.join(bull_s[:3]) if bull_s else 'None'}<br>
                🔴 <b style="color:#4a6080;">Weak sectors:</b> {', '.join(bear_s[:3]) if bear_s else 'None'}<br>
                🔥 <b style="color:#4a6080;">Social buzz:</b> {', '.join(hot[:5])}<br>
                🔊 <b style="color:#4a6080;">Volume king:</b> {top_v.get('t','—')} ({top_v.get('vr',0):.1f}x avg)<br>
                📈 <b style="color:#4a6080;">Top gainer:</b> {top_g.get('t','—')} (+{top_g.get('pct',0):.2f}%)
                </div>
            </div>""",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: PRICING
# ─────────────────────────────────────────────────────────────────────
def page_pricing():
    render_topbar("pricing")
    st.markdown('<div class="pg">',unsafe_allow_html=True)
    st.markdown('<div class="sec">💰 Plans & Pricing</div>',unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:13px;color:#3a5068;margin-bottom:24px;">Simple pricing. Cancel anytime.</div>',unsafe_allow_html=True)
    p1,p2,p3=st.columns([1,1.1,1],gap="small")
    with p1:
        st.markdown("""<div class="pc"><div style="font-size:15px;font-weight:700;color:#c9d3e0;">Free</div>
            <div class="pc-price">$0</div><div style="font-size:11px;color:#2a3a50;margin-bottom:14px;">forever</div>
            <hr style="border-color:#111c2e;margin:14px 0;">
            <div style="font-size:12px;color:#3a5068;line-height:2.2;">
            ✅ Market overview & indexes<br>✅ 5 stock categories<br>✅ StockTwits hot list<br>
            ✅ Basic signals (RSI, MACD)<br>✅ Plain-English insights<br>✅ Watchlist (10 stocks)<br>
            ✅ Basic BI preview<br>❌ Short squeeze scanner<br>❌ Advanced screener<br>
            ❌ Premium categories<br>❌ Score breakdowns<br>❌ Watchlist analytics</div></div>""",unsafe_allow_html=True)
        if not is_authed():
            if st.button("Get Started Free",use_container_width=True): nav("signup")
    with p2:
        st.markdown("""<div class="pc-feat"><div style="background:#2563eb;color:white;font-size:9px;font-weight:700;padding:3px 10px;border-radius:20px;display:inline-block;margin-bottom:8px;letter-spacing:1.5px;">⭐ MOST POPULAR</div>
            <div style="font-size:15px;font-weight:700;color:#c9d3e0;">Premium Monthly</div>
            <div class="pc-price">$29</div><div style="font-size:11px;color:#2a3a50;margin-bottom:14px;">per month · cancel anytime</div>
            <hr style="border-color:#111c2e;margin:14px 0;">
            <div style="font-size:12px;color:#3a5068;line-height:2.2;">
            ✅ Everything in Free<br>✅ All 13+ stock categories<br>✅ Short squeeze scanner<br>
            ✅ Advanced multi-factor screener<br>✅ Full BI analytics<br>✅ Score breakdowns<br>
            ✅ Volume surge detection<br>✅ Momentum scanner<br>✅ Reversal candidates<br>
            ✅ Unlimited watchlist<br>✅ Watchlist analytics<br>✅ Saved screeners</div></div>""",unsafe_allow_html=True)
        if st.button("🚀 Start Premium →",type="primary",use_container_width=True):
            st.info("💳 Payment processing coming soon. Contact support@stockwins.com to upgrade.")
    with p3:
        st.markdown("""<div class="pc"><div style="background:linear-gradient(90deg,#854d0e,#d97706);color:white;font-size:9px;font-weight:700;padding:3px 10px;border-radius:20px;display:inline-block;margin-bottom:4px;letter-spacing:1px;">BEST VALUE</div>
            <div style="font-size:15px;font-weight:700;color:#c9d3e0;">Annual Plan</div>
            <div class="pc-price">$199</div><div style="font-size:11px;color:#2a3a50;margin-bottom:14px;">per year · save 43%</div>
            <hr style="border-color:#111c2e;margin:14px 0;">
            <div style="font-size:12px;color:#3a5068;line-height:2.2;">
            ✅ Everything in Premium<br>✅ Priority support<br>✅ Early feature access<br>
            ✅ Export data to CSV<br>✅ Custom price alerts<br>✅ API access (Q3 2026)<br>
            ✅ Backtesting module (coming)<br>✅ Portfolio tracker (coming)</div></div>""",unsafe_allow_html=True)
        if st.button("Get Annual Plan →",use_container_width=True):
            st.info("💳 Payment processing coming soon!")
    st.markdown('<div class="disc">⚠️ StockWins is an educational data analysis tool. Subscriptions provide access to data features only. Nothing constitutes financial advice. Always consult a licensed advisor.</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────────────────────────────────
def page_settings():
    render_topbar()
    st.markdown('<div class="pg">',unsafe_allow_html=True)
    st.markdown('<div class="sec">⚙️ Account Settings</div>',unsafe_allow_html=True)
    db_user=get_db_user(); email=st.session_state.user["email"] if is_authed() else ""
    tabs=st.tabs(["👤 Profile","🔐 Security","🔔 Alerts","📊 Subscription"])
    with tabs[0]:
        with st.form("pf"):
            new_name=st.text_input("Display Name",value=st.session_state.user.get("name",""))
            st.text_input("Email",value=email,disabled=True)
            st.caption("Email cannot be changed.")
            verified=db_user.get("verified",False)
            if not verified: st.warning("⚠️ Email not verified.")
            else: st.markdown('<span style="font-size:12px;color:#22c55e;">✅ Email verified</span>',unsafe_allow_html=True)
            if st.form_submit_button("Save Changes",type="primary") and new_name:
                st.session_state.user["name"]=new_name
                if email in st.session_state.users_db: st.session_state.users_db[email]["name"]=new_name
                st.success("✅ Profile updated!")
    with tabs[1]:
        with st.form("pwf"):
            cp=st.text_input("Current Password",type="password")
            np=st.text_input("New Password",type="password")
            np2=st.text_input("Confirm New",type="password")
            if st.form_submit_button("Update Password",type="primary"):
                if hp(cp)!=db_user.get("pw",""): st.error("Current password incorrect.")
                elif np!=np2: st.error("New passwords don't match.")
                elif len(np)<6: st.error("Must be 6+ characters.")
                else: st.session_state.users_db[email]["pw"]=hp(np); st.success("✅ Password updated!")
        st.divider()
        if st.button("🚪 Logout All Sessions",use_container_width=True): logout()
    with tabs[2]:
        with st.form("af"):
            ac1,ac2,ac3=st.columns(3)
            with ac1: at=st.text_input("Ticker",placeholder="AAPL").upper()
            with ac2: ap=st.number_input("Alert Price",value=100.0,min_value=0.01)
            with ac3: atype=st.selectbox("Type",["Price Above","Price Below","% Move Up","% Move Down"])
            if st.form_submit_button("➕ Add Alert",type="primary") and at:
                st.session_state.alerts.append({"ticker":at,"price":ap,"type":atype,"active":True})
                st.success(f"Alert set: {at} {atype} ${ap:.2f}")
        if st.session_state.alerts:
            for i,a in enumerate(st.session_state.alerts):
                ac1,ac2=st.columns([4,1])
                with ac1: st.markdown(f'<div class="sw-card" style="padding:10px 14px;margin-bottom:4px;"><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;">{a["ticker"]}</span> <span style="font-size:12px;color:#3a5068;">{a["type"]} ${a["price"]:.2f}</span></div>',unsafe_allow_html=True)
                with ac2:
                    if st.button("🗑",key=f"da_{i}",use_container_width=True): st.session_state.alerts.pop(i); st.rerun()
        else: st.caption("No active alerts.")
    with tabs[3]:
        role=st.session_state.role
        rl={"free":"Free","premium":"Premium Monthly","admin":"Admin","owner":"Owner"}.get(role,"Free")
        rc_={"free":"#506070","premium":"#a78bfa","admin":"#60a5fa","owner":"#f59e0b"}.get(role,"#506070")
        st.markdown(f"""<div class="sw-card card-blue">
            <div style="font-size:15px;font-weight:800;color:#e2e8f0;margin-bottom:4px;">Current Plan: <span style="color:{rc_};">{rl}</span></div>
            <div style="font-size:12px;color:#3a5068;">Member since {db_user.get('joined','N/A')}</div>
        </div>""",unsafe_allow_html=True)
        if not is_premium():
            st.markdown("<br>",unsafe_allow_html=True)
            uc1,uc2=st.columns(2)
            with uc1:
                if st.button("🚀 Upgrade Monthly ($29/mo)",type="primary",use_container_width=True): st.info("💳 Coming soon!")
            with uc2:
                if st.button("💰 Get Annual ($199/yr)",use_container_width=True): st.info("💳 Coming soon!")
    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# PAGE: ADMIN PANEL
# ─────────────────────────────────────────────────────────────────────
def page_admin():
    if not is_admin():
        st.error("Access denied. Admin only."); return
    render_topbar("admin")
    st.markdown('<div class="pg">',unsafe_allow_html=True)

    # Admin badge
    role_lbl="👑 Owner" if is_owner() else "🛡 Admin"
    st.markdown(f'<div class="sec">🛠️ Admin Panel <span class="cnt">{role_lbl}</span></div>',unsafe_allow_html=True)

    tabs=st.tabs(["📊 Overview","👥 User Management","🔑 API Settings","⚙️ Site Config","📈 Analytics"])

    # OVERVIEW
    with tabs[0]:
        ss=st.session_state.site_stats
        oc=st.columns(5)
        for col,(v,l,c) in zip(oc,[
            (ss["total_signups"],"Total Signups","#60a5fa"),
            (ss["premium_users"],"Premium Users","#a78bfa"),
            (ss["daily_active"],"Daily Active","#22c55e"),
            (f"{ss['conversion_rate']:.1f}%","Conversion Rate","#fbbf24"),
            (len(st.session_state.users_db),"Registered Accounts","#94a3b8"),
        ]):
            col.markdown(f'<div class="admin-stat"><div style="font-family:\'JetBrains Mono\',monospace;font-size:22px;font-weight:700;color:{c};">{v}</div><div class="stat-l">{l}</div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        ac1,ac2=st.columns(2)
        with ac1:
            st.markdown('<div class="sec" style="font-size:12px;">Most Viewed Categories</div>',unsafe_allow_html=True)
            cats=[("🔥 Trending Now",4218),("💻 Tech",3891),("🤖 AI",3104),("💥 Squeeze Radar",2876),("📡 Social Buzz",2341)]
            for cat,views in cats: st.markdown(f'<div class="mv"><span style="font-size:12px;color:#c9d3e0;">{cat}</span><span style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:#60a5fa;">{views:,} views</span></div>',unsafe_allow_html=True)
        with ac2:
            st.markdown('<div class="sec" style="font-size:12px;">Top Watchlisted Stocks</div>',unsafe_allow_html=True)
            stocks=ss.get("top_watchlisted",[]); counts=[894,762,651,598,487]
            for t,c in zip(stocks,counts): st.markdown(f'<div class="mv"><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:#60a5fa;">{t}</span><span style="font-size:12px;color:#3a5068;">{c:,} users watching</span></div>',unsafe_allow_html=True)
        st.markdown('<div class="sec" style="font-size:12px;margin-top:16px;">Data Source Health</div>',unsafe_allow_html=True)
        hc=st.columns(3)
        key_set=bool(get_td_key())
        for col,(name,status,note) in zip(hc,[
            ("Yahoo Finance","✅ Online","Free tier · No key needed"),
            ("StockTwits API","✅ Online","Public endpoints · Rate limited"),
            ("Twelve Data",f"{'✅ Configured' if key_set else '⚠️ Not Set'}","Optional · Premium data quality"),
        ]):
            c_="#22c55e" if "✅" in status else "#fbbf24"
            col.markdown(f'<div class="sw-card"><div style="font-size:12px;font-weight:700;color:#c9d3e0;margin-bottom:4px;">{name}</div><div style="font-size:12px;font-weight:700;color:{c_};">{status}</div><div style="font-size:11px;color:#2a3a50;margin-top:3px;">{note}</div></div>',unsafe_allow_html=True)

    # USER MANAGEMENT
    with tabs[1]:
        st.markdown('<div class="sec" style="font-size:13px;">Registered Users</div>',unsafe_allow_html=True)
        db=st.session_state.users_db
        for email,u in db.items():
            role=u["role"]; badge_cls={"owner":"role-badge-owner","admin":"role-badge-admin","premium":"role-badge-premium","free":"role-badge-free"}.get(role,"role-badge-free")
            uc1,uc2,uc3,uc4=st.columns([3,1,2,2])
            with uc1:
                v_icon="✅" if u.get("verified") else "⚠️"
                st.markdown(f'<div style="padding:8px 0;"><div style="font-size:13px;font-weight:600;color:#c9d3e0;">{u["name"]}</div><div style="font-size:11px;color:#2a3a50;">{v_icon} {email} · Joined {u.get("joined","N/A")}</div></div>',unsafe_allow_html=True)
            with uc2:
                st.markdown(f'<div style="padding:10px 0;"><span class="{badge_cls}">{role.upper()}</span></div>',unsafe_allow_html=True)
            with uc3:
                if is_owner() and role!="owner":
                    new_role=st.selectbox("Role",["free","premium","admin"],index=["free","premium","admin"].index(role) if role in ["free","premium","admin"] else 0,key=f"role_{email}",label_visibility="collapsed")
                    if st.button("Update",key=f"upd_{email}",use_container_width=True):
                        st.session_state.users_db[email]["role"]=new_role; st.success(f"Updated {email} to {new_role}"); st.rerun()
            with uc4:
                if is_owner() and email!=st.session_state.user["email"]:
                    if st.button("🗑 Delete",key=f"del_{email}",use_container_width=True):
                        del st.session_state.users_db[email]; st.rerun()
            st.markdown('<div style="border-bottom:1px solid #0e1525;margin-bottom:4px;"></div>',unsafe_allow_html=True)
        st.markdown('<div class="sec" style="font-size:12px;margin-top:16px;">Add Test Account</div>',unsafe_allow_html=True)
        with st.form("add_user"):
            tc1,tc2,tc3,tc4=st.columns(4)
            with tc1: ne=st.text_input("Email",placeholder="test@example.com")
            with tc2: nn=st.text_input("Name",placeholder="Test User")
            with tc3: np_=st.text_input("Password",placeholder="password123")
            with tc4: nr=st.selectbox("Role",["free","premium","admin"])
            if st.form_submit_button("Create Account",type="primary"):
                if ne and nn and np_:
                    ok,msg=signup(ne,np_,nn)
                    if ok:
                        st.session_state.users_db[ne]["role"]=nr
                        st.session_state.users_db[ne]["verified"]=True
                        st.success(f"Account created: {ne} ({nr})")
                    else: st.error(msg)

    # API SETTINGS (admin only)
    with tabs[2]:
        st.markdown('<div class="sec" style="font-size:13px;">Data Provider Configuration</div>',unsafe_allow_html=True)
        st.markdown("""<div class="sw-card card-green">
            <div style="font-size:12px;font-weight:700;color:#4ade80;margin-bottom:6px;">✅ Yahoo Finance — Always Active</div>
            <div style="font-size:12px;color:#3a5068;">Free tier. No key needed. Used for all price data, volume, fundamentals, and short interest by default.</div>
        </div>""",unsafe_allow_html=True)
        st.markdown("""<div class="sw-card">
            <div style="font-size:12px;font-weight:700;color:#c9d3e0;margin-bottom:6px;">✅ StockTwits API — Always Active</div>
            <div style="font-size:12px;color:#3a5068;">Free public endpoints. Used for social sentiment, trending stocks, and watchlist counts. No key required.</div>
        </div>""",unsafe_allow_html=True)
        st.markdown('<div class="sec" style="font-size:13px;margin-top:8px;">Twelve Data API (Optional — Premium Quality)</div>',unsafe_allow_html=True)
        try:
            sk=st.secrets.get("TWELVE_DATA_API_KEY","")
            if sk: st.markdown('<div style="background:#052e16;border:1px solid #166534;border-radius:6px;padding:10px 14px;font-size:12px;color:#4ade80;">✅ Configured via Streamlit Secrets (server-side, secure)</div>',unsafe_allow_html=True)
        except: pass
        st.caption("If not in Streamlit Secrets, you can set a session key below (admin only, never shown to users):")
        cur_key=st.session_state.api_override
        masked=f"{'*'*(len(cur_key)-4)}{cur_key[-4:]}" if len(cur_key)>4 else ("Set" if cur_key else "Not set")
        st.markdown(f'<div style="font-size:12px;color:#3a5068;margin-bottom:6px;">Current: {masked}</div>',unsafe_allow_html=True)
        with st.form("api_form"):
            new_key=st.text_input("Twelve Data API Key",type="password",placeholder="Enter key here (admin only)")
            if st.form_submit_button("Save Key",type="primary"):
                st.session_state.api_override=new_key
                st.success("✅ Key saved for this session. For permanent setup, add to Streamlit Cloud Secrets.")
        if st.button("Clear API Key",use_container_width=True):
            st.session_state.api_override=""; st.success("Key cleared.")
        st.markdown("""<div class="disc">🔒 <strong>Security Note:</strong> API keys are never exposed to regular users. Keys are stored server-side only. For permanent deployment, always use Streamlit Cloud Secrets (Settings → Secrets) rather than the session override above.</div>""",unsafe_allow_html=True)

    # SITE CONFIG
    with tabs[3]:
        if not is_owner():
            st.warning("Site configuration is available to Owner role only.")
        else:
            st.markdown('<div class="sec" style="font-size:13px;">Featured Categories</div>',unsafe_allow_html=True)
            st.multiselect("Free tier categories",list(CATEGORIES.keys()),default=FREE_CATS,key="featured_free")
            st.multiselect("Premium categories",list(CATEGORIES.keys()),default=list(PREMIUM_CATS),key="featured_prem")
            st.divider()
            st.markdown('<div class="sec" style="font-size:13px;">Homepage Content</div>',unsafe_allow_html=True)
            st.text_input("Hero Headline",value="Spot Market Opportunities Before They Get Crowded")
            st.text_area("Hero Subheadline",value="Discover trending stocks, social buzz, short squeeze candidates, and momentum shifts in one powerful dashboard.",height=80)
            if st.button("Save Site Config",type="primary"): st.success("Config saved (simulated in demo)")
            st.divider()
            st.markdown('<div class="sec" style="font-size:13px;">Danger Zone</div>',unsafe_allow_html=True)
            if st.button("🔄 Reset Demo Data"): st.warning("This would reset all demo user data. (Simulated)")

    # ANALYTICS
    with tabs[4]:
        st.markdown('<div class="sec" style="font-size:13px;">Conversion Analytics</div>',unsafe_allow_html=True)
        ss=st.session_state.site_stats
        ac=st.columns(4)
        for col,(v,l) in zip(ac,[(f"{ss['total_signups']:,}","Total Signups"),(f"{ss['premium_users']:,}","Premium"),(f"{ss['conversion_rate']:.1f}%","Trial→Paid"),(f"{ss['daily_active']:,}","Daily Active")]):
            col.markdown(f'<div class="admin-stat"><div style="font-family:\'JetBrains Mono\',monospace;font-size:18px;font-weight:700;color:#60a5fa;">{v}</div><div class="stat-l">{l}</div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="sec" style="font-size:13px;">Simulated Growth Trend (30d)</div>',unsafe_allow_html=True)
        import random
        dates=pd.date_range(end=datetime.now(),periods=30,freq='D')
        signups=[random.randint(40,120) for _ in range(30)]
        premium=[random.randint(5,25) for _ in range(30)]
        chart_df=pd.DataFrame({"Signups":signups,"Premium Upgrades":premium},index=dates)
        st.line_chart(chart_df)
        st.markdown('<div class="disc">📊 Analytics are simulated for demo purposes. In production, connect to your analytics provider (Mixpanel, PostHog, Segment, etc.)</div>',unsafe_allow_html=True)

    st.markdown('</div>',unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────
render_sidebar()

page=st.session_state.page
guard={"dashboard","discover","watchlist","screener","bi_dashboard","stock_detail","settings","admin"}

if page in guard and not is_authed():
    page_login()
elif page=="landing":          page_landing()
elif page=="login":            page_login()
elif page=="signup":           page_signup()
elif page=="verify_email":     page_verify()
elif page=="forgot_pw":        page_forgot_pw()
elif page=="pricing":          page_pricing()
elif page=="dashboard":        page_dashboard()
elif page=="discover":         page_discover()
elif page=="watchlist":        page_watchlist()
elif page=="screener":         page_screener()
elif page=="bi_dashboard":     page_bi()
elif page=="stock_detail":     page_detail()
elif page=="settings":         page_settings()
elif page=="admin":
    if is_admin(): page_admin()
    else: st.error("Access denied."); nav("dashboard")
else: page_landing()
