import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table,dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import dash_bootstrap_components as dbc
from functions import *
from dash import Input, Output, html
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

#hide warnings
import warnings
warnings.filterwarnings('ignore')

""" 

today = "2023-09-18"
yesterday = "2023-09-17"
tomorrow = "2023-09-19"

"""

"""

Green = #618264
Red =  #D80032
Yellow = #FFB000
Dark Blue = "#27374D"
Renewable Green = "#618264"
Gain Blue = #285A84
Gain Red = #E13915

"""
saat = pd.Series(range(0,24))
watermark_src = "https://lh3.googleusercontent.com/p/AF1QipOZB0N4E1nh2RqCcWemoZpPNCpZ6JwOc-HDzhRg=s1360-w1360-h1020"
if datetime.today().hour >= 17:
    today = datetime.today().strftime('%Y-%m-%d')
    print(today)
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    first_day_of_the_month = datetime.today().strftime('%Y-%m-01')
    first_day_of_the_year = datetime.today().strftime('%Y-01-01')
    first_day_of_the_month_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-01')
    first_day_of_the_year_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-01-01')
    today_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    rapor_tarihi = datetime.today().strftime("%d-%m-%Y")

    week_start_date = (datetime.today() - timedelta(days=datetime.today().weekday()))
    week_start_date = week_start_date - timedelta(days=28)
    week_end_date = (datetime.today() - timedelta(days=datetime.today().weekday())) - timedelta(days=1)
    week_start_date = week_start_date.strftime('%Y-%m-%d')
    week_end_date = week_end_date.strftime('%Y-%m-%d')

else:
    today = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    tomorrow = datetime.today().strftime('%Y-%m-%d')
    if datetime.today().day == 1:
        first_day_of_the_month = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-01')
    else:
        first_day_of_the_month = datetime.today().strftime('%Y-%m-01')
    first_day_of_the_year = datetime.today().strftime('%Y-01-01')
    first_day_of_the_month_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-01')
    first_day_of_the_year_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-01-01')
    today_last_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    rapor_tarihi = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")

    week_start_date = (datetime.today() - timedelta(days=datetime.today().weekday()))
    week_start_date = week_start_date - timedelta(days=28)
    week_end_date = (datetime.today() - timedelta(days=datetime.today().weekday())) - timedelta(days=1)
    week_start_date = week_start_date.strftime('%Y-%m-%d')
    week_end_date = week_end_date.strftime('%Y-%m-%d')

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



df = pd.DataFrame(columns=['Saat', 'PTF(D+1)',"PTF(D)","PTF(D-1)","SMF(D-1)"])
df["Saat"] = price_yesterday["Saat"]
df["PTF(D+1)"] = price_tomorrow["PTF"]
df["PTF(D)"] = price_today["PTF"]
df["PTF(D-1)"] = price_yesterday["PTF"]
df["SMF(D-1)"] = price_yesterday["SMF"]


df_display = df.copy()
df_display['PTF(D+1)'] = df['PTF(D+1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_display['PTF(D)'] = df['PTF(D)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_display['PTF(D-1)'] = df['PTF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_display['SMF(D-1)'] = df['SMF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))



df_avg = df.mean().to_frame().T
df_avg = df_avg.rename(columns={"Saat": 'Ortalama'})
df_avg["Ortalama"] = ""
df_avg = df_avg.round(2)


df_usd = pd.DataFrame(columns=['Saat', 'PTF(D+1)',"PTF(D)","PTF(D-1)","SMF(D-1)"])
df_usd["Saat"] = price_yesterday_usd["Saat"]
df_usd["PTF(D+1)"] = price_tomorrow_usd["PTF"]
df_usd["PTF(D)"] = price_today_usd["PTF"]
df_usd["PTF(D-1)"] = price_yesterday_usd["PTF"]
df_usd["SMF(D-1)"] = price_yesterday_usd["SMF"]


df_avg_usd = df_usd.mean().to_frame().T
df_avg_usd = df_avg_usd.rename(columns={"Saat": 'Ortalama'})
df_avg_usd["Ortalama"] = ""
df_avg_usd = df_avg_usd.round(2)

df_avg_usd_display = df_avg_usd.copy()
df_avg_usd_display['PTF(D+1)'] = df_avg_usd['PTF(D+1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_usd_display['PTF(D)'] = df_avg_usd['PTF(D)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_usd_display['PTF(D-1)'] = df_avg_usd['PTF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_usd_display['SMF(D-1)'] = df_avg_usd['SMF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))

df_eur = pd.DataFrame(columns=['Saat', 'PTF(D+1)',"PTF(D)","PTF(D-1)","SMF(D-1)"])
df_eur["Saat"] = price_yesterday_eur["Saat"]
df_eur["PTF(D+1)"] = price_tomorrow_eur["PTF"]
df_eur["PTF(D)"] = price_today_eur["PTF"]
df_eur["PTF(D-1)"] = price_yesterday_eur["PTF"]
df_eur["SMF(D-1)"] = price_yesterday_eur["SMF"]
df_avg_eur = df_eur.mean().to_frame().T
df_avg_eur = df_avg_eur.rename(columns={"Saat": 'Ortalama'})
df_avg_eur["Ortalama"] = ""
df_avg_eur = df_avg_eur.round(2)

df_avg_eur_display = df_avg_eur.copy()
df_avg_eur_display['PTF(D+1)'] = df_avg_eur['PTF(D+1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_eur_display['PTF(D)'] = df_avg_eur['PTF(D)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_eur_display['PTF(D-1)'] = df_avg_eur['PTF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_eur_display['SMF(D-1)'] = df_avg_eur['SMF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))


#add new row to ORT column
df_avg.loc[-1] = ["TL/MWh",df_avg["PTF(D+1)"],df_avg["PTF(D)"],df_avg["PTF(D-1)"],df_avg["SMF(D-1)"]]
df_avg.index = df_avg.index + 1  # shifting index
df_avg.loc[-1] = ["USD/MWh",df_avg_usd["PTF(D+1)"],df_avg_usd["PTF(D)"],df_avg_usd["PTF(D-1)"],df_avg_usd["SMF(D-1)"]]
df_avg.index = df_avg.index + 1  # shifting index
df_avg.loc[-1] = ["EUR/MWh",df_avg_eur["PTF(D+1)"],df_avg_eur["PTF(D)"],df_avg_eur["PTF(D-1)"],df_avg_eur["SMF(D-1)"]]
df_avg.sort_index(inplace=True)
df_avg = df_avg[:-1]
df_avg = df_avg.iloc[::-1]

df_avg["PTF(D+1)"] = df_avg["PTF(D+1)"].astype(float)
df_avg["PTF(D)"] = df_avg["PTF(D)"].astype(float)
df_avg["PTF(D-1)"] = df_avg["PTF(D-1)"].astype(float)
df_avg["SMF(D-1)"] = df_avg["SMF(D-1)"].astype(float)

df_avg["PTF(D+1)"] = df_avg["PTF(D+1)"]
df_avg["PTF(D)"] = df_avg["PTF(D)"]
df_avg["PTF(D-1)"] = df_avg["PTF(D-1)"]
df_avg["SMF(D-1)"] = df_avg["SMF(D-1)"]

df_avg_display = df_avg.copy()
df_avg_display['PTF(D+1)'] = df_avg['PTF(D+1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_display['PTF(D)'] = df_avg['PTF(D)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_display['PTF(D-1)'] = df_avg['PTF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_avg_display['SMF(D-1)'] = df_avg['SMF(D-1)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))



table_new = dash_table.DataTable(
        df_display.to_dict('records'),
    
    [
        dict(id = "Saat", name = "Saatlik PTF" , type = "numeric", format = Format() ),
        dict(id = "PTF(D+1)", name = "D+1" , type = "numeric", format = Format(precision =6).group(True)),
        dict(id = "PTF(D)", name = "D" , type = "numeric", format = Format(precision =6).group(True)),
        dict(id = "PTF(D-1)", name = "D-1" , type = "numeric", format = Format(precision =6).group(True)),
    ],

    style_as_list_view=True,
    style_table = {
        'overflowX': 'auto',

    },
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle'  # Dikeyde ortalama
    },

    style_cell={
        'height': 'auto',
        'whiteSpace': 'normal',
        'fontWeight': 'bold',
        "font":"16px Calibri",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',

        },
        {
            'if': {'column_id': 'Saat'},  # Sadece "A" sütunu için
            'fontWeight': 'bold'  # Kalın yap
        }
        ],

    style_data={
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle',  # Dikeyde ortalama
        "maxWidth":"40px",
        "width":"40px",
        "minWidth":"40px",
    }

    )

table_avg = dbc.Table.from_dataframe(df_avg,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_avg_new = dash_table.DataTable(
        df_avg_display.to_dict('records'),
    
    [
        dict(id = "Ortalama", name = "Ortalama PTF" , type = "text"),
        dict(id = "PTF(D+1)", name = "D+1" , type = "numeric", format = Format().group(True)),
        dict(id = "PTF(D)", name = "D" , type = "numeric", format = Format().group(True)),
        dict(id = "PTF(D-1)", name = "D-1" , type = "numeric", format = Format().group(True)),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
        "whiteSpace" : "normal",
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle',  # Dikeyde ortalama
        "width":"40px",
        "minWidth":"40px",
        "maxWidth":"40px",
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
        "whiteSpace" : "normal",

    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        }
        ],
    
    style_data={
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle',  # Dikeyde ortalama
        "maxWidth":"40px",
        "width":"40px",
        "minWidth":"40px",
    }

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



ptf_fig = px.line(df, x="Saat", y=["PTF(D-1)","PTF(D)","PTF(D+1)"], 
                  title='',
                  labels={"value": "PTF (TL/MWh)", "variable":""},
                  template="plotly_white",
                  orientation="v",
                  range_x=[0,23],)

ptf_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=800,
    height=475,
)

ptf_fig.update_xaxes(range=[0, 23], constrain='domain')
ptf_fig.update_xaxes(dtick=1)

#min value in df
min_value_ptf_fig = df.min().min()
max_value_ptf_fig = df.max().max()

