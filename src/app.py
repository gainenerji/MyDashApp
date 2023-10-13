import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table,dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import dash_bootstrap_components as dbc
from functions import *
from dash import Input, Output, html
from datetime import datetime, timedelta

""" 

today = "2023-09-18"
yesterday = "2023-09-17"
tomorrow = "2023-09-19"

"""
saat = pd.Series(range(0,24))

if datetime.today().hour > 17:
    today = datetime.today().strftime('%Y-%m-%d')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    first_day_of_the_month = datetime.today().strftime('%Y-%m-01')
    first_day_of_the_year = datetime.today().strftime('%Y-01-01')
    first_day_of_the_month_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-01')
    first_day_of_the_year_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-01-01')
    today_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    rapor_tarihi = datetime.today().strftime("%d-%m-%Y")
else:
    today = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    tomorrow = datetime.today().strftime('%Y-%m-%d')
    first_day_of_the_month = datetime.today().strftime('%Y-%m-01')
    first_day_of_the_year = datetime.today().strftime('%Y-01-01')
    first_day_of_the_month_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-01')
    first_day_of_the_year_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-01-01')
    today_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    rapor_tarihi = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")

price_yesterday = ptf_smf(yesterday, yesterday)
price_today = ptf_smf(today, today)
price_tomorrow = ptf_smf(tomorrow, tomorrow)

price_yesterday["Tarih"] = pd.to_datetime(price_yesterday["Tarih"])

max_fiyat = price_yesterday.apply(fiyat_max, axis=1)
min_fiyat = price_yesterday.apply(fiyat_min, axis=1)
price_yesterday["+EDF"] = round((min_fiyat * 0.97),2)
price_yesterday["-EDF"] = round((max_fiyat * 1.03),2)
price_yesterday= saat_sutunu_ekle(price_yesterday)

price_today_usd = change_currency("USD",price_today)
price_today_eur = change_currency("EUR",price_today)

price_tomorrow_usd = change_currency("USD",price_tomorrow)
price_tomorrow_eur = change_currency("EUR",price_tomorrow)

price_yesterday_usd = change_currency("USD",price_yesterday)
price_yesterday_eur = change_currency("EUR",price_yesterday)



df = pd.DataFrame(columns=['Saat', 'PTF (D+1)',"PTF (D)","PTF (D-1)","SMF (D-1)"])
df["Saat"] = price_yesterday["Saat"]
df["PTF (D+1)"] = price_tomorrow["PTF"]
df["PTF (D)"] = price_today["PTF"]
df["PTF (D-1)"] = price_yesterday["PTF"]
df["SMF (D-1)"] = price_yesterday["SMF"]
df_avg = df.mean().to_frame().T
df_avg = df_avg.rename(columns={"Saat": 'AOF'})
df_avg["AOF"] = ""
df_avg = df_avg.round(2)



df_usd = pd.DataFrame(columns=['Saat', 'PTF (D+1)',"PTF (D)","PTF (D-1)","SMF (D-1)"])
df_usd["Saat"] = price_yesterday_usd["Saat"]
df_usd["PTF (D+1)"] = price_tomorrow_usd["PTF"]
df_usd["PTF (D)"] = price_today_usd["PTF"]
df_usd["PTF (D-1)"] = price_yesterday_usd["PTF"]
df_usd["SMF (D-1)"] = price_yesterday_usd["SMF"]

df_avg_usd = df_usd.mean().to_frame().T
df_avg_usd = df_avg_usd.rename(columns={"Saat": 'AOF'})
df_avg_usd["AOF"] = ""
df_avg_usd = df_avg_usd.round(2)

df_eur = pd.DataFrame(columns=['Saat', 'PTF (D+1)',"PTF (D)","PTF (D-1)","SMF (D-1)"])
df_eur["Saat"] = price_yesterday_eur["Saat"]
df_eur["PTF (D+1)"] = price_tomorrow_eur["PTF"]
df_eur["PTF (D)"] = price_today_eur["PTF"]
df_eur["PTF (D-1)"] = price_yesterday_eur["PTF"]
df_eur["SMF (D-1)"] = price_yesterday_eur["SMF"]
df_avg_eur = df_eur.mean().to_frame().T
df_avg_eur = df_avg_eur.rename(columns={"Saat": 'AOF'})
df_avg_eur["AOF"] = ""
df_avg_eur = df_avg_eur.round(2)

#add new row to AOF column
df_avg.loc[-1] = ["TL",df_avg["PTF (D+1)"],df_avg["PTF (D)"],df_avg["PTF (D-1)"],df_avg["SMF (D-1)"]]
df_avg.index = df_avg.index + 1  # shifting index
df_avg.loc[-1] = ["USD",df_avg_usd["PTF (D+1)"],df_avg_usd["PTF (D)"],df_avg_usd["PTF (D-1)"],df_avg_usd["SMF (D-1)"]]
df_avg.index = df_avg.index + 1  # shifting index
df_avg.loc[-1] = ["EUR",df_avg_eur["PTF (D+1)"],df_avg_eur["PTF (D)"],df_avg_eur["PTF (D-1)"],df_avg_eur["SMF (D-1)"]]
df_avg.sort_index(inplace=True)
df_avg = df_avg[:-1]
df_avg = df_avg.iloc[::-1]

