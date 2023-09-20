import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table,dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import dash_bootstrap_components as dbc
from functions import *
from dash import Input, Output, html

today = "2023-09-18"
yesterday = "2023-09-17"
tomorrow = "2023-09-19"

saat = pd.Series(range(0,24))

""" today = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d') """

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

yesterday_production = get_real_time_production(yesterday, yesterday)
today_production = get_real_time_production(today, today)
tomorrow_production = get_real_time_production(tomorrow, tomorrow)

yesterday_production = yesterday_production.reset_index(drop=True)
today_production = today_production.reset_index(drop=True)
tomorrow_production = tomorrow_production.reset_index(drop=True)

df_production_fb = pd.DataFrame(columns=['Saat', 'Üretim (D-1)',"Üretim (D)","Üretim (D+1)"])
df_production_fb["Saat"] = saat
df_production_fb["Üretim (D-1)"] = yesterday_production["river"] + yesterday_production["wind"] + yesterday_production["sun"] + yesterday_production["geothermal"] + yesterday_production["biomass"]
df_production_fb["Üretim (D)"] = today_production["river"] + today_production["wind"] + today_production["sun"] + today_production["geothermal"] + today_production["biomass"]
df_production_fb["Üretim (D+1)"] = tomorrow_production["river"] + tomorrow_production["wind"] + tomorrow_production["sun"] + tomorrow_production["geothermal"] + tomorrow_production["biomass"]

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
                     barmode="group",)


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
                               
            html.Li("Rapor Tarihi: 18.09.2023",
                                    style={"display":"inline-block",
                                            "margin-top":"10px",
                                            "margin-right":"20px",
                                            "color":"black",
                                            "text-decoration":"none",
                                            "float":"left"},
                                            ),

            html.Li(html.A("Yıllık Raporlar", href="#dgp",
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
                dbc.Col(html.Div(
                [
                    table_new,table_avg_new
                ]
            )),

            dbc.Col([dcc.Graph(figure = ptf_fig),dcc.Graph(figure=ptf_smf_fig)],width=8),
            html.Hr(),
            ],
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
                    dcc.Graph(figure = load_fig), dcc.Graph(figure = euas_sell_fig)
                ]
                )),

                dbc.Col(html.Div(
                [
                    dcc.Graph(figure = production_fb_fig), dcc.Graph(figure = kalan_yük_fig)
                ]
                )),
                html.Hr(),
            ]
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
                  html.Div([table_dgp_new])
              ),

              dbc.Col(html.Div(
                    [
                        dcc.Graph(figure = edmal_fig)
                    ]),
                    width=8,
                ),
              html.Hr(),
            ]
        )
    ])
)


if __name__ == '__main__':
    app.run(debug=True)