ptf_fig.update_yaxes(range=[min_value_ptf_fig, max_value_ptf_fig+500], constrain='domain')
ptf_fig.update_yaxes(dtick=500)

ptf_fig.update_traces(name="D-1", selector=dict(name="PTF(D-1)"))
ptf_fig.update_traces(name="D", selector=dict(name="PTF(D)"))
ptf_fig.update_traces(name="D+1", selector=dict(name="PTF(D+1)"))

ptf_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=2.5, sizey=2.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))





month_to_date = ptf(first_day_of_the_month, today)
month_to_date_last_year = ptf(first_day_of_the_month_last_year, today_last_year)
year_to_date = ptf(first_day_of_the_year, today)
year_to_date_last_year = ptf(first_day_of_the_year_last_year, today_last_year)

month_to_date = month_to_date.reset_index(drop=True)
month_to_date_last_year = month_to_date_last_year.reset_index(drop=True)
year_to_date = year_to_date.reset_index(drop=True)
year_to_date_last_year = year_to_date_last_year.reset_index(drop=True)



price_date_summary = pd.DataFrame(columns = ["Ortalama PTF","2023 (TL)","2023 (EUR)","2023 (USD)",
                                             "2022 (TL)","2022 (EUR)","2022 (USD)",
                                             "TL Değişim","EUR Değişim","USD Değişim"])

price_date_summary["Ortalama PTF"] = ["Ay Başından Bugüne","Yıl Başından Bugüne"]
price_date_summary["2023 (TL/MWh)"] = [month_to_date["Fiyat (TL)"].mean(),year_to_date["Fiyat (TL)"].mean()]
price_date_summary["2023 (EUR/MWh)"] = [month_to_date["Fiyat (EUR)"].mean(),year_to_date["Fiyat (EUR)"].mean()]
price_date_summary["2023 (USD/MWh)"] = [month_to_date["Fiyat (USD)"].mean(),year_to_date["Fiyat (USD)"].mean()]
price_date_summary["2022 (TL/MWh)"] = [month_to_date_last_year["Fiyat (TL)"].mean(),year_to_date_last_year["Fiyat (TL)"].mean()]
price_date_summary["2022 (EUR/MWh)"] = [month_to_date_last_year["Fiyat (EUR)"].mean(),year_to_date_last_year["Fiyat (EUR)"].mean()]
price_date_summary["2022 (USD/MWh)"] = [month_to_date_last_year["Fiyat (USD)"].mean(),year_to_date_last_year["Fiyat (USD)"].mean()]
price_date_summary["TL Değişim"] = ((price_date_summary["2023 (TL/MWh)"]/price_date_summary["2022 (TL/MWh)"]) - 1) * 100
price_date_summary["EUR Değişim"] = ((price_date_summary["2023 (EUR/MWh)"]/price_date_summary["2022 (EUR/MWh)"]) - 1) * 100
price_date_summary["USD Değişim"] = ((price_date_summary["2023 (USD/MWh)"]/price_date_summary["2022 (USD/MWh)"]) - 1) * 100
price_date_summary = price_date_summary.round(2)

""" price_date_summary_display = price_date_summary.copy()
price_date_summary_display['2023 (TL/MWh)'] = price_date_summary['2023 (TL/MWh)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['2023 (EUR/MWh)'] = price_date_summary['2023 (EUR/MWh)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['2023 (USD/MWh)'] = price_date_summary['2023 (USD/MWh)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['2022 (TL/MWh)'] = price_date_summary['2022 (TL/MWh)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['2022 (EUR/MWh)'] = price_date_summary['2022 (EUR/MWh)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['2022 (USD/MWh)'] = price_date_summary['2022 (USD/MWh)'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['TL Değişim'] = price_date_summary['TL Değişim'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['EUR Değişim'] = price_date_summary['EUR Değişim'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
price_date_summary_display['USD Değişim'] = price_date_summary['USD Değişim'].apply(lambda x: f'{x:.2f}'.replace('.', ','))

price_date_summary_display['TL Değişim'] = price_date_summary_display['TL Değişim'].apply(lambda x: f"{x}%")
price_date_summary_display['EUR Değişim'] = price_date_summary_display['EUR Değişim'].apply(lambda x: f"{x}%")
price_date_summary_display['USD Değişim'] = price_date_summary_display['USD Değişim'].apply(lambda x: f"{x}%")



table_price_date_summary = dash_table.DataTable(
        price_date_summary_display.to_dict('records'),
    
    [
        dict(id = "Ortalama PTF", name = "Ortalama PTF" , type = "text"),
        dict(id = "2023 (TL/MWh)", name = "2023 TL/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "2023 (EUR/MWh)", name = "2023 EUR/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "2023 (USD/MWh)", name = "2023 USD/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "2022 (TL/MWh)", name = "2022 TL/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "2022 (EUR/MWh)", name = "2022 EUR/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "2022 (USD/MWh)", name = "2022 USD/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "TL Değişim", name = "Değişim TL/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "EUR Değişim", name = "Değişim EUR/MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "USD Değişim", name = "Değişim USD/MWh" , type = "numeric", format = Format().group(True)),
    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
        "whiteSpace" : "normal",
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle'  # Dikeyde ortalama
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
        "whiteSpace" : "normal",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        },
        {
            'if': {'column_id': 'Ortalama PTF'}, 
            "maxWidth":"100px",
            "width":"100px",
            "minWidth":"100px",
        }
        ],

    style_data={
    'text-align': 'center',  # Yatayda ortalama
    'vertical-align': 'middle',  # Dikeyde ortalama
    "maxWidth":"40px",
    "width":"40px",
    "minWidth":"40px",
    },

    ) """

#######################################################

tl_date_summary = pd.DataFrame(columns = ["Periyot","Fiyat","Yıl"])

tl_date_summary["Periyot"] = ["Ay Başından Bugüne","Yıl Başından Bugüne","Ay Başından Bugüne","Yıl Başından Bugüne"]
tl_date_summary["Fiyat"] = [month_to_date_last_year["Fiyat (TL)"].mean(),year_to_date_last_year["Fiyat (TL)"].mean(),month_to_date["Fiyat (TL)"].mean(),year_to_date["Fiyat (TL)"].mean()]
tl_date_summary["Yıl"] = ["2022","2022","2023","2023"]

usd_date_summary = pd.DataFrame(columns = ["Periyot","Fiyat","Yıl"])

usd_date_summary["Periyot"] = ["Ay Başından Bugüne","Yıl Başından Bugüne","Ay Başından Bugüne","Yıl Başından Bugüne"]
usd_date_summary["Fiyat"] = [month_to_date_last_year["Fiyat (USD)"].mean(),year_to_date_last_year["Fiyat (USD)"].mean(),month_to_date["Fiyat (USD)"].mean(),year_to_date["Fiyat (USD)"].mean()]
usd_date_summary["Yıl"] = ["2022","2022","2023","2023"]

değişim = [price_date_summary["TL Değişim"][0],price_date_summary["TL Değişim"][1],
              price_date_summary["USD Değişim"][0],price_date_summary["USD Değişim"][1]]

değişim = [f"{değişim[0]:.1f}%",f"{değişim[1]:.1f}%",f"{değişim[2]:.1f}%",f"{değişim[3]:.1f}%"]

fig_tl = px.bar(tl_date_summary, x='Periyot', y='Fiyat', color="Yıl", barmode='group',
                 labels={'Fiyat': 'Fiyat (TL/MWh)'},text="Fiyat",color_discrete_sequence=["#285A84","#E13915"])

fig_tl.update_traces(texttemplate='%{text:.2f}', textposition='inside')

# USD için bar grafiği
fig_usd = px.bar(usd_date_summary, x='Periyot', y='Fiyat', color="Yıl", barmode='group',
                  labels={'Fiyat': 'Fiyat (USD/MWh)'},text="Fiyat",color_discrete_sequence=["#285A84","#E13915"] )

fig_usd.update_traces(texttemplate='%{text:.2f}', textposition='inside')

# Subplot'ları oluştur (3 sütun ve 1 satır)
fig = make_subplots(rows=1, cols=2, shared_xaxes=False, horizontal_spacing=0.1,
                    subplot_titles=('PTF(TL/MWh)','PTF(USD/MWh)'))



# TL grafiğini ekle
for trace in fig_tl.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig_usd.data:
    trace.showlegend = False

# USD grafiğini ekle
for trace in fig_usd.data:
    fig.add_trace(trace, row=1, col=2)

# TL grafiği için
fig.add_annotation(
    x=tl_date_summary['Periyot'][2], 
    y=tl_date_summary['Fiyat'][2], # Biraz daha yukarıda yer alması için 10 ekledim
    text=f"<b>{değişim[0]}🡻</b>",
    showarrow=False,
    #bold
    font=dict(color="red", size=12),
    row=1, col=1,
    yshift=20,
    xshift=32
)

fig.add_annotation(
    x=tl_date_summary['Periyot'][3], 
    y=tl_date_summary['Fiyat'][3], # Biraz daha yukarıda yer alması için 10 ekledim
    text=f"<b>{değişim[1]}🡻</b>",
    showarrow=False,
    font=dict(color="red", size=12),
    row=1, col=1,
    yshift=20,
    xshift=32
)

fig.add_annotation(
    x=usd_date_summary['Periyot'][2], 
    y=usd_date_summary['Fiyat'][2], # Biraz daha yukarıda yer alması için 10 ekledim
    text=f"<b>{değişim[2]}🡻</b>",
    showarrow=False,
    font=dict(color="red", size=12),
    row=1, col=2,
    yshift=20,
    xshift=32
)

fig.add_annotation(
    x=usd_date_summary['Periyot'][3], 
    y=usd_date_summary['Fiyat'][3], # Biraz daha yukarıda yer alması için 10 ekledim
    text=f"<b>{değişim[3]}🡻</b>",
    showarrow=False,
    font=dict(color="red", size=12),
    row=1, col=2,
    yshift=20,
    xshift=32
)

# Grafiğin layout'ını güncelle
fig.update_layout(height=475, width=800, title_text="")

# Set y-axes range
fig.update_yaxes(range=[0, 4000], row=1, col=1)
fig.update_yaxes(dtick=1000, row=1, col=1)
fig.update_yaxes(range=[0, 300], row=1, col=2)
fig.update_yaxes(dtick=75, row=1, col=2)

