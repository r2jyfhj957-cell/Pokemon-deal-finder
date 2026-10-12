import streamlit as st
import pandas as pd
from urllib.parse import quote_plus

st.set_page_config(page_title="Pokémon Deal Finder", page_icon="🔎", layout="wide")
st.title("Pokémon Deal Finder — Starter")
st.caption("Compare candidate listings with your own verified market prices. No live marketplace connection yet.")
category=st.selectbox("Product type", ["Sealed Pokémon products","Individual cards","PSA 10 graded cards"])
query=st.text_input("Search terms", "Pokémon booster box")
cols=st.columns(3)
with cols[0]: asking=st.number_input("Listing price ($)", min_value=0.0, value=100.0, step=1.0)
with cols[1]: shipping=st.number_input("Shipping ($)", min_value=0.0, value=0.0, step=1.0)
with cols[2]: market=st.number_input("Verified comparable market value ($)", min_value=0.0, value=130.0, step=1.0)
fee=st.slider("Estimated resale fees (%)", 0, 30, 13)
other=st.number_input("Other costs ($)", min_value=0.0, value=0.0, step=1.0)
cost=asking+shipping
net=market*(1-fee/100)-cost-other
discount=(market-cost)/market*100 if market else 0
a,b,c=st.columns(3)
a.metric("Total purchase cost",f"${cost:,.2f}")
b.metric("Below market",f"{discount:.1f}%")
c.metric("Estimated resale profit",f"${net:,.2f}")
st.info("Estimates only: confirm exact variant, condition, authenticity, completed sales, taxes, and current availability.")
st.subheader("Find candidate listings")
st.markdown(f"[Search eBay listings](https://www.ebay.com/sch/i.html?_nkw={quote_plus(query)}) · [Search eBay sold listings](https://www.ebay.com/sch/i.html?_nkw={quote_plus(query)}&LH_Sold=1&LH_Complete=1) · [Search TCGplayer](https://www.tcgplayer.com/search/all/product?q={quote_plus(query)})")
st.subheader("Save your comparisons")
if "rows" not in st.session_state: st.session_state.rows=[]
if st.button("Add comparison"):
    st.session_state.rows.append(dict(type=category, item=query, asking=asking, shipping=shipping, market_value=market, estimated_profit=round(net,2), below_market_pct=round(discount,1)))
if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True)
    st.download_button("Download comparisons CSV",df.to_csv(index=False),"pokemon_comparisons.csv","text/csv")
