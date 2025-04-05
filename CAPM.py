import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import capm_function
st.set_page_config(page_title="CAPM",
page_icon="chart_with_upwards_trend",
layout="wide"
)
st.title=("Capital Asset Model")
col1,col2=st.columns([1,1])
with col1:
    stock_list=st.multiselect("choose stocks",(
    "AAPL",  # Apple Inc.
    "MSFT",  # Microsoft Corporation
    "GOOGL",  # Alphabet Inc. (Google)
    "AMZN",  # Amazon.com Inc.
    "TSLA",  # Tesla Inc.
    "NVDA",  # NVIDIA Corporation
    "META",  # Meta Platforms Inc. (Facebook)
    "BRK.B",  # Berkshire Hathaway Inc. (Class B)
    "JPM",  # JPMorgan Chase & Co.
    "V",  # Visa Inc.
    "JNJ",  # Johnson & Johnson
    "WMT",  # Walmart Inc.
    "PG",  # Procter & Gamble Co.
    "DIS",  # The Walt Disney Company
    "NFLX",  # Netflix Inc.
    "KO",  # The Coca-Cola Company
    "PEP",  # PepsiCo Inc.
    "XOM",  # ExxonMobil Corporation
    "CVX",  # Chevron Corporation
    "INTC",  # Intel Corporation
    "AMD",  # Advanced Micro Devices Inc.
    "BA",  # The Boeing Company
    "GS",  # The Goldman Sachs Group Inc.
    "PYPL",  # PayPal Holdings Inc.
    "ADBE",  # Adobe Inc.
    "COST",  # Costco Wholesale Corporation
    "MRNA",  # Moderna Inc.
    "NKE",  # Nike Inc.
    "T",  # AT&T Inc.
    "SOFI"  # SoFi Technologies Inc.

),["TSLA","AAPL","NFLX","MSFT"])
with col2:
    year=st.number_input("Enter the number of years",1,4)

end=datetime.date.today()
start=datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
SP500=web.DataReader(["sp500"],'fred',start,end)
stock_df=pd.DataFrame()
# print(SP500.head())
for stock in stock_list:
    data=yf.download(stock,period=f"{year}y")
    stock_df[f"{stock}"]=data["Close"]
stock_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns=["Date",'sp500']
stock_df['Date']=stock_df['Date'].astype("datetime64[ns]")
stock_df['Date']=stock_df["Date"].apply(lambda x:str(x)[:10])
stock_df['Date']=pd.to_datetime(stock_df["Date"])
stock_df=pd.merge(stock_df,SP500,on='Date',how="inner")
col1,col2=st.columns([1,1])
with col1:
    st.markdown("### DataFrame head")
    st.dataframe(stock_df.head(),use_container_width=True)
with col2:
    st.markdown("### DataFrame Tail")
    st.dataframe(stock_df.tail(),use_container_width=True)
col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Price of all the stock")
    st.plotly_chart(capm_function.interactive_plot(stock_df))
with col2:
    st.markdown("### Price of all the stock After Normalization")
    st.plotly_chart(capm_function.interactive_plot(capm_function.normalization(stock_df)))

stocks_daily_return=capm_function.daily_return(stock_df)
print(stocks_daily_return.head())
beta={}
alpha={}
for i in stocks_daily_return.columns:
    if i !='Date' and i !='sp500':
        b,a=capm_function.calculate_beta(stocks_daily_return,i)
        beta[i]=b
        alpha[i]=a

beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
beta_df['Stock']=beta.keys()
beta_df['Beta Value']=[str(round(i,2)) for i in beta.values()]
with col1:
    st.markdown('### Calculate Beta Value')
    st.dataframe(beta_df,use_container_width=True)
rf=0
rm=stocks_daily_return['sp500'].mean()*252
return_df=pd.DataFrame()
return_value=[]
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df['Stock']=stock_list
return_df['Return Value']=return_value
with col2:
    st.markdown('### Calculate Return using CAPM')
    st.dataframe(return_df,use_container_width=True)