#legend 
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
        
    ),



)

fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0,
    y=-0.30,
    text="<i><b>Ay Başından Bugüne</b>, içinden bulunduğumuz ayın ilk gününden; <b>Yıl Başından Bugüne</b>, yılın ilk gününden rapor tarihine kadar<br>olan dönemi ifade etmektedir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    yanchor="top",
    xanchor="left",
    align="left",
)


fig.update_layout(margin=dict(t=80, b=120))

fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=2.5, sizey=2.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

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
                   title='Yük Tahmin Planı',
                   labels={"value": "Yük Tahmini (MWh)", "variable":""},
                   template="plotly_white")

load_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)




load_fig.update_xaxes(range=[0, 23], constrain='domain')
load_fig.update_xaxes(dtick=1)

load_fig.update_yaxes(exponentformat='none', showexponent='none')

load_fig.update_traces(name="D-1", selector=dict(name="Yük Tahmini (D-1)"))
load_fig.update_traces(name="D", selector=dict(name="Yük Tahmini (D)"))
load_fig.update_traces(name="D+1", selector=dict(name="Yük Tahmini (D+1)"))

load_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i><b>Yük Tahmin Planı</b>, sistem operatörü (TEİAŞ) tarafından saatlik bazda yapılan talep tahminidir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    yanchor="top",
    xanchor="left",
)

load_fig.update_layout(margin=dict(t=40, b=120))

load_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

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
                            title='Fiyat Bağımsız Yenilenebilir Enerji Üretimi',
                            labels={"value": "Üretim (MWh)", "variable":""},
                            template="plotly_white")

production_fb_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)



production_fb_fig.update_traces(name="D-1", selector=dict(name="Üretim (D-1)"))
production_fb_fig.update_traces(name="D", selector=dict(name="Üretim (D)"))
production_fb_fig.update_traces(name="D+1", selector=dict(name="Üretim (D+1)"))

production_fb_fig.update_xaxes(range=[0, 23], constrain='domain')
production_fb_fig.update_xaxes(dtick=1)
production_fb_fig.update_yaxes(range=[0, 25_000])
production_fb_fig.update_yaxes(dtick=2500)
production_fb_fig.update_yaxes(exponentformat='none', showexponent='none')

production_fb_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Spot piyasa fiyatlarından bağımsız olarak üretim gerçekleştirip satışa sunan,<b>akarsu</b>; <b>rüzgar</b>;" +
         "<br>" + "<b>jeotermal</b>; <b>biyokütle</b> ve <b>güneş</b> enerjisi santrallerinin saatlik üretim planlamasıdır.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

production_fb_fig.update_layout(margin=dict(t=40, b=120))

production_fb_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))



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
                            title='EUAS İkili Anlaşma Satış İstatistiği',
                            labels={"value": "İA Satış Miktarı", "variable":""},
                            template="plotly_white")

coal_kgup = pd.DataFrame(columns=['Saat', 'Kömür KGUP'])
coal_kgup['Saat'] = yesterday_production['Saat']
coal_kgup['Kömür KGUP (D-1)'] = yesterday_production["Ithalkomur"] + yesterday_production["Linyit"]
coal_kgup['Kömür KGUP (D)'] = today_production["Ithalkomur"] + today_production["Linyit"]
coal_kgup['Kömür KGUP (D+1)'] = tomorrow_production["Ithalkomur"] + tomorrow_production["Linyit"]

coal_kgup_fig = px.line(coal_kgup, x="Saat", y=["Kömür KGUP (D-1)","Kömür KGUP (D)","Kömür KGUP (D+1)"],
                            title='Kömürden Elektrik Üretimi',
                            labels={"value": "Üretim (MWh)", "variable":""},
                            template="plotly_white")

coal_kgup_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)

coal_kgup_fig.update_xaxes(range=[0, 23], constrain='domain')
coal_kgup_fig.update_xaxes(dtick=1)
coal_kgup_fig.update_yaxes(range=[0, 25_000])
coal_kgup_fig.update_yaxes(dtick=2500)
coal_kgup_fig.update_yaxes(exponentformat='none', showexponent='none')

coal_kgup_fig.update_traces(name="D-1", selector=dict(name="Kömür KGUP (D-1)"))
coal_kgup_fig.update_traces(name="D", selector=dict(name="Kömür KGUP (D)"))
coal_kgup_fig.update_traces(name="D+1", selector=dict(name="Kömür KGUP (D+1)"))

coal_kgup_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i><b>Yerli</b> ve <b>ithal kömür</b> santrallerinin saatlik üretim planlamasıdır.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    yanchor="top",
    xanchor="left",
)

coal_kgup_fig.update_layout(margin=dict(t=40, b=120))

coal_kgup_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))




df_kalan_yük = pd.DataFrame(columns=['Saat', 'Kalan Yük (D-1)',"Kalan Yük (D)","Kalan Yük (D+1)"])
df_kalan_yük["Saat"] = saat
df_kalan_yük["Kalan Yük (D-1)"] = df_load["Yük Tahmini (D-1)"] - df_production_fb["Üretim (D-1)"] - df_euas_sell["İA Satış (D-1)"]
df_kalan_yük["Kalan Yük (D)"] = df_load["Yük Tahmini (D)"] - df_production_fb["Üretim (D)"] - df_euas_sell["İA Satış (D)"]
df_kalan_yük["Kalan Yük (D+1)"] = df_load["Yük Tahmini (D+1)"] - df_production_fb["Üretim (D+1)"] - df_euas_sell["İA Satış (D+1)"]

kalan_yük_fig = px.line(df_kalan_yük, x="Saat", y=["Kalan Yük (D-1)","Kalan Yük (D)","Kalan Yük (D+1)"],
                        title='Kalan Yük',
                        labels={"value": "Kalan Yük (MWh)", "variable":""},
                        template="plotly_white")

kalan_yük_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)

kalan_yük_fig.update_xaxes(range=[0, 23], constrain='domain')
kalan_yük_fig.update_xaxes(dtick=1)
kalan_yük_fig.update_yaxes(range=[0, 25_000])
kalan_yük_fig.update_yaxes(dtick=2500)
kalan_yük_fig.update_yaxes(exponentformat='none', showexponent='none')

kalan_yük_fig.update_traces(name="D-1", selector=dict(name="Kalan Yük (D-1)"))
kalan_yük_fig.update_traces(name="D", selector=dict(name="Kalan Yük (D)"))
kalan_yük_fig.update_traces(name="D+1", selector=dict(name="Kalan Yük (D+1)"))

kalan_yük_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Yük Tahmin Planından, Fiyat Bağımsız Yenilenebilir Enerji Üretimi ve Kömürden Elektrik Üretimi" + "<br>" +"düşüldükten sonra kalan taleptir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

kalan_yük_fig.update_layout(margin=dict(t=40, b=120))

kalan_yük_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

##############################################################################
fiyat_week = ptf(week_start_date, week_end_date)
tüketim_week = get_real_time_consumption(week_start_date, week_end_date)
tüketim_week = tüketim_week.reset_index()
fiyat_week["Tüketim"] = tüketim_week["Tüketim"]

fiyat_week = fiyat_week.drop(columns=["Fiyat (EUR)"])
fiyat_week = fiyat_week.drop(columns=["Tarih"])

week1_raw = fiyat_week.iloc[:168]
week2_raw = fiyat_week.iloc[168:336]
week3_raw = fiyat_week.iloc[336:504]
week4_raw = fiyat_week.iloc[504:672]





week1 = pd.DataFrame(columns=["Pzt", "Salı","Çarş","Perş","Cuma","Cmt","Paz"])
week2 = pd.DataFrame(columns=["Pzt", "Salı","Çarş","Perş","Cuma","Cmt","Paz"])
week3 = pd.DataFrame(columns=["Pzt", "Salı","Çarş","Perş","Cuma","Cmt","Paz"])
week4 = pd.DataFrame(columns=["Pzt", "Salı","Çarş","Perş","Cuma","Cmt","Paz"])

week1["Pzt"] = (week1_raw.iloc[0:24].mean().values).round(2)
week1["Salı"] = (week1_raw.iloc[24:48].mean().values).round(2)
week1["Çarş"] = (week1_raw.iloc[48:72].mean().values).round(2)
week1["Perş"] = (week1_raw.iloc[72:96].mean().values).round(2)
week1["Cuma"] = (week1_raw.iloc[96:120].mean().values).round(2)
week1["Cmt"] = (week1_raw.iloc[120:144].mean().values).round(2)
week1["Paz"] = (week1_raw.iloc[144:168].mean().values).round(2)
week1["Ort"] = week1.mean(axis=1).values.round(2)

week2["Pzt"] = week2_raw.iloc[0:24].mean().values.round(2)
week2["Salı"] = week2_raw.iloc[24:48].mean().values.round(2)
week2["Çarş"] = week2_raw.iloc[48:72].mean().values.round(2)
week2["Perş"] = week2_raw.iloc[72:96].mean().values.round(2)
week2["Cuma"] = week2_raw.iloc[96:120].mean().values.round(2)
week2["Cmt"] = week2_raw.iloc[120:144].mean().values.round(2)
week2["Paz"] = week2_raw.iloc[144:168].mean().values.round(2)
week2["Ort"] = week2.mean(axis=1).values.round(2)

week3["Pzt"] = week3_raw.iloc[0:24].mean().values.round(2)
week3["Salı"] = week3_raw.iloc[24:48].mean().values.round(2)
week3["Çarş"] = week3_raw.iloc[48:72].mean().values.round(2)
week3["Perş"] = week3_raw.iloc[72:96].mean().values.round(2)
week3["Cuma"] = week3_raw.iloc[96:120].mean().values.round(2)
week3["Cmt"] = week3_raw.iloc[120:144].mean().values.round(2)
week3["Paz"] = week3_raw.iloc[144:168].mean().values.round(2)
week3["Ort"] = week3.mean(axis=1).values.round(2)