df_avg["PTF (D+1)"] = df_avg["PTF (D+1)"].astype(float)
df_avg["PTF (D)"] = df_avg["PTF (D)"].astype(float)
df_avg["PTF (D-1)"] = df_avg["PTF (D-1)"].astype(float)
df_avg["SMF (D-1)"] = df_avg["SMF (D-1)"].astype(float)



table = dbc.Table.from_dataframe(df, 
                             striped=True, 
                             bordered=True, 
                             hover=True,
                             responsive=True,
                             size = 'sm')

table_new = dash_table.DataTable(
        df.to_dict('records'),
    
    [
        dict(id = "Saat", name = "Saat" , type = "numeric", format = Format() ),
        dict(id = "PTF (D+1)", name = "PTF (D+1)" , type = "numeric", format = Format().group(True)),
        dict(id = "PTF (D)", name = "PTF (D)" , type = "numeric", format = Format().group(True)),
        dict(id = "PTF (D-1)", name = "PTF (D-1)" , type = "numeric", format = Format().group(True)),
        dict(id = "SMF (D-1)", name = "SMF (D-1)" , type = "numeric", format = Format().group(True)),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        }
        ]

    )

table_avg = dbc.Table.from_dataframe(df_avg,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_avg_new = dash_table.DataTable(
        df_avg.to_dict('records'),
    
    [
        dict(id = "AOF", name = "AOF" , type = "text"),
        dict(id = "PTF (D+1)", name = "PTF (D+1)" , type = "numeric", format = Format().group(True)),
        dict(id = "PTF (D)", name = "PTF (D)" , type = "numeric", format = Format().group(True)),
        dict(id = "PTF (D-1)", name = "PTF (D-1)" , type = "numeric", format = Format().group(True)),
        dict(id = "SMF (D-1)", name = "SMF (D-1)" , type = "numeric", format = Format().group(True)),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        }
        ]

    )