week4["Pzt"] = week4_raw.iloc[0:24].mean().values.round(2)
week4["Salı"] = week4_raw.iloc[24:48].mean().values.round(2)
week4["Çarş"] = week4_raw.iloc[48:72].mean().values.round(2)
week4["Perş"] = week4_raw.iloc[72:96].mean().values.round(2)
week4["Cuma"] = week4_raw.iloc[96:120].mean().values.round(2)
week4["Cmt"] = week4_raw.iloc[120:144].mean().values.round(2)
week4["Paz"] = week4_raw.iloc[144:168].mean().values.round(2)
week4["Ort"] = week4.mean(axis=1).values.round(2)

week1["Veri Tipi"] = ["PTF(TL)", "PTF(USD)","Tüketim"]
week2["Veri Tipi"] = ["PTF(TL)", "PTF(USD)","Tüketim"]
week3["Veri Tipi"] = ["PTF(TL)", "PTF(USD)","Tüketim"]
week4["Veri Tipi"] = ["PTF(TL)", "PTF(USD)","Tüketim"]

week_start_date = datetime.strptime(week_start_date, '%Y-%m-%d')
merged = pd.concat([week1, week2, week3, week4], axis=0)

table_last_four_week = pd.DataFrame(columns=["Hafta","Veri Tipi", "Pzt", "Salı","Çarş","Perş","Cuma","Cmt","Paz"])
table_last_four_week["Hafta"] = [week_start_date.strftime("%d.%m") + " - " + (week_start_date+timedelta(days=6)).strftime("%d.%m"),"","",(week_start_date + timedelta(days=7)).strftime("%d.%m") + " - " + (week_start_date + timedelta(days=13)).strftime("%d.%m") ,"","", (week_start_date + timedelta(days=14)).strftime("%d.%m") + " - " + (week_start_date + timedelta(days=20)).strftime("%d.%m"),"","", (week_start_date + timedelta(days=21)).strftime("%d.%m") + " - " + (week_start_date + timedelta(days=27)).strftime("%d.%m"),"",""]
table_last_four_week["Veri Tipi"] = ["PTF (TL/MWh)", "PTF (USD/MWh)","Tüketim (MWh)","PTF (TL/MWh)", "PTF (USD/MWh)","Tüketim (MWh)","PTF (TL/MWh)", "PTF (USD/MWh)","Tüketim (MWh)","PTF (TL/MWh)", "PTF (USD/MWh)","Tüketim (MWh)"]
table_last_four_week["Pzt"] = merged["Pzt"].values
table_last_four_week["Salı"] = merged["Salı"].values
table_last_four_week["Çarş"] = merged["Çarş"].values
table_last_four_week["Perş"] = merged["Perş"].values
table_last_four_week["Cuma"] = merged["Cuma"].values
table_last_four_week["Cmt"] = merged["Cmt"].values
table_last_four_week["Paz"] = merged["Paz"].values
table_last_four_week["Ort"] = merged["Ort"].values
table_last_four_week["Değişim Oranı"] = [np.nan,np.nan,np.nan,
                                         table_last_four_week["Ort"].iloc[3]/table_last_four_week["Ort"].iloc[0] - 1,
                                         table_last_four_week["Ort"].iloc[4]/table_last_four_week["Ort"].iloc[1] - 1,
                                         table_last_four_week["Ort"].iloc[5]/table_last_four_week["Ort"].iloc[2] - 1,
                                         table_last_four_week["Ort"].iloc[6]/table_last_four_week["Ort"].iloc[3] - 1,
                                         table_last_four_week["Ort"].iloc[7]/table_last_four_week["Ort"].iloc[4] - 1,
                                         table_last_four_week["Ort"].iloc[8]/table_last_four_week["Ort"].iloc[5] - 1,
                                         table_last_four_week["Ort"].iloc[9]/table_last_four_week["Ort"].iloc[6] - 1,
                                         table_last_four_week["Ort"].iloc[10]/table_last_four_week["Ort"].iloc[7] - 1,
                                         table_last_four_week["Ort"].iloc[11]/table_last_four_week["Ort"].iloc[8] - 1,]

table_last_four_week["Değişim Oranı"] = table_last_four_week["Değişim Oranı"] * 100

#table_last_four_week["Değişim Oranı"] convert type to float



table_last_four_week["Pzt"] = table_last_four_week["Pzt"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Salı"] = table_last_four_week["Salı"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Çarş"] = table_last_four_week["Çarş"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Perş"] = table_last_four_week["Perş"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Cuma"] = table_last_four_week["Cuma"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Cmt"] = table_last_four_week["Cmt"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Paz"] = table_last_four_week["Paz"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Ort"] = table_last_four_week["Ort"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Değişim Oranı"] = table_last_four_week["Değişim Oranı"].apply(lambda x: f'{x:.2f}'.replace('.', ','))
table_last_four_week["Değişim Oranı"] = table_last_four_week["Değişim Oranı"].apply(lambda x: f"{x}%")

table_last_four_week["Değişim Oranı"].iloc[0] = ""
table_last_four_week["Değişim Oranı"].iloc[1] = ""
table_last_four_week["Değişim Oranı"].iloc[2] = ""




week_start_date = datetime.strftime(week_start_date, '%Y-%m-%d')

table_week = dash_table.DataTable(
        table_last_four_week.to_dict('records'),
        [
            dict(id = "Hafta", name = "Hafta" , type = "text"),
            dict(id = "Veri Tipi", name = "Veri Tipi" , type = "text"),
            dict(id = "Pzt", name = "Pzt" , type = "numeric", format = Format().group(True)),
            dict(id = "Salı", name = "Salı" , type = "numeric", format = Format().group(True)),
            dict(id = "Çarş", name = "Çarş" , type = "numeric", format = Format().group(True)),
            dict(id = "Perş", name = "Perş" , type = "numeric", format = Format().group(True)),
            dict(id = "Cuma", name = "Cuma" , type = "numeric", format = Format().group(True)),
            dict(id = "Cmt", name = "Cmt" , type = "numeric", format = Format().group(True)),
            dict(id = "Paz", name = "Paz" , type = "numeric", format = Format().group(True)),
            dict(id = "Ort", name = "Haftalık Ortalama" , type = "numeric", format = Format().group(True)),
            dict(id = "Değişim Oranı", name = "Haftalık Değişim (%)" , type = "text"),

        ],

    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
        "whiteSpace" : "normal",
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle'  # Dikeyde ortalama
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
        'height': 'auto',
        # all three widths are needed
        'whiteSpace': 'normal',
        "maxWidth":"40px",
        "width":"40px",
        "minWidth":"40px",

    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        },
        {
            'if': {'column_id': 'Veri Tipi'},
            'text-align': 'left',  # Yatayda ortalama
        },
        {
            "if": {"column_id": "Hafta"},
            "font":"italic 16px Calibri",
        },
        {
            "if": {"column_id": "Ort"},
            "font":"bold 16px Calibri",
        },
        {
            "if": {"column_id": "Değişim Oranı"},
            "font":"bold 16px Calibri",
        }
        ],

    style_data={
    'text-align': 'center',  # Yatayda ortalama
    'vertical-align': 'middle'  # Dikeyde ortalama
    }
    
    )





##############################################################################
# GİP
raw = trade_history_raw(yesterday, yesterday)
parsed_data = trade_history_parsed(yesterday, yesterday)
contract_list = parse_contract(parsed_data)
contract_list = np.array(contract_list)

totalP = []
totalV = []
max200P = []
min200P = []

for element in contract_list:
    table = element.table
    table = table.reset_index(drop=True)
    table = table.groupby(['Tarih', 'Saat', 'Kontrat Adı',]).apply(weighted_average).reset_index()
    totalP.append(table[0][0])

    table = element.table
    table = table.reset_index(drop=True)
    totalV.append(table["Miktar (Lot)"].sum()/10)

    table = get_max_trades(element,2000)
    table = table.reset_index(drop=True)
    table = table.groupby(['Tarih', 'Saat', 'Kontrat Adı',]).apply(weighted_average).reset_index()
    max200P.append(table[0][0])

    table = get_min_trades(element,2000)
    table = table.reset_index(drop=True)
    table = table.groupby(['Tarih', 'Saat', 'Kontrat Adı',]).apply(weighted_average).reset_index()
    min200P.append(table[0][0])

gip_table = pd.DataFrame(columns=["Saat","totalV","totalP","max200P","min200P"])
gip_table["Saat"] = range(0,24)
gip_table["totalV"] = totalV
gip_table["totalP"] = totalP
gip_table["max200P"] = max200P
gip_table["min200P"] = min200P

#####################################################
yesterday_order = get_order(yesterday, yesterday)
yesterday_order = yesterday_order.reset_index(drop=True)

df_dgp = pd.DataFrame(columns=['Saat', 'PTF',"SMF","+EDMal","-EDMal","Net Talimat Hacmi"])
df_dgp["Saat"] = saat
df_dgp["PTF"] = price_yesterday["PTF"]
#smf her koşulda virgülden sonra 2 hane. Eğer tam sayı ise virgülden sonra 2 sıfır olmalı
df_dgp["SMF"] = price_yesterday["SMF"]

df_dgp["+EDMal"] = round(price_yesterday["PTF"] - price_yesterday["+EDF"],2)
df_dgp["-EDMal"] = round(price_yesterday["-EDF"] - price_yesterday["PTF"],2)
df_dgp["Pozitif Dengesizlik Fiyatı"] = price_yesterday["+EDF"]
df_dgp["Negatif Dengesizlik Fiyatı"] = price_yesterday["-EDF"]

df_dgp['Net Talimat Hacmi'] = df_dgp['Net Talimat Hacmi'].replace(".",",")


df_dgp["Net Talimat Hacmi"] = yesterday_order["Net Talimat"].astype(str) + yesterday_order["Net Talimat"].apply(lambda x: "🟢" if x < 0 else "🟡" if x == 0 else "🔴")

df_dgp_display = df_dgp.copy()
df_dgp_display['PTF'] = df_dgp['PTF'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['SMF'] = df_dgp['SMF'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['Pozitif Dengesizlik Fiyatı'] = df_dgp['Pozitif Dengesizlik Fiyatı'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['Negatif Dengesizlik Fiyatı'] = df_dgp['Negatif Dengesizlik Fiyatı'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['Net Talimat Hacmi'] = df_dgp['Net Talimat Hacmi']
df_dgp_display['totalV'] = gip_table['totalV'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['totalP'] = gip_table['totalP'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['max200P'] = gip_table['max200P'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['min200P'] = gip_table['min200P'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
df_dgp_display['Sistem Yönü'] = yesterday_order['Sistem Yönü']
df_dgp["PTF - GİP AOF"] = round(df_dgp["PTF"] - gip_table["totalP"],2)
df_dgp["PTF - +EDF"] = round(df_dgp["PTF"] - df_dgp["Pozitif Dengesizlik Fiyatı"],2)
df_dgp["PTF - -EDF"] = round(df_dgp["PTF"] - df_dgp["Negatif Dengesizlik Fiyatı"],2)




table_dgp_new = dash_table.DataTable(
        df_dgp_display.to_dict('records'),
    
    [
        dict(id = "Saat", name = "Saat" , type = "numeric", format = Format() ),
        dict(id = "PTF", name = "PTF" , type = "numeric", format = Format().group(True)),
        dict(id = "SMF", name = "SMF" , type = "numeric", format = Format().group(True)),
        dict(id = "Pozitif Dengesizlik Fiyatı", name = "(+) Dengesizlik Fiyatı" , type = "numeric", format = Format().group(True)),
        dict(id = "Negatif Dengesizlik Fiyatı", name = "(-) Dengesizlik Fiyatı" , type = "numeric", format = Format().group(True)),
        dict(id = "totalP", name = "GİP AOF" , type = "numeric", format = Format().group(True)),
        dict(id = "min200P", name = "GİP Minimum 200MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "max200P", name = "GİP Maksimum 200MWh" , type = "numeric", format = Format().group(True)),
        dict(id = "totalV", name = "GİP İşlem Hacmi" , type = "numeric", format = Format().group(True)),
        dict(id = "Sistem Yönü", name = "Sistem Yönü" , type = "text"),
        dict(id = "Net Talimat Hacmi", name = "Net Talimat Hacmi" , type = "text"),

    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': '#285A84',
        'fontWeight': 'bold',
        "font":"bold 16px Calibri",
        "color":"white",
        "whiteSpace" : "normal",
        'text-align': 'center',  # Yatayda ortalama
        'vertical-align': 'middle',  # Dikeyde ortalama
        "height":"auto",
        'width': '80px',
        "minWidth":"80px",
        "maxWidth":"80px",

    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
        'height': 'auto',
    },


    
    style_data={
    'text-align': 'center',  # Yatayda ortalama
    'vertical-align': 'middle',  # Dikeyde ortalama
    "whiteSpace" : "normal",
    'width': '80px',
    "minWidth":"80px",
    "maxWidth":"80px",
    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',
        },

        {
            'if': {'column_id': 'Net Talimat Hacmi'},
            'text-align': 'right',  # Yatayda ortalama
        },
        {
            #Sistem Yönü YAT ise yazı rengi yeşil, DEĞİLSE kırmızı
            'if': {'column_id': 'Sistem Yönü',
                   'filter_query': '{Sistem Yönü} eq "YAT"'},
            'color': '#28A745',
            "font":"bold 16px Calibri",
        },
        {
            'if': {'column_id': 'Sistem Yönü',
                    'filter_query': '{Sistem Yönü} eq "YAL"'},
            'color': '#E13915',
            "font":"bold 16px Calibri",
        },
        {
            'if': {'column_id': 'Sistem Yönü',
                    'filter_query': '{Sistem Yönü} eq "DNG"'},
            'color': '#FFB000',
            "font":"bold 16px Calibri",

        }

    ],

    )

edmal_fig = px.bar(df_dgp, x="Saat", y=["+EDMal","-EDMal"],
                     title='Dengesizlik Maliyeti İstatistikleri (D-1)',
                     labels={"value": "Enerji Dengesizlik Maliyeti (TL/MWh)", "variable":""},
                     template="plotly_white",
                     barmode="group",
                     color_discrete_sequence=["#285A84","#E13915"])

edmal_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)

edmal_fig.update_xaxes(range=[0, 23], constrain='domain')
edmal_fig.update_xaxes(dtick=1)

edmal_fig.update_traces(name="Pozitif Dengesizlik Maliyeti", selector=dict(name="+EDMal"))
edmal_fig.update_traces(name="Negatif Dengesizlik Maliyeti", selector=dict(name="-EDMal"))

edmal_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

edmal_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Her 1 MWh'lik pozitif (enerji fazlası) ve negatif (enerji açığı) dengesizliğin TL/MWh cinsinden"+ 
    "<br>" + "saatlik bazda birim maliyeti gösterilmektedir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

edmal_fig.update_layout(margin=dict(t=40, b=120))

# Makas = PTF-SMF. Create line blot for Makas and add Net Talimat Hacmi as box plot
df_makas = pd.DataFrame(columns=['Saat', 'Makas',"Net Talimat Hacmi"])
df_makas["Saat"] = saat
df_makas["Makas"] = round(price_yesterday["PTF"] - price_yesterday["SMF"],2)
df_makas["Net Talimat Hacmi"] = yesterday_order["Net Talimat"]

#net talimat hacmi sıfırdan küçükse "green", sıfırdan büyükse "red" yazacak color sütunu ekle

colors = ['#28A745' if val < 0 else '#E13915' for val in df_makas["Net Talimat Hacmi"]] 
makas_fig = px.line(df_makas, x="Saat", y=["Makas"],
                        title='Talimat Hacmine ve PTF-SMF Farkı (D-1)',
                        labels={"value": "PTF-SMF (TL/MWh)", "variable":""},
                        template="plotly_white",
                        color_discrete_sequence=["#285A84","#E13915"],
                        )
makas_fig.add_bar(x=df_makas["Saat"], y=df_makas["Net Talimat Hacmi"], name="Net Talimat Hacmi",marker_color=colors,yaxis="y2")

makas_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    yaxis=dict(
        title="PTF-SMF (TL/MWh)",
    ),
     yaxis2=dict(  # İkincil y ekseni için layout ayarları
        title="Net Talimat Hacmi",
        overlaying="y",  # İkincil y eksenini ana y ekseninin üzerine koy
        side="right",  # İkincil y ekseni sağda olsun
    )

)

makas_fig.update_xaxes(range=[0, 23], constrain='domain')
makas_fig.update_xaxes(dtick=1)

y_max = max(abs(df_makas["Makas"].max()), abs(df_makas["Makas"].min()))
makas_fig.update_yaxes(range=[-y_max, y_max])

makas_fig.update_traces(name="PTF-SMF Farkı (D-1)", selector=dict(name="Makas"))

y2_max = max(abs(df_makas["Net Talimat Hacmi"].max()), abs(df_makas["Net Talimat Hacmi"].min()))

#makas fig Net Talimat Hacmi için için ikinci bir eksen oluştur. 
makas_fig.update_layout(
    yaxis2=dict(
        overlaying="y",
        side="right",
        showgrid=False,
        showticklabels=True,
        zeroline=False,
        showline=False,
        range=[-y2_max, y2_max],
    ),
    width=625,
    height=475,
)

makas_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Piyasa Takas Fiyatı ile aynı saate ait Sistem Marjinal Fiyatının farkı ve bu farkın" + 
    "<br>" + "Net Talimat Hacmi ile ilişkisi gösterilmektedir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

makas_fig.update_layout(margin=dict(t=40, b=120))


makas_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

""" ## TEST ##
makas_fig.add_shape(
    go.layout.Shape(
        type="line",
        x0=0,
        x1=23,
        y0=0,
        y1=0,
        line=dict(color="rgba(255, 255, 255, 0)", width=0)
    )
)

# x eksenindeki etiketleri y=0 çizgisine ekleyin
for i, saat in enumerate(df_makas["Saat"]):
    makas_fig.add_annotation(
        go.layout.Annotation(
            x=saat,
            y=0,
            xref="x",
            yref="y",
            text=str(saat),
            showarrow=False,
            ax=0,
            ay=-20,  # y=0 çizgisinden ne kadar aşağıda olduğunu ayarlayabilirsiniz
            font=dict(size=11)
        )
    )

# Asıl x eksenindeki etiketleri gizleyin
makas_fig.update_xaxes(showticklabels=False)

####### """

gip_fig = px.line(df_dgp, x="Saat", y= ["PTF - GİP AOF"],
                        title='PTF, GİP AOF ve Dengesizlik Fiyatlarının İlişkisi (D-1)',
                        labels={"value": "Fiyat (TL/MWh)", "variable":""},
                        template="plotly_white",
                        color_discrete_sequence=["#285A84","#E13915"],
                        )

#ADD [PTF - +EDF] and [PTF - -EDF] to the graph
gip_fig.add_trace(go.Scatter(x=df_dgp["Saat"], y=df_dgp["PTF - +EDF"], name="PTF - +EDF", line=dict(color="#00b159")))
gip_fig.add_trace(go.Scatter(x=df_dgp["Saat"], y=df_dgp["PTF - -EDF"], name="PTF - -EDF", line=dict(color="#d11141")))

# find max between [PTF - +EDF] and [PTF - -EDF] and [PTF - GİP]

ptf_pedf = (df_dgp["PTF - +EDF"].abs()).max()
ptf_nedf = (df_dgp["PTF - -EDF"].abs()).max()
ptf_gip = (df_dgp["PTF - GİP AOF"].abs()).max()

max_df_dgp = pd.Series([ptf_pedf, ptf_nedf, ptf_gip]).max() + 100

# set the y axis range to [-max_df_dgp, max_df_dgp]
gip_fig.update_yaxes(range=[-max_df_dgp.max(), max_df_dgp.max()])
gip_fig.update_xaxes(range=[0, 23], constrain='domain')
gip_fig.update_xaxes(dtick=1)

gip_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)

gip_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Piyasa Takas Fiyatı'nın, saatlik GİP işlemlerinin ağırlıklı ortalama fiyatı,"+ "<br>" +"Pozitif Dengesizlik Fiyatı ve Negatif Dengesizlik Fiyatı ile farkı gösterilmektedir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

gip_fig.update_layout(margin=dict(t=40, b=120))


gip_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

ptf_smf_gip_df = pd.DataFrame(columns=['Saat', 'PTF(D-1)',"SMF(D-1)","GİP AOF(D-1)"])
ptf_smf_gip_df["Saat"] = saat
ptf_smf_gip_df["PTF(D-1)"] = price_yesterday["PTF"]
ptf_smf_gip_df["SMF(D-1)"] = price_yesterday["SMF"]
ptf_smf_gip_df["GİP AOF(D-1)"] = gip_table["totalP"]

ptf_smf_fig = px.line(ptf_smf_gip_df, x="Saat", y=["PTF(D-1)","SMF(D-1)","GİP AOF(D-1)"], 
                      title='PTF SMF ve GİP AOF İstatistikleri (D-1)',
                      labels={"value": "Fiyat (TL/MWh)", "variable":""},
                      template="plotly_white",
                      range_x=[0,23],
                      )

ptf_smf_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)
ptf_smf_fig.update_layout(margin=dict(t=40, b=120))

ptf_smf_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))


ptf_smf_fig.update_xaxes(range=[0, 23], constrain='domain')
ptf_smf_fig.update_xaxes(dtick=1)

ptf_smf_fig.update_yaxes(range=[0, 3000], constrain='domain')
ptf_smf_fig.update_yaxes(dtick=500)

ptf_smf_fig.update_traces(name="PTF", selector=dict(name="PTF(D-1)"))
ptf_smf_fig.update_traces(name="SMF", selector=dict(name="SMF(D-1)"))
ptf_smf_fig.update_traces(name="GİP AOF", selector=dict(name="GİP AOF(D-1)"))


production_T = get_real_time_production_transposed(yesterday, yesterday)
production_T["Üretimdeki Pay"] = production_T["Üretimdeki Pay"] * 100

production_T_display = production_T.copy()
production_T_display['Günlük Üretim'] = production_T['Günlük Üretim'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
production_T_display['Saatlik Üretim'] = production_T['Saatlik Üretim'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
production_T_display['Üretimdeki Pay'] = production_T['Üretimdeki Pay'].apply(lambda x: f'{x:.1f}'.replace('.', ',')) + " %"
production_T_display['Kurulu Güç'] = production_T['Kurulu Güç'].apply(lambda x: f'{x:.0f}'.replace('.', ','))
production_T_display['Kapasite Faktörü'] = production_T['Kapasite Faktörü'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
production_T_display = production_T_display.replace(np.nan, '')


table_production_T = dash_table.DataTable(
        production_T_display.to_dict('records'),
    
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
        "whiteSpace" : "normal",
        'text-align': 'center',  # Yatayda ortalama
        "height": "auto",
        'vertical-align': 'middle'  # Dikeyde ortalama
    },

    style_cell={
        'fontWeight': 'bold',
        "font":"16px Calibri",
        'height': 'auto',

    },

    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5faff',

        },
        {
            'if': {'column_id': 'Kaynak Tipi'},
            'text-align': 'left',
            "fontWeight": "bold",
        },
        {
            "if": {"row_index": -1},
            'fontWeight': 'bold',

        },

        ],

    style_data={
    'text-align': 'center',  # Yatayda ortalama
    'vertical-align': 'middle'  # Dikeyde ortalama
    },


    )

# Termik = Doğal Gaz,Linyit,İthal Kömür,Diğer. Yenilenebilir = Rüzgar,Güneş,Barajlı,Akarsu,Biyokütle,Jeotermal. Create pie chart
# Create pie chart
termik = ["Doğal Gaz","Linyit","İthal Kömür","Diğer"]
production_T_pie_table = production_T.copy()
production_T_pie_table['Kaynak Türü'] = production_T['Kaynak Tipi'].apply(lambda x: 'Termik' if x in termik else 'Yenilenebilir')
production_T_pie_table = production_T_pie_table.sort_values(by=['Kaynak Türü', 'Kaynak Tipi']).reset_index(drop=True)
production_T_pie_table = production_T_pie_table[:-1]

color_map = {
    "Termik" : "#27374D",
    "Yenilenebilir" : "#618264",
}


# Grafik
production_T_pie = px.sunburst(
    production_T_pie_table, 
    path=['Kaynak Türü', 'Kaynak Tipi'], 
    values='Günlük Üretim', 
    color='Kaynak Türü',
    color_discrete_map=color_map,
    
)

production_T_pie.update_layout(width=600, height=600)

####################################################




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
                            title='Yıllara Göre PTF İstatistiği (TL/MWh)',
                            labels={"value": "PTF (TL/MWh)", "variable":""},
                            template="plotly_white")

yearly_price_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),
)