table_usd = dbc.Table.from_dataframe(df_usd,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_avg_usd = dbc.Table.from_dataframe(df_avg_usd,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_eur = dbc.Table.from_dataframe(df_eur,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_avg_eur = dbc.Table.from_dataframe(df_avg_eur,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm',
                                    style = {"color":"red"})



ptf_fig = px.line(df, x="Saat", y=["PTF (D-1)","PTF (D)","PTF (D+1)"], 
                  title='PTF Karşılaştırması',
                  labels={"value": "PTF", "variable":"Veri"},
                  template="plotly_white",
                  orientation="v",
                  range_x=[0,23],)
ptf_smf_fig = px.line(df, x="Saat", y=["PTF (D-1)","SMF (D-1)"], 
                      title='PTF SMF Karşılaştırması (D-1)',
                      labels={"value": "PTF", "variable":"Veri"},
                      template="plotly_white",
                      range_x=[0,23],
                      )

month_to_date = ptf(first_day_of_the_month, today)
month_to_date_last_year = ptf(first_day_of_the_month_last_year, today_last_year)
year_to_date = ptf(first_day_of_the_year, today)
year_to_date_last_year = ptf(first_day_of_the_year_last_year, today_last_year)

month_to_date = month_to_date.reset_index(drop=True)
month_to_date_last_year = month_to_date_last_year.reset_index(drop=True)
year_to_date = year_to_date.reset_index(drop=True)
year_to_date_last_year = year_to_date_last_year.reset_index(drop=True)



price_date_summary = pd.DataFrame(columns = ["Ortalama PTF","2023 PTF (TL)","2023 PTF (EUR)","2023 PTF (USD)",
                                             "2022 PTF (TL)","2022 PTF (EUR)","2022 PTF (USD)",
                                             "TL Değişim(%)","EUR Değişim(%)","USD Değişim(%)"])

price_date_summary["Ortalama PTF"] = ["Month to Date","Year to Date"]
price_date_summary["2023 PTF (TL)"] = [month_to_date["Fiyat (TL)"].mean(),year_to_date["Fiyat (TL)"].mean()]
price_date_summary["2023 PTF (EUR)"] = [month_to_date["Fiyat (EUR)"].mean(),year_to_date["Fiyat (EUR)"].mean()]
price_date_summary["2023 PTF (USD)"] = [month_to_date["Fiyat (USD)"].mean(),year_to_date["Fiyat (USD)"].mean()]
price_date_summary["2022 PTF (TL)"] = [month_to_date_last_year["Fiyat (TL)"].mean(),year_to_date_last_year["Fiyat (TL)"].mean()]
price_date_summary["2022 PTF (EUR)"] = [month_to_date_last_year["Fiyat (EUR)"].mean(),year_to_date_last_year["Fiyat (EUR)"].mean()]
price_date_summary["2022 PTF (USD)"] = [month_to_date_last_year["Fiyat (USD)"].mean(),year_to_date_last_year["Fiyat (USD)"].mean()]
price_date_summary["TL Değişim(%)"] = (price_date_summary["2023 PTF (TL)"][0]-price_date_summary["2022 PTF (TL)"][0]) / (price_date_summary["2023 PTF (TL)"])*100
price_date_summary["EUR Değişim(%)"] = (price_date_summary["2023 PTF (EUR)"][0]-price_date_summary["2022 PTF (EUR)"][0]) / (price_date_summary["2023 PTF (EUR)"])*100
price_date_summary["USD Değişim(%)"] = (price_date_summary["2023 PTF (USD)"][0]-price_date_summary["2022 PTF (USD)"][0]) / (price_date_summary["2023 PTF (USD)"])*100

price_date_summary = price_date_summary.round(2)

table_price_date_summary = dash_table.DataTable(
        price_date_summary.to_dict('records'),
    
    [
        dict(id = "Ortalama PTF", name = "Ortalama PTF" , type = "text"),
        dict(id = "2023 PTF (TL)", name = "2023 PTF (TL)" , type = "numeric", format = Format().group(True)),
        dict(id = "2023 PTF (EUR)", name = "2023 PTF (EUR)" , type = "numeric", format = Format().group(True)),
        dict(id = "2023 PTF (USD)", name = "2023 PTF (USD)" , type = "numeric", format = Format().group(True)),
        dict(id = "2022 PTF (TL)", name = "2022 PTF (TL)" , type = "numeric", format = Format().group(True)),
        dict(id = "2022 PTF (EUR)", name = "2022 PTF (EUR)" , type = "numeric", format = Format().group(True)),
        dict(id = "2022 PTF (USD)", name = "2022 PTF (USD)" , type = "numeric", format = Format().group(True)),
        dict(id = "TL Değişim(%)", name = "TL Değişim(%)" , type = "numeric", format = Format().group(True)),
        dict(id = "EUR Değişim(%)", name = "EUR Değişim(%)" , type = "numeric", format = Format().group(True)),
        dict(id = "USD Değişim(%)", name = "USD Değişim(%)" , type = "numeric", format = Format().group(True)),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        }
        ]

    )


#######################################################

load_yesterday = get_load_forecast(yesterday, yesterday)
load_today = get_load_forecast(today, today)
load_tomorrow = get_load_forecast(tomorrow, tomorrow)

load_yesterday = load_yesterday.reset_index(drop=True)
load_today = load_today.reset_index(drop=True)
load_tomorrow = load_tomorrow.reset_index(drop=True)

df_load = pd.DataFrame(columns=['Saat', 'Yük Tahmini (D-1)',"Yük Tahmini (D)","Yük Tahmini (D+1)"])
df_load["Saat"] = load_yesterday["Saat"]
df_load["Yük Tahmini (D-1)"] = load_yesterday["Yük Tahmini"]
df_load["Yük Tahmini (D)"] = load_today["Yük Tahmini"]
df_load["Yük Tahmini (D+1)"] = load_tomorrow["Yük Tahmini"]

load_fig = px.line(df_load, x="Saat", y=["Yük Tahmini (D-1)","Yük Tahmini (D)","Yük Tahmini (D+1)"],
                   title='Yük Tahmini Karşılaştırması',
                   labels={"value": "Yük Tahmini", "variable":"Veri"},
                   template="plotly_white")

yesterday_production = kgup(yesterday, yesterday)
today_production = kgup(today, today)
tomorrow_production = kgup(tomorrow, tomorrow)

yesterday_production = yesterday_production.reset_index(drop=True)
today_production = today_production.reset_index(drop=True)
tomorrow_production = tomorrow_production.reset_index(drop=True)

df_production_fb = pd.DataFrame(columns=['Saat', 'Üretim (D-1)',"Üretim (D)","Üretim (D+1)"])
df_production_fb["Saat"] = saat
df_production_fb["Üretim (D-1)"] = yesterday_production["Akarsu"] + yesterday_production["Ruzgar"]  + yesterday_production["Jeotermal"] + yesterday_production["Biokutle"]
df_production_fb["Üretim (D)"] = today_production["Akarsu"] + today_production["Ruzgar"]  + today_production["Jeotermal"] + today_production["Biokutle"]
df_production_fb["Üretim (D+1)"] = tomorrow_production["Akarsu"] + tomorrow_production["Ruzgar"]  + tomorrow_production["Jeotermal"] + tomorrow_production["Biokutle"]

production_fb_fig = px.line(df_production_fb, x="Saat", y=["Üretim (D-1)","Üretim (D)","Üretim (D+1)"],
                            title='Fiyat Bağımsız Yenilenebilir Enerji Üretim Karşılaştırması',
                            labels={"value": "Üretim", "variable":"Veri"},
                            template="plotly_white")

yesterday_euas_sell = get_euas_bilateral_sell_quantity(yesterday, yesterday)
today_euas_sell = get_euas_bilateral_sell_quantity(today, today)
tomorrow_euas_sell = get_euas_bilateral_sell_quantity(tomorrow, tomorrow)

yesterday_euas_sell = yesterday_euas_sell.reset_index(drop=True)
today_euas_sell = today_euas_sell.reset_index(drop=True)
tomorrow_euas_sell = tomorrow_euas_sell.reset_index(drop=True)

df_euas_sell = pd.DataFrame(columns=['Saat', 'İA Satış (D-1)',"İA Satış (D)","İA Satış (D+1)"])
df_euas_sell["Saat"] = saat
df_euas_sell["İA Satış (D-1)"] = yesterday_euas_sell["İA Satış Miktarı"]
df_euas_sell["İA Satış (D)"] = today_euas_sell["İA Satış Miktarı"]
df_euas_sell["İA Satış (D+1)"] = tomorrow_euas_sell["İA Satış Miktarı"]



euas_sell_fig = px.line(df_euas_sell, x="Saat", y=["İA Satış (D-1)","İA Satış (D)","İA Satış (D+1)"],
                            title='EUAS İkili Anlaşma Satış Karşılaştırması',
                            labels={"value": "İA Satış Miktarı", "variable":"Veri"},
                            template="plotly_white")

coal_kgup = pd.DataFrame(columns=['Saat', 'Kömür KGUP'])
coal_kgup['Saat'] = yesterday_production['Saat']
coal_kgup['Kömür KGUP (D-1)'] = yesterday_production["Ithalkomur"] + yesterday_production["Linyit"]
coal_kgup['Kömür KGUP (D)'] = today_production["Ithalkomur"] + today_production["Linyit"]
coal_kgup['Kömür KGUP (D+1)'] = tomorrow_production["Ithalkomur"] + tomorrow_production["Linyit"]

coal_kgup_fig = px.line(coal_kgup, x="Saat", y=["Kömür KGUP (D-1)","Kömür KGUP (D)","Kömür KGUP (D+1)"],
                            title='Yerli ve İthal Kömür Üretim Karşılaştırması',
                            labels={"value": "Kömür Üretim", "variable":"Veri"},
                            template="plotly_white")



df_kalan_yük = pd.DataFrame(columns=['Saat', 'Kalan Yük (D-1)',"Kalan Yük (D)","Kalan Yük (D+1)"])
df_kalan_yük["Saat"] = saat
df_kalan_yük["Kalan Yük (D-1)"] = df_load["Yük Tahmini (D-1)"] - df_production_fb["Üretim (D-1)"] - df_euas_sell["İA Satış (D-1)"]
df_kalan_yük["Kalan Yük (D)"] = df_load["Yük Tahmini (D)"] - df_production_fb["Üretim (D)"] - df_euas_sell["İA Satış (D)"]
df_kalan_yük["Kalan Yük (D+1)"] = df_load["Yük Tahmini (D+1)"] - df_production_fb["Üretim (D+1)"] - df_euas_sell["İA Satış (D+1)"]

kalan_yük_fig = px.line(df_kalan_yük, x="Saat", y=["Kalan Yük (D-1)","Kalan Yük (D)","Kalan Yük (D+1)"],
                        title='Kalan Yük Karşılaştırması',
                        labels={"value": "Kalan Yük", "variable":"Veri"},
                        template="plotly_white")
##############################################################################

yesterday_order = get_order(yesterday, yesterday)
yesterday_order = yesterday_order.reset_index(drop=True)

df_dgp = pd.DataFrame(columns=['Saat', 'PTF',"SMF","+EDMal","-EDMal","Net Talimat Hacmi"])
df_dgp["Saat"] = saat
df_dgp["PTF"] = price_yesterday["PTF"]
#smf her koşulda virgülden sonra 2 hane. Eğer tam sayı ise virgülden sonra 2 sıfır olmalı
df_dgp["SMF"] = price_yesterday["SMF"]
#smf virgülden sonra 2 hane

df_dgp["+EDMal"] = round(price_yesterday["PTF"] - price_yesterday["+EDF"],2)
df_dgp["-EDMal"] = round(price_yesterday["-EDF"] - price_yesterday["PTF"],2)


df_dgp["Net Talimat Hacmi"] = yesterday_order["Net Talimat"].astype(str) + yesterday_order["Net Talimat"].apply(lambda x: "🟢" if x < 0 else "🟡" if x == 0 else "🔴")

table_dgp = dbc.Table.from_dataframe(df_dgp,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_dgp_new = dash_table.DataTable(
        df_dgp.to_dict('records'),
    
    [
        dict(id = "Saat", name = "Saat" , type = "numeric", format = Format() ),
        dict(id = "PTF", name = "PTF" , type = "numeric", format = Format().group(True)),
        dict(id = "SMF", name = "SMF" , type = "numeric", format = Format().group(True)),
        dict(id = "+EDMal", name = "+EDMal" , type = "numeric", format = Format().group(True)),
        dict(id = "-EDMal", name = "-EDMal" , type = "numeric", format = Format().group(True)),
        dict(id = "Net Talimat Hacmi", name = "Net Talimat Hacmi" , type = "text"),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        }
        ]

    )

edmal_fig = px.bar(df_dgp, x="Saat", y=["+EDMal","-EDMal"],
                     title='Dengesizlik Maliyeti Karşılaştırması',
                     labels={"value": "EDMal", "variable":"Veri"},
                     template="plotly_white",
                     barmode="group",
                     color_discrete_sequence=["#285A84","#E13915"])

# Makas = PTF-SMF. Create line blot for Makas and add Net Talimat Hacmi as box plot
df_makas = pd.DataFrame(columns=['Saat', 'Makas',"Net Talimat Hacmi"])
df_makas["Saat"] = saat
df_makas["Makas"] = round(price_yesterday["PTF"] - price_yesterday["SMF"],2)
df_makas["Net Talimat Hacmi"] = yesterday_order["Net Talimat"]

#net talimat hacmi sıfırdan küçükse "green", sıfırdan büyükse "red" yazacak color sütunu ekle

makas_fig = px.line(df_makas, x="Saat", y=["Makas"],
                        title='Talimat Hacmine göre PTF-SMF Makası',
                        labels={"value": "PTF-SMF", "variable":"Veri"},
                        template="plotly_white",
                        color_discrete_sequence=["#285A84","#E13915"],
                        )
makas_fig.add_bar(x=df_makas["Saat"], y=df_makas["Net Talimat Hacmi"], name="Net Talimat Hacmi",marker_color="#E13915")



production_T = get_real_time_production_transposed(yesterday, yesterday)

table_production_T = dash_table.DataTable(
        production_T.to_dict('records'),
    
    [
        dict(id = "Kaynak Tipi", name = "Kaynak Tipi" , type = "text", format = Format() ),
        dict(id = "Günlük Üretim", name = "Günlük Üretim" , type = "numeric", format = Format().group(True)),
        dict(id = "Saatlik Üretim", name = "Saatlik Üretim" , type = "numeric", format = Format().group(True)),
        dict(id = "Üretimdeki Pay", name = "Üretimdeki Pay" , type = "numeric", format = Format().group(True)),
        dict(id = "Kurulu Güç", name = "Kurulu Güç" , type = "numeric", format = Format().group(True)),
        dict(id = "Kapasite Faktörü", name = "Kapasite Faktörü" , type = "numeric", format = Format().group(True)),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        }
        ]

    )

# Termik = Doğal Gaz,Linyit,İthal Kömür,Diğer. Yenilenebilir = Rüzgar,Güneş,Barajlı,Akarsu,Biyokütle,Jeotermal. Create pie chart
# Create pie chart
labels = ["Termik", "Yenilenebilir"]
values = [production_T["Günlük Üretim"][0], production_T["Günlük Üretim"][1]]
colors = ['#285A84', '#E13915']

production_T_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
production_T_pie.update_traces(marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
production_T_pie.update_layout(title_text="Termik vs Yenilenebilir",title_x=0.3,template="plotly_white")


#####################################################

ptf_2023 = ptf("2023-01-01",today)
ptf_2023 = ptf_2023.set_index("Tarih")
ptf_2023_m = ptf_2023.groupby(pd.Grouper(freq="M")).mean()
ptf_2023_m = ptf_2023_m.reset_index()

ptf_2022 = ptf("2022-01-01","2022-12-31")
ptf_2022 = ptf_2022.set_index("Tarih")
ptf_2022_m = ptf_2022.groupby(pd.Grouper(freq="M")).mean()
ptf_2022_m = ptf_2022_m.reset_index()

ptf_2021 = ptf("2021-01-01","2021-12-31")
ptf_2021 = ptf_2021.set_index("Tarih")
ptf_2021_m = ptf_2021.groupby(pd.Grouper(freq="M")).mean()
ptf_2021_m = ptf_2021_m.reset_index()

yearly_price = pd.DataFrame( columns=["Ay","2021 (TL)","2022 (TL)","2023 (TL)","2021 (USD)","2022 (USD)","2023 (USD)"])
yearly_price["Ay"] = ptf_2021_m.index + 1
yearly_price["2021 (TL)"] = ptf_2021_m["Fiyat (TL)"]
yearly_price["2022 (TL)"] = ptf_2022_m["Fiyat (TL)"]
yearly_price["2023 (TL)"] = ptf_2023_m["Fiyat (TL)"]
yearly_price["2021 (USD)"] = ptf_2021_m["Fiyat (USD)"]
yearly_price["2022 (USD)"] = ptf_2022_m["Fiyat (USD)"]
yearly_price["2023 (USD)"] = ptf_2023_m["Fiyat (USD)"]

yearly_price_fig = px.line(yearly_price, x="Ay", y=["2021 (TL)","2022 (TL)","2023 (TL)"],
                            title='Yıllara Göre Fiyat Karşılaştırması (TL)',
                            labels={"value": "PTF", "variable":"Veri"},
                            template="plotly_white")

yearly_price_usd_fig = px.line(yearly_price, x="Ay", y=["2021 (USD)","2022 (USD)","2023 (USD)"],
                            title='Yıllara Göre Fiyat Karşılaştırması (USD)',
                            labels={"value": "PTF", "variable":"Veri"},
                            template="plotly_white")

cons_2023 = get_real_time_consumption("2023-01-01",today)
cons_2023_m = cons_2023.groupby(pd.Grouper(freq="M")).mean()

cons_2022 = get_real_time_consumption("2022-01-01","2022-12-31")
cons_2022_m = cons_2022.groupby(pd.Grouper(freq="M")).mean()

cons_2021 = get_real_time_consumption("2021-01-01","2021-12-31")
cons_2021_m = cons_2021.groupby(pd.Grouper(freq="M")).mean()

yearly_cons = pd.DataFrame( columns=["Ay","2021","2022","2023"])
yearly_cons["Ay"] = cons_2021_m.index.month

cons_2021_m = cons_2021_m.reset_index(drop=True)
cons_2022_m = cons_2022_m.reset_index(drop=True)
cons_2023_m = cons_2023_m.reset_index(drop=True)

yearly_cons["2021"] = cons_2021_m["Tüketim"]
yearly_cons["2022"] = cons_2022_m["Tüketim"]
yearly_cons["2023"] = cons_2023_m["Tüketim"]

#drop last row
yearly_cons = yearly_cons[:-1]

yearly_cons_fig = px.line(yearly_cons, x="Ay", y=["2021","2022","2023"],
                            title='Yıllara Göre Tüketim Karşılaştırması',
                            labels={"value": "Tüketim", "variable":"Veri"},
                            template="plotly_white")

price_2021 = ptf_smf("2021-01-01", "2021-12-31")
price_2022 = ptf_smf("2022-01-01", "2022-12-31")
price_2023 = ptf_smf("2023-01-01", today)


price_2021["Tarih"] = pd.to_datetime(price_2021["Tarih"])

max_fiyat = price_2021.apply(fiyat_max, axis=1)
min_fiyat = price_2021.apply(fiyat_min, axis=1)
price_2021["+EDF"] = round((min_fiyat * 0.97),2)
price_2021["-EDF"] = round((max_fiyat * 1.03),2)
price_2021["+EDMal"] = round(price_2021["PTF"] - price_2021["+EDF"],2)
price_2021["-EDMal"] = round(price_2021["-EDF"] - price_2021["PTF"],2)

#Aylık ortalamalar
price_2021["Ay"] = price_2021["Tarih"].dt.month
price_2021_aylik = price_2021.groupby("Ay").mean()
price_2021_aylik = price_2021_aylik.reset_index()


price_2022["Tarih"] = pd.to_datetime(price_2022["Tarih"])
max_fiyat = price_2022.apply(fiyat_max, axis=1)
min_fiyat = price_2022.apply(fiyat_min, axis=1)
price_2022["+EDF"] = round((min_fiyat * 0.97),2)
price_2022["-EDF"] = round((max_fiyat * 1.03),2)
price_2022["+EDMal"] = round(price_2022["PTF"] - price_2022["+EDF"],2)
price_2022["-EDMal"] = round(price_2022["-EDF"] - price_2022["PTF"],2)

price_2022["Ay"] = price_2022["Tarih"].dt.month
price_2022_aylik = price_2022.groupby("Ay").mean()
price_2022_aylik = price_2022_aylik.reset_index()


price_2023["Tarih"] = pd.to_datetime(price_2023["Tarih"])
max_fiyat = price_2023.apply(fiyat_max, axis=1)
min_fiyat = price_2023.apply(fiyat_min, axis=1)
price_2023["+EDF"] = round((min_fiyat * 0.97),2)
price_2023["-EDF"] = round((max_fiyat * 1.03),2)
price_2023["+EDMal"] = round(price_2023["PTF"] - price_2023["+EDF"],2)
price_2023["-EDMal"] = round(price_2023["-EDF"] - price_2023["PTF"],2)

price_2023["Ay"] = price_2023["Tarih"].dt.month
price_2023_aylik = price_2023.groupby("Ay").mean()
price_2023_aylik = price_2023_aylik.reset_index()



yearly_price = pd.DataFrame(columns=["Ay","2021 PTF", "2022 PTF", "2023 PTF","2021 +EDMal", "2022 +EDMal", "2023 +EDMal", "2021 -EDMal", "2022 -EDMal", "2023 -EDMal"])
yearly_price["Ay"] = price_2021_aylik["Ay"]
yearly_price["2021 PTF"] = price_2021_aylik["PTF"]
yearly_price["2022 PTF"] = price_2022_aylik["PTF"]
yearly_price["2023 PTF"] = price_2023_aylik["PTF"]
yearly_price["2021 +EDMal"] = price_2021_aylik["+EDMal"]
yearly_price["2022 +EDMal"] = price_2022_aylik["+EDMal"]
yearly_price["2023 +EDMal"] = price_2023_aylik["+EDMal"]
yearly_price["2021 -EDMal"] = price_2021_aylik["-EDMal"]
yearly_price["2022 -EDMal"] = price_2022_aylik["-EDMal"]
yearly_price["2023 -EDMal"] = price_2023_aylik["-EDMal"]
yearly_price["2021 +EDMal/PTF"] = round(yearly_price["2021 +EDMal"] / yearly_price["2021 PTF"],2)
yearly_price["2022 +EDMal/PTF"] = round(yearly_price["2022 +EDMal"] / yearly_price["2022 PTF"],2)
yearly_price["2023 +EDMal/PTF"] = round(yearly_price["2023 +EDMal"] / yearly_price["2023 PTF"],2)
yearly_price["2021 -EDMal/PTF"] = round(yearly_price["2021 -EDMal"] / yearly_price["2021 PTF"],2)
yearly_price["2022 -EDMal/PTF"] = round(yearly_price["2022 -EDMal"] / yearly_price["2022 PTF"],2)
yearly_price["2023 -EDMal/PTF"] = round(yearly_price["2023 -EDMal"] / yearly_price["2023 PTF"],2)


yearly_positive_edmal_fig = px.line(yearly_price, x="Ay", y=["2021 +EDMal","2022 +EDMal","2023 +EDMal"],
                            title='Yıllara Göre +EDMal Karşılaştırması',
                            labels={"value": "+EDMal", "variable":"Veri"},
                            template="plotly_white")

yearly_negative_edmal_fig = px.line(yearly_price, x="Ay", y=["2021 -EDMal","2022 -EDMal","2023 -EDMal"],
                            title='Yıllara Göre -EDMal Karşılaştırması',
                            labels={"value": "-EDMal", "variable":"Veri"},
                            template="plotly_white")

# aylık  ortalama +edmal/ptf grafiği
yearly_positive_edmal_ptf_fig = px.line(yearly_price, x="Ay", y=["2021 +EDMal/PTF","2022 +EDMal/PTF","2023 +EDMal/PTF"],
                            title='Yıllara Göre +EDMal/PTF Karşılaştırması',
                            labels={"value": "+EDMal/PTF", "variable":"Veri"},
                            template="plotly_white")

# aylık  ortalama -edmal/ptf grafiği
yearly_negative_edmal_ptf_fig = px.line(yearly_price, x="Ay", y=["2021 -EDMal/PTF","2022 -EDMal/PTF","2023 -EDMal/PTF"],
                            title='Yıllara Göre -EDMal/PTF Karşılaştırması',
                            labels={"value": "-EDMal/PTF", "variable":"Veri"},
                            template="plotly_white")

# Akarsu Kapasite Faktörü

akarsu_kf_2021 = get_river_capacity_factor("2021-01-01","2021-12-31")
akarsu_kf_2022 = get_river_capacity_factor("2022-01-01","2022-12-31")
akarsu_kf_2023 = get_river_capacity_factor("2023-01-01",today)

akarsu_kf = pd.DataFrame(columns=["Ay","2021","2022","2023"])
akarsu_kf_2021 = akarsu_kf_2021.set_index("Tarih")
akarsu_kf["Ay"] = akarsu_kf_2021.index
akarsu_kf_2021 = akarsu_kf_2021.reset_index(drop=True)
akarsu_kf_2022 = akarsu_kf_2022.reset_index(drop=True)
akarsu_kf_2023 = akarsu_kf_2023.reset_index(drop=True)
akarsu_kf["2021"] = akarsu_kf_2021["Kapasite Faktörü"]
akarsu_kf["2022"] = akarsu_kf_2022["Kapasite Faktörü"]
akarsu_kf["2023"] = akarsu_kf_2023["Kapasite Faktörü"]

akarsu_kf

akarsu_kf_fig = px.line(akarsu_kf, x="Ay", y=["2021","2022","2023"],
                            title='Yıllara Göre Akarsu Kapasite Faktörü Karşılaştırması',
                            labels={"value": "Kapasite Faktörü", "variable":"Veri"},
                            template="plotly_white")



#####################################################
fiyat = html.Div([
                    html.Div(style={"width":"100vw","height":"100px","background-color":"#285A84","position":"relative","top":"-30px"}),
                    html.H3("Fiyat Raporu",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="fiyat")

yük = html.Div([    
                    html.Div(style={"width":"100vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("Üretim ve Talep Raporu",style={"color":"#285A84",
                                                 "position":"relative",})
                ],id="load")

dgp = html.Div([
                    html.Div(style={"width":"100vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("DGP ve GİP Raporu",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="dgp")

yıllık = html.Div([
                    html.Div(style={"width":"100vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("Yıllık Raporlar",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="yıllık")

nav_contents = [
    html.Ul(
        [   
            html.Li(html.A(
                        html.Img(src="https://www.gainenerji.com/wp-content/uploads/2022/10/gain-20-web.png",
                                 style={"width":"45%","height":"auto"},
                                 ),href="https://www.gainenerji.com/",target="_blank"
                        ),
                        style={"display":"inline-block",
                               "float":"left"}),
                               
            html.Li("Rapor Tarihi: " + rapor_tarihi,
                                    style={"display":"inline-block",
                                            "margin-top":"10px",
                                            "margin-right":"20px",
                                            "color":"black",
                                            "text-decoration":"none",
                                            "float":"left"},
                                            ),

            html.Li(html.A("Yıllık Raporlar", href="#yıllık",
                                    style={"display":"block",
                                            "padding":"8px 30px",
                                            "margin-top":"4px",
                                            "background-color":"white",
                                            "color":"#285A84",
                                            "text-decoration":"none",
                                            "border-radius":"5px",}),
                                            style={"display":"inline-block",
                                                    "margin-right":"40px",
                                                    "float":"right",
                                                    "font-size":"16px"}
                                            ),

            html.Li(html.A("DGP ve GİP Raporu", href="#dgp",
                           style={"display":"block",
                                  "padding":"8px 30px",
                                  "margin-top":"4px",
                                  "background-color":"white",
                                  "color":"#285A84",
                                  "text-decoration":"none",
                                  "border-radius":"5px",
                                  }),
                                  style={"display":"inline-block",
                                         "margin-right":"5px",
                                         "float":"right",
                                         "font-size":"16px"}
                                  ),
            html.Li(html.A("Üretim ve Talep Raporu", href="#load",
                           style={"display":"block",
                                  "padding":"8px 30px",
                                  "margin-top":"4px",
                                  "background-color":"white",
                                  "color":"#285A84",
                                  "text-decoration":"none",
                                  "border-radius":"5px",}),
                                  style={"display":"inline-block",
                                         "margin-right":"5px",
                                         "float":"right",
                                         "font-size":"16px"}
                                  ),
            html.Li(html.A("Fiyat Raporu", href="#fiyat",
                           style={"display":"block",
                                  "padding":"8px 30px",
                                  "margin-top":"4px",
                                  "background-color":"white",
                                  "color":"#285A84",
                                  "text-decoration":"none",
                                  "border-radius":"5px",}),
                                  style={"display":"inline-block",
                                         "margin-right":"5px",
                                         "float":"right",
                                         "font-size":"16px"}
                                  ),                      

        ],style={"list-style":"None",
                 "position":"fixed",
                 "top":"0","left":"0",
                 "z-index":"1",
                 "background-color":"white",
                 "width":"100vw",
                 "padding-left":"30px",
                 "padding-top":"20px",
                 "padding-bottom":"20px",
                 "bottom-border":"5px solid black",
                 "box-shadow":"0 0 10px 0 rgba(0,0,0,0.1)",
                 }
    )
]



app = Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.layout = dbc.Container(
    html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [   
                        html.Div(nav_contents)
                    ],
                width=8,),
            ],
            style={"margin-bottom":"10px", "margin-top":"25px"}
        ),

        dbc.Row(
            [
            dbc.Col(
                [
                    fiyat
                ]
                ),
            ],
        style={"margin-bottom":"10px","margin-top":"-30px",}
        ),

        dbc.Row(
            [
                dbc.Col(
                [
                    html.Div(
                        [
                            table_new,
                        ],
                        style={"margin-bottom":"10px"}
                        ),

                    html.Div(
                        [
                            table_avg_new,
                        ],
                        )
                ]),

            dbc.Col([dcc.Graph(figure = ptf_fig),dcc.Graph(figure=ptf_smf_fig)],width=8),
            
            ],
        ),

        dbc.Row(
            [
                dbc.Col([
                    table_price_date_summary
                ]),
                html.Hr(),
            ]

        ),

        dbc.Row(
            [
            dbc.Col(
                [
                yük
                ]
                )
            ],
        style={"margin-bottom":"10px","margin-top":"-100px"}
        ),

        dbc.Row(
            [
                dbc.Col(html.Div(
                [
                    dcc.Graph(figure = load_fig), dcc.Graph(figure = coal_kgup_fig)
                ]
                )),

                dbc.Col(html.Div(
                [
                    dcc.Graph(figure = production_fb_fig), dcc.Graph(figure = kalan_yük_fig)
                ]
                )),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([table_production_T])
                    ]
                ),

                dbc.Col(html.Div(
                    [
                        dcc.Graph(figure = production_T_pie)
                    ]),
                    width=6,
                ),
                html.Hr(),
            ],
            
            
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dgp
                    ],
                    width=4,
                ),
                
            ],
            style={"margin-bottom":"10px","margin-top":"-100px"}
        ),
        dbc.Row(
            [
              dbc.Col(
                [html.Div(
                        [
                          table_dgp_new
                        ],
                        style={"margin-bottom":"20px"}
                          ),
                ]
                
              ),

              dbc.Col(html.Div(
                    [
                        dcc.Graph(figure = edmal_fig), dcc.Graph(figure = makas_fig)
                    ]),
                    width=8,
                ),

             html.Hr()
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        yıllık
                    ],
                    width=4,
                ),
                
            ],
            style={"margin-bottom":"10px","margin-top":"-100px"}
        ),

        dbc.Row(
            [
              dbc.Col(
                [html.Div(
                        [
                          dcc.Graph(figure = yearly_price_fig), 
                          dcc.Graph(figure = yearly_cons_fig),
                          dcc.Graph(figure = yearly_positive_edmal_fig),
                          dcc.Graph(figure = yearly_positive_edmal_ptf_fig),
                          
                        ],
                        style={}
                          ),
                ]
                
              ),

                dbc.Col(html.Div(
                    [   
                        dcc.Graph(figure = akarsu_kf_fig),
                        dcc.Graph(figure = yearly_price_usd_fig),
                        dcc.Graph(figure = yearly_negative_edmal_fig),
                        dcc.Graph(figure = yearly_negative_edmal_ptf_fig)
                    ]),
                ),

             html.Hr()
            ]
        ),
    ])
)


if __name__ == '__main__':
    app.run(debug=True)