yearly_price_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_price_fig.update_xaxes(dtick=1)

yearly_price_fig.update_traces(name="2021", selector=dict(name="2021 (TL)"))
yearly_price_fig.update_traces(name="2022", selector=dict(name="2022 (TL)"))
yearly_price_fig.update_traces(name="2023", selector=dict(name="2023 (TL)"))

yearly_price_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

yearly_price_usd_fig = px.line(yearly_price, x="Ay", y=["2021 (USD)","2022 (USD)","2023 (USD)"],
                            title='Yıllara Göre PTF İstatistiği (USD/MWh)',
                            labels={"value": "PTF (USD/MWh)", "variable":""},
                            template="plotly_white")

yearly_price_usd_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),
)

yearly_price_usd_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_price_usd_fig.update_xaxes(dtick=1)

yearly_price_usd_fig.update_yaxes(range=[0, 250], constrain='domain')
yearly_price_usd_fig.update_yaxes(dtick=50)

yearly_price_usd_fig.update_traces(name="2021", selector=dict(name="2021 (USD)"))
yearly_price_usd_fig.update_traces(name="2022", selector=dict(name="2022 (USD)"))
yearly_price_usd_fig.update_traces(name="2023", selector=dict(name="2023 (USD)"))

yearly_price_usd_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

cons_2023 = get_real_time_consumption("2023-01-01",today)

cons_2023_m = cons_2023.groupby(pd.Grouper(freq="M")).agg({'Saat': 'mean', 'Tüketim': 'mean'})

cons_2022 = get_real_time_consumption("2022-01-01","2022-12-31")

cons_2022_m = cons_2022.groupby(pd.Grouper(freq="M")).agg({'Saat': 'mean', 'Tüketim': 'mean'})

cons_2021 = get_real_time_consumption("2021-01-01","2021-12-31")

cons_2021_m = cons_2021.groupby(pd.Grouper(freq="M")).agg({'Saat': 'mean', 'Tüketim': 'mean'})

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
                            title='Yıllara Göre Tüketim',
                            labels={"value": "Tüketim (MWh)", "variable":""},
                            template="plotly_white")

yearly_cons_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),
)



yearly_cons_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_cons_fig.update_xaxes(dtick=1)

yearly_cons_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))


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
price_2021.set_index("Tarih", inplace=True)
price_2021_aylik = price_2021.groupby(pd.Grouper(freq="M")).agg({'PTF': 'mean', 'SMF': 'mean', '+EDF': 'mean', '-EDF': 'mean', '+EDMal': 'mean', '-EDMal': 'mean'})
price_2021_aylik = price_2021_aylik.reset_index()
price_2021_aylik["Ay"] = range(1,13)


price_2022["Tarih"] = pd.to_datetime(price_2022["Tarih"])
max_fiyat = price_2022.apply(fiyat_max, axis=1)
min_fiyat = price_2022.apply(fiyat_min, axis=1)
price_2022["+EDF"] = round((min_fiyat * 0.97),2)
price_2022["-EDF"] = round((max_fiyat * 1.03),2)
price_2022["+EDMal"] = round(price_2022["PTF"] - price_2022["+EDF"],2)
price_2022["-EDMal"] = round(price_2022["-EDF"] - price_2022["PTF"],2)

price_2022["Ay"] = price_2022["Tarih"].dt.month
price_2022.set_index("Tarih", inplace=True)
price_2022_aylik = price_2022.groupby(pd.Grouper(freq="M")).agg({'PTF': 'mean', 'SMF': 'mean', '+EDF': 'mean', '-EDF': 'mean', '+EDMal': 'mean', '-EDMal': 'mean'})
price_2022_aylik = price_2022_aylik.reset_index()
price_2022_aylik["Ay"] = range(1,13)


price_2023["Tarih"] = pd.to_datetime(price_2023["Tarih"])
max_fiyat = price_2023.apply(fiyat_max, axis=1)
min_fiyat = price_2023.apply(fiyat_min, axis=1)
price_2023["+EDF"] = round((min_fiyat * 0.97),2)
price_2023["-EDF"] = round((max_fiyat * 1.03),2)
price_2023["+EDMal"] = round(price_2023["PTF"] - price_2023["+EDF"],2)
price_2023["-EDMal"] = round(price_2023["-EDF"] - price_2023["PTF"],2)

price_2023["Ay"] = price_2023["Tarih"].dt.month
price_2023.set_index("Tarih", inplace=True)
price_2023_aylik = price_2023.groupby(pd.Grouper(freq="M")).agg({'PTF': 'mean', 'SMF': 'mean', '+EDF': 'mean', '-EDF': 'mean', '+EDMal': 'mean', '-EDMal': 'mean'})
price_2023_aylik = price_2023_aylik.reset_index()   
price_2023_aylik["Ay"] = range(1,int(datetime.strptime(today, '%Y-%m-%d').month) +1)


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
                            title='Yıllara Göre Pozitif Dengesizlik Maliyeti İstatistiği',
                            labels={"value": "Pozitif Enerji Dengesizlik Maliyeti (TL/MWh)", "variable":""},
                            template="plotly_white")

yearly_positive_edmal_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),
)

yearly_positive_edmal_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_positive_edmal_fig.update_xaxes(dtick=1)
yearly_positive_edmal_fig.update_yaxes(range=[15, 400])

yearly_positive_edmal_fig.update_traces(name="2021", selector=dict(name="2021 +EDMal"))
yearly_positive_edmal_fig.update_traces(name="2022", selector=dict(name="2022 +EDMal"))
yearly_positive_edmal_fig.update_traces(name="2023", selector=dict(name="2023 +EDMal"))

yearly_positive_edmal_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

yearly_negative_edmal_fig = px.line(yearly_price, x="Ay", y=["2021 -EDMal","2022 -EDMal","2023 -EDMal"],
                            title='Yıllara Göre Negatif Dengesizlik Maliyeti İstatistiği',
                            labels={"value": "Negatif Enerji Dengesizlik Maliyeti (TL/MWh)", "variable":""},
                            template="plotly_white")

yearly_negative_edmal_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),
)


yearly_negative_edmal_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_negative_edmal_fig.update_xaxes(dtick=1)
yearly_negative_edmal_fig.update_yaxes(range=[15, 400])

yearly_negative_edmal_fig.update_traces(name="2021", selector=dict(name="2021 -EDMal"))
yearly_negative_edmal_fig.update_traces(name="2022", selector=dict(name="2022 -EDMal"))
yearly_negative_edmal_fig.update_traces(name="2023", selector=dict(name="2023 -EDMal"))

yearly_negative_edmal_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

# aylık  ortalama +edmal/ptf grafiği
yearly_positive_edmal_ptf_fig = px.line(yearly_price, x="Ay", y=["2021 +EDMal/PTF","2022 +EDMal/PTF","2023 +EDMal/PTF"],
                            title='Yıllara Göre Pozitif Enerji Dengesizlik Maliyetinin PTF''ye Oranı',
                            labels={"value": "+EDMal/PTF", "variable":""},
                            template="plotly_white")

yearly_positive_edmal_ptf_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)

yearly_positive_edmal_ptf_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_positive_edmal_ptf_fig.update_xaxes(dtick=1)
yearly_positive_edmal_ptf_fig.update_yaxes(range=[0, 0.3])

yearly_positive_edmal_ptf_fig.update_traces(name="2021", selector=dict(name="2021 +EDMal/PTF"))
yearly_positive_edmal_ptf_fig.update_traces(name="2022", selector=dict(name="2022 +EDMal/PTF"))
yearly_positive_edmal_ptf_fig.update_traces(name="2023", selector=dict(name="2023 +EDMal/PTF"))

yearly_positive_edmal_ptf_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Aylık ortalama Birim Pozitif Enerji Dengesizlik Maliyetinin, aynı aya ait Piyasa Takas Fiyatı" +"<br>" + "ortalamasına oranı gösterilmektedir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

yearly_positive_edmal_ptf_fig.update_layout(margin=dict(t=40, b=120))


yearly_positive_edmal_ptf_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

# aylık  ortalama -edmal/ptf grafiği
yearly_negative_edmal_ptf_fig = px.line(yearly_price, x="Ay", y=["2021 -EDMal/PTF","2022 -EDMal/PTF","2023 -EDMal/PTF"],
                            title='Yıllara Göre Negatif Enerji Dengesizlik Maliyetinin PTF''ye Oranı',
                            labels={"value": "-EDMal/PTF", "variable":""},
                            template="plotly_white")

yearly_negative_edmal_ptf_fig.update_layout(    
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
)

yearly_negative_edmal_ptf_fig.update_xaxes(range=[1, 12], constrain='domain')
yearly_negative_edmal_ptf_fig.update_xaxes(dtick=1)
yearly_negative_edmal_ptf_fig.update_yaxes(range=[0, 0.3])

yearly_negative_edmal_ptf_fig.update_traces(name="2021", selector=dict(name="2021 -EDMal/PTF"))
yearly_negative_edmal_ptf_fig.update_traces(name="2022", selector=dict(name="2022 -EDMal/PTF"))
yearly_negative_edmal_ptf_fig.update_traces(name="2023", selector=dict(name="2023 -EDMal/PTF"))

yearly_negative_edmal_ptf_fig.add_annotation(
    xref="paper",
    yref="paper",
    x=-0,
    y=-0.25,
    text="<i>Aylık ortalama Birim Negatif Enerji Dengesizlik Maliyetinin, aynı aya ait Piyasa Takas Fiyatı" + 
    "<br>" + "ortalamasına oranı gösterilmektedir.</i>",
    showarrow=False,
    font=dict(color="#73777B", size=10,family="Arial"),
    align="left",
    yanchor="top",
    xanchor="left",
)

yearly_negative_edmal_ptf_fig.update_layout(margin=dict(t=40, b=120))


yearly_negative_edmal_ptf_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))
# Akarsu Kapasite Faktörü

akarsu_kf_2021 = get_river_capacity_factor("2021-01-01","2021-12-31")
akarsu_kf_2022 = get_river_capacity_factor("2022-01-01","2022-12-31")
akarsu_kf_2023 = get_river_capacity_factor("2023-01-01",today)

akarsu_kf = pd.DataFrame(columns=["Ay","2021","2022","2023"])
akarsu_kf_2021 = akarsu_kf_2021.set_index("Tarih")

akarsu_kf_2021 = akarsu_kf_2021.reset_index(drop=True)
akarsu_kf_2022 = akarsu_kf_2022.reset_index(drop=True)
akarsu_kf_2023 = akarsu_kf_2023.reset_index(drop=True)
akarsu_kf["Ay"] = akarsu_kf_2021.index + 1
akarsu_kf["2021"] = akarsu_kf_2021["Kapasite Faktörü"]
akarsu_kf["2022"] = akarsu_kf_2022["Kapasite Faktörü"]
akarsu_kf["2023"] = akarsu_kf_2023["Kapasite Faktörü"]
akarsu_kf["Uzun Yıllar Ort."] = [0.22,0.28,0.4,0.52,0.49,0.35,0.21,0.16,0.14,0.14,0.13,0.17]


akarsu_kf

akarsu_kf_fig = px.line(akarsu_kf, x="Ay", y=["2021","2022","2023"],
                            title='Yıllara Göre Akarsu Kapasite Faktörü İstatistiği',
                            labels={"value": "Kapasite Faktörü", "variable":""},
                            template="plotly_white",)

akarsu_kf_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),

)

#add Uzun Yıllar Ort. line
akarsu_kf_fig.add_scatter(x=akarsu_kf["Ay"], y=akarsu_kf["Uzun Yıllar Ort."], name="Uzun Yıllar Ort.", mode="lines",line=dict(color="black", dash="dash"))

akarsu_kf_fig.update_xaxes(range=[1, 12], constrain='domain')
akarsu_kf_fig.update_xaxes(dtick=1)
akarsu_kf_fig.update_yaxes(range=[0, 1])

akarsu_kf_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))

# Rüzgar Kapasite Faktörü

rüzgar_kf_2021 = get_wind_capacity_factor("2021-01-01","2021-12-31")
rüzgar_kf_2022 = get_wind_capacity_factor("2022-01-01","2022-12-31")
rüzgar_kf_2023 = get_wind_capacity_factor("2023-01-01",today)

rüzgar_kf = pd.DataFrame(columns=["Ay","2021","2022","2023"])
rüzgar_kf_2021 = rüzgar_kf_2021.set_index("Tarih")

rüzgar_kf_2021 = rüzgar_kf_2021.reset_index(drop=True)
rüzgar_kf_2022 = rüzgar_kf_2022.reset_index(drop=True)
rüzgar_kf_2023 = rüzgar_kf_2023.reset_index(drop=True)

rüzgar_kf["Ay"] = rüzgar_kf_2021.index + 1
rüzgar_kf["2021"] = rüzgar_kf_2021["Kapasite Faktörü"]
rüzgar_kf["2022"] = rüzgar_kf_2022["Kapasite Faktörü"]
rüzgar_kf["2023"] = rüzgar_kf_2023["Kapasite Faktörü"]
rüzgar_kf["Uzun Yıllar Ort."] = [0.37,0.37,0.36,0.29,0.26,0.28,0.42,0.42,0.32,0.29,0.32,0.35]

rüzgar_kf_fig = px.line(rüzgar_kf, x="Ay", y=["2021","2022","2023"],
                            title='Yıllara Göre Rüzgar Kapasite Faktörü İstatistiği',
                            labels={"value": "Kapasite Faktörü", "variable":""},
                            template="plotly_white")

#add Uzun Yıllar Ort. line, color black, dashed
rüzgar_kf_fig.add_scatter(x=rüzgar_kf["Ay"], y=rüzgar_kf["Uzun Yıllar Ort."], name="Uzun Yıllar Ort.", mode="lines", line=dict(color="black", dash="dash"))

rüzgar_kf_fig.update_layout(
    legend=dict(
        orientation="h",  # Yatay (horizontal) legend
        x=0.5,  # Legendi grafiğin ortasına hizala
        y=-0.15,  # X ekseni başlığından biraz daha aşağıda
        xanchor="center",  # X eksenindeki hizalamayı ortala
    ),
    width=625,
    height=475,
    margin=dict(t=40, b=120),

)

rüzgar_kf_fig.update_xaxes(range=[1, 12], constrain='domain')
rüzgar_kf_fig.update_xaxes(dtick=1)
rüzgar_kf_fig.update_yaxes(range=[0, 1])

rüzgar_kf_fig.add_layout_image(
    dict(
        source=watermark_src,
        xref="paper", yref="paper",
        x=0.5, y=0.5,  # Resmi ortala
        sizex=1.5, sizey=1.5,  # Resmin boyutunu ayarla
        xanchor="center", yanchor="middle",  # Resmin konumunu ayarla
        opacity=0.05,  # Resmi yarı şeffaf yap
    ))




#####################################################
fiyat = html.Div([
                    html.Div(style={"width":"50vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("Fiyat Raporu",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="fiyat")

yük = html.Div([    
                    html.Div(style={"width":"50vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("Üretim ve Talep Raporu",style={"color":"#285A84",
                                                 "position":"relative",})
                ],id="load")

dgp = html.Div([
                    html.Div(style={"width":"50vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("DGP ve GİP Raporu (D-1)",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="dgp")

yıllık = html.Div([
                    html.Div(style={"width":"50vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H3("Yıllık Raporlar",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="yıllık")

açıklamalar = html.Div([
                    html.Div(style={"width":"50vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H6("Açıklamalar ve Sorumluluk Reddi",style={"color":"#285A84",
                                                 "position":"relative",}),
                ],id="açıklamalar")

rapor_ismi = html.Div([
                    html.Div(style={"width":"50vw","height":"100px","background-color":"#285A84","position":"relative","top":"-50000px"}),
                    html.H1("Türkiye Elektrik Piyasası Raporu",style={"color":"#E13915",
                                                 "position":"relative",}),
                ],id="rapor_ismi")

#format rapor tarihi


nav_contents = [
    html.Ul(
        [   
            html.Li(html.A(
                        html.Img(src="https://www.gainenerji.com/wp-content/uploads/2022/10/gain-20-web.png",
                                 style={"width":"55%","height":"auto"},
                                 ),href="https://www.gainenerji.com/",target="_blank"
                        ),
                        style={"display":"inline-block",
                               "float":"left"}),
                                
            html.Li(html.Div(["Rapor Tarihi",html.Br(),rapor_tarihi],
                                    style={"display":"inline-block",
                                            "margin-top":"0px",
                                            "margin-right":"20px",
                                            "text-decoration":"none",
                                            "float":"left",
                                            "align":"center",
                                            "color":"#0d1f2e",},
                                            )),

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

app.title = 'Gain Enerji - Türkiye Elektrik Piyasası Raporu'

server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = dbc.Container(
    # Set size of the app 1920*1080
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
                        rapor_ismi,
                    ],style={"margin-bottom":"-15px","margin-top":"-10px"}
                    ),
            ]
        ),
        dbc.Row(
            [
            dbc.Col(
                [
                    fiyat
                ]
                ),
            ],
        style={"margin-bottom":"10px","margin-top":"-70px",}
        ),

        dbc.Row(
            dbc.Col(html.H5("Piyasa Takas Fiyatı (PTF) İstatistikleri",style={"color":"#323232","margin-bottom":"10px"})),
        ),

        dbc.Row(
            [
                dbc.Col(
                [   
                    html.Div(
                            [
                                table_avg_new,
                            ], style={"margin-bottom":"10px"}
                            ),

                    html.Div
                    (
                        [
                            table_new,
                            html.P("D rapor tarihini, D-1 ve D+1 ise sırasıyla rapor tarihinden önceki ve sonraki günü ifade eder.",style={"font-size":"10px","color":"#73777B","margin-top":"20px","font-style":"italic"}),
                            html.P([
                                    "Saatlik PTF değerleri ",
                                    html.B("TL/MWh"),
                                     " cinsindendir."
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),
                        ],
                        style={}
                    ),
                ],width=4),
                

                dbc.Col([

                    dbc.Row(
                        dbc.Col([
                            dcc.Graph(figure = ptf_fig, style={"margin-top":"-50px","margin-left":"50px"}),
                        ],width=12,style={"margin-bottom":"40px"})
                    ),

                    dbc.Row(
                        dbc.Col(
                            dcc.Graph(figure = fig, style={"margin-left":"50px"}),
                        )
                    ),
                

                    ],style={"margin-bottom":"10px"},width=8),
            
            ],
        ),

        dbc.Row(
            dbc.Col(html.H5("Son 4 Haftaya Ait Günlük PTF ve Tüketim Değerleri",style={"color":"#323232","margin-bottom":"10px","margin-top":"30px"})),
        ),
        dbc.Row(
            [dbc.Col(
                [
                 table_week,
                ], width=12
            ),
            html.Hr(style={"margin-bottom":"50px","margin-top":"50px"}),
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
                    dcc.Graph(figure = load_fig,style={"padding-bottom":"40px","margin-bottom":"30px",}), dcc.Graph(figure = coal_kgup_fig,style={"padding-bottom":"40px","margin-bottom":"30px"})
                ]
                )),

                dbc.Col(html.Div(
                [
                    dcc.Graph(figure = production_fb_fig,style={"padding-bottom":"40px","margin-bottom":"30px","margin-left":"20px"}), dcc.Graph(figure = kalan_yük_fig, style={"margin-left":"20px"})
                ],
                style={"margin-bottom":"50px"}
                )),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Kaynaklara Göre Gerçekleşen Üretim Miktarı (D-1)",style={"color":"#323232","margin-bottom":"10px"}),
                        html.Div([table_production_T]),
                        html.P(["Üretim değeri ",
                               html.B("MWh"),
                               ",kurulu güç değerleri",
                               html.B("MW"),
                               "cinsindendir"],
                               style={"font-size":"10px","color":"#73777B","margin-top":"20px","font-style":"italic"}),
                        html.P("Lisanssız güneş enerjisi santrallerinin gerçekleşen üretim değerleri gecikmeli olarak yayımlanmakta ve bu nedenle tabloda gösterilememektedir.",style={"font-size":"10px","color":"#73777B","margin-top":"-10px","font-style":"italic"}),
                    ],
                    style={"margin-top":"50px"}
                ),

                dbc.Col(html.Div(
                    [
                        dcc.Graph(figure = production_T_pie)
                    ],style={}),
                    width=6,
                ),
                html.Hr(style={"margin-bottom":"50px"}),
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
                          table_dgp_new,
                          html.P([
                                    "Tablo, rapor tarihinden bir gün önceki verileri içermekte olup, fiyat verileri ",
                                    html.B("TL/MWh,"),
                                    " hacim verileri.",
                                    html.B(" MWh,"),
                                    " cinsindendir."
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"20px","font-style":"italic"}),
                          html.P([  
                                    html.B("PTF,"),
                                    " Piyasa Takas Fiyatını; ",
                                    html.B("SMF,"),
                                    " Sistem Mütakabat Fiyatını ifade etmektedir.",
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),
                          html.P([  
                                    html.B("GİP İşlem Hacmi,"),
                                    " saatlik tahtada gerçekleşen toplam GİP işlem miktarıdır.",
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),
                          html.P([  
                                    html.B("GİP AOF,"),
                                    " saatlik tahtada gerçekleşen GİP işlemlerinin ağırlıklı ortalama fiyatıdır.",
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),
                          html.P([  
                                    html.B("GİP Min 200 MWh,"),
                                    " saatlik tahtada gerçekleşen en düşük fiyatlı ilk 200 MWh'lik işlemin ağırlıklı ortalama fiyatıdır.",
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),      
                          html.P([  
                                    html.B("GİP Max 200 MWh,"),
                                    " saatlik tahtada gerçekleşen en yüksek fiyatlı ilk 200 MWh'lik işlemin ağırlıklı ortalama fiyatıdır.",
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),
                          html.P([  
                                    html.B("YAL (Yük Al)"),
                                    " sistemde enerji açığı olduğunu, ",
                                    html.B("YAT (Yük At)"),
                                    " sistemde enerji fazlası olduğunu, ",
                                    html.B("DNG (Denge)"),
                                    " sistemin dengede olduğunu gösterir."
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),
                          html.P([  
                                    html.B("Net Talimat Hacmi,"),
                                    " TEİAŞ tarafından ilgili saatte verilen tüm YAL (pozitif) ve YAT (negatif) talimatlarının toplamıdır.",
                                    ], style={"font-size": "10px", "color": "#73777B","margin-top":"-10px","font-style":"italic"}),

                        ],
                        style={"margin-bottom":"30px"}
                          ),
                ],width=12
                
              ),
            ]
        ),
        dbc.Row(
            [dbc.Col(
                html.Div(
                    [
                        dcc.Graph(figure = edmal_fig,style={"margin-bottom":"30px"})
                    ]),
                    width=6,
            ),
            dbc.Col(
                html.Div(
                    [
                        dcc.Graph(figure = makas_fig,style={"margin-bottom":"30px","margin-left":"20px"})
                    ]),
                    width=6,
            ),]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(figure = gip_fig)
                        ]
                    ),
                ),

                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(figure=ptf_smf_fig,style={"margin-left":"20px"})
                        ]
                    )
                ),

                html.Hr(style={"margin-bottom":"50px","margin-top":"50px"}),
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
                          dcc.Graph(figure = akarsu_kf_fig),
                          dcc.Graph(figure = yearly_positive_edmal_fig),
                          dcc.Graph(figure = yearly_positive_edmal_ptf_fig),
                          
                        ],
                        style={}
                          ),
                ],
                style={"margin-bottom":"30px"},
                
              ),

                dbc.Col(html.Div(
                    [   
                        dcc.Graph(figure = yearly_price_usd_fig, style={"margin-left":"20px"}),
                        dcc.Graph(figure = rüzgar_kf_fig, style={"margin-left":"20px"}),
                        dcc.Graph(figure = yearly_negative_edmal_fig, style={"margin-left":"20px"}),
                        dcc.Graph(figure = yearly_negative_edmal_ptf_fig, style={"margin-left":"20px"}),
                    ]),
                style={"margin-bottom":"10px"},
                ),

             html.Hr()
            ]
        ),

        dbc.Row(
            dbc.Col(
                [
                    açıklamalar,
                    html.P("Bu Türkiye Elektrik Piyasası Raporu ('Rapor'), Gain Enerji Ticaret A.Ş. ('Gain') tarafından Enerji Piyasaları İşletme A.Ş. (EPİAŞ) ve Türkiye Elektrik İletim A.Ş. (TEİAŞ) tarafından kamuya açık biçimde yayımlanan veriler kullanılarak oluşturulmuştur. Gain, Rapordaki bilgilerin doğruluğu ve bütünlüğü konusunda herhangi bir garanti vermemektedir.",style={"font-size":"12px","color":"#73777B","margin-top":"-5px","font-style":"italic"}),
                    html.P("Rapor, yalnızca bilgi vermek amacıyla hazırlanmış olup, yatırım tavsiyesi niteliği taşımamaktadır.  Bu raporun içeriğinin kullanılması sonucunda ortaya çıkabilecek her türlü maddi/manevi zarar ve kayıplardan dolayı Gain sorumlu tutulamaz.",style={"font-size":"12px","color":"#73777B","margin-top":"-10px","font-style":"italic"}),
                    html.P("Raporda yer alan görseller, Gain'in yazılı izni olmaksızın kısmen veya tamamen kopyalanamaz.",style={"font-size":"12px","color":"#73777B","margin-top":"-10px","font-style":"italic"}),
                ],
            )

        )
    

    ]),style={"width":"1920px","height":"1080px","background-color":"white"},


)


if __name__ == '__main__':
    app.run(debug=True)