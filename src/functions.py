import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import datetime
import pytz
from ortak import *


class Kontrat:
    def __init__(self,name,table):
        self.name = name
        self.table = table

def ptf_smf(start_date,end_date):
    url = "market/" + "mcp-smp" + "?startDate=" + start_date + "&endDate=" + end_date
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    corresponding_url = main_url + url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()

    df = pd.DataFrame(json["body"]["mcpSmps"])
    df.rename(index=str,columns={"date":"Tarih","mcp": "PTF", "smp": "SMF", "smpDirection": "Sistem Yönü", "smpDirection": "Sistem Yönü" },inplace=True)
    df['Tarih'] = pd.to_datetime(df['Tarih']).dt.tz_localize(None)
    df = df.reset_index(drop=True)
    return df

def parse_contract(df):
    kontrat_liste = []
    for kontrat in df["Kontrat Adı"].unique():
        kontrat_liste.append(Kontrat(kontrat,df[df["Kontrat Adı"] == kontrat]))
        
    return kontrat_liste


def get_order(start_date,end_date):
    url = "market/" + "bpm-order-summary" + "?startDate=" + start_date + "&endDate=" + end_date
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    corresponding_url = main_url + url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()

    df = pd.DataFrame(json["body"]["bpmOrderSummaryList"])
    df.rename(index=str,columns={"date":"Tarih","mcp": "PTF", "smp": "SMF", "smpDirection": "Sistem Yönü", "smpDirection": "Sistem Yönü" },inplace=True)
    df['Tarih'] = pd.to_datetime(df['Tarih']).dt.tz_localize(None)
    df = df.reset_index(drop=True)

    # Tarih sütunundaki tarihlerin saat değerlerini yeni sütun olarak ekle
    df['Saat'] = df['Tarih'].dt.strftime('%H')
    df['Tarih Datetime'] = df['Tarih']
    df['Tarih'] = df['Tarih'].dt.strftime('%d-%m-%Y')

    # Sütun isimleri değiştir
    df = df.rename(columns={"net": "Net Talimat", "direction": "Sistem Yönü", "upRegulationDelivered": "YAL Miktarı", "downRegulationDelivered": "YAT Miktarı"})

    # Bazı sütunları at
    df = df.drop(columns=['upRegulationZeroCoded', 'upRegulationOneCoded', 'upRegulationTwoCoded', 'downRegulationZeroCoded', 'downRegulationOneCoded','downRegulationTwoCoded',"nextHour"])

    #Sistem yönü sütunundaki değerleri değiştir
    df['Sistem Yönü'] = df['Sistem Yönü'].replace({'ENERGY_SURPLUS': 'YAT', 'ENERGY_DEFICIT': 'YAL', 'IN_BALANCE': 'DNG'})

    # Sıralı sütunları düzenle
    df = df[['Tarih Datetime','Tarih', 'Saat','Net Talimat','YAL Miktarı','YAT Miktarı', "Sistem Yönü"]]

    return df

def get_load_forecast(start_date,end_date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "consumption/" + "load-estimation-plan" + "?startDate=" + start_date + "&endDate=" + end_date
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    json
    df = pd.DataFrame(json["body"]["loadEstimationPlanList"])

    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "consumption/" + "real-time-consumption" + "?startDate=" + start_date + "&endDate=" + end_date
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    json
    if json['body']["hourlyConsumptions"] == []:
        consumption = pd.DataFrame(columns=["Datetime","Tüketim"])
        consumption["Datetime"] = pd.date_range(start=start_date,end=end_date,freq="H")
        consumption["Tüketim"] = np.nan
    else:
        consumption = pd.DataFrame(json['body']["hourlyConsumptions"])
        consumption = consumption.rename(columns={"date":"Datetime","consumption":"Tüketim"})
        #datetime formatına çevrildi
        consumption["Datetime"] = pd.to_datetime(consumption["Datetime"])
        target_timezone = pytz.timezone("Europe/Istanbul")
        consumption["Datetime"] = consumption["Datetime"].apply(lambda x: x.replace(tzinfo=pytz.UTC).astimezone(target_timezone))
        consumption = consumption.set_index("Datetime")
    #rename columns
    df = df.rename(columns={"date":"Datetime","lep":"Yük Tahmini"})
    #Datetime sütunu datetime formatına çevrildi. Her bir saat UTC +3 formatında değiştirildi
    df["Datetime"] = pd.to_datetime(df["Datetime"])
        #Datetime sütunundan gün ve saat bilgileri ayrıldı
    df["Tarih"] = df["Datetime"].dt.date
    df["Saat"] = df["Datetime"].dt.time
    #Saat sütunundaki tarihlerin saat bilgileri alındı
    df["Saat"] = df["Saat"].astype(str).str[0:2]
    #saat sütunu int formatına çevrildi
    df["Saat"] = df["Saat"].astype(int)
    #Tarih sütunu değerleri string formatına çevrildi
    df["Tarih"] = df["Tarih"].astype(str)

    target_timezone = pytz.timezone("Europe/Istanbul")
    df["Datetime"] = df["Datetime"].apply(lambda x: x.replace(tzinfo=pytz.UTC).astimezone(target_timezone))

    
    #Datetime sütunu index olarak atandı
    df = df.set_index("Datetime")
    
    #sütunların sırası değiştirildi
    df = df[["Tarih","Saat","Yük Tahmini"]]
    df["Tüketim"] = consumption["Tüketim"]
    return df

def get_res_forecast(start_date,end_date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "production/" + "wpp-generation-and-forecast" + "?startDate=" + start_date + "&endDate=" + end_date
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    json
    df = pd.DataFrame(json['body']["data"])

    #drop unnecessary columns
    df = df.drop(columns=["quarter1","quarter2","quarter3","quarter4","createIp","modifyIp"])
    #rename columns
    df = df.rename(columns={"effectiveDate":"Datetime","generation":"Üretim","forecast":"Tahmin"})

    #convert Datetime column to datetime format
    df["Datetime"] = pd.to_datetime(df["Datetime"])

        #Datetime sütununu Tarih ve Saat olarak ikiye ayırma
    df["Tarih"] = df["Datetime"].dt.date
    df["Saat"] = df["Datetime"].dt.time
    #Saat sütunu sadece saat olarak gösterilecek
    df["Saat"] = df["Saat"].astype(str).str[:2]
    #saat sütunu int formatına çevrildi
    df["Saat"] = df["Saat"].str.replace(":","").astype(int)
    #Tarih sütunu string formatına çevrildi
    df["Tarih"] = df["Tarih"].astype(str)

    #Datetime sütunu datetime formatına çevrildi. Her bir saat UTC +3 formatında değiştirildi
    target_timezone = pytz.timezone("Europe/Istanbul")
    df["Datetime"] = df["Datetime"].apply(lambda x: x.replace(tzinfo=pytz.UTC).astimezone(target_timezone))
    # set timezome to europe istanbul
    df["Datetime"] = df["Datetime"].dt.tz_convert("Europe/Istanbul")

    #set Datetime column as index
    df = df.set_index("Datetime")

    #sütunları yeniden sırala
    df = df[["Tarih","Saat","Üretim","Tahmin"]]
    return df

def get_real_time_production(start_date,end_date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "production/" + "real-time-generation" + "?startDate=" + start_date + "&endDate=" + end_date
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    df = pd.DataFrame(json["body"]["hourlyGenerations"])
    return df

def get_real_time_consumption(start_date,end_date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "consumption/" + "real-time-consumption" + "?startDate=" + start_date + "&endDate=" + end_date
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    json
    df = pd.DataFrame(json["body"]["hourlyConsumptions"])
    #rename columns
    df = df.rename(columns={"date":"Datetime","consumption":"Tüketim"})
    #Datetime sütununu Tarih ve Saat olarak ikiye ayırma
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df["Tarih"] = df["Datetime"].dt.date
    df["Saat"] = df["Datetime"].dt.time
    #Saat sütunu sadece saat olarak gösterilecek
    df["Saat"] = df["Saat"].astype(str).str[:2]
    #saat sütunu int formatına çevrildi
    df["Saat"] = df["Saat"].str.replace(":","").astype(int)
    #Tarih sütunu string formatına çevrildi
    df["Tarih"] = df["Tarih"].astype(str)
    #datetime sütunu utc +3 formatına çevrildi
    target_timezone = pytz.timezone("Europe/Istanbul")
    df["Datetime"] = df["Datetime"].apply(lambda x: x.replace(tzinfo=pytz.UTC).astimezone(target_timezone))
    # set timezome to europe istanbul
    df["Datetime"] = df["Datetime"].dt.tz_convert("Europe/Istanbul")
    #set Datetime column as index
    df = df.set_index("Datetime")
    #sütunları yeniden sırala
    df = df[["Tarih","Saat","Tüketim"]]
    return df

def get_block_offers(start_date,end_date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "market/" + "amount-of-block" + "?startDate=" + start_date + "&endDate=" + end_date
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    df = pd.DataFrame(json["body"]["amountOfBlockList"])
    #rename columns
    df = df.rename(columns={"date": "Datetime", "amountOfPurchasingTowardsBlock": "Toplam Blok Alış Miktarı ", "amountOfPurchasingTowardsMatchBlock": "Eşleşen Blok Alış Miktarı", "amountOfSalesTowardsBlock": "Toplam Blok Satış Miktarı", "amountOfSalesTowardsMatchBlock": "Eşleşen Blok Satış Miktarı"})
    #convert date column to datetime
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    # Datetime sütununun tarih ve saat bilgilerini ayrı ayrı sütunlara ayırma
    df["Tarih"] = df["Datetime"].dt.date
    df["Saat"] = df["Datetime"].dt.time
    # Tarih ve saat sütunları stringe dönüştürme
    df["Tarih"] = df["Tarih"].astype(str)
    df["Saat"] = df["Saat"].astype(str)
    # Saat sütunu sadece saat bilgisini içerdiği için ":" karakterini silme ve ilk iki karakteri alarak saat bilgisini elde etme
    df["Saat"] = df["Saat"].str.replace(":", "").str[:2]
    #datetime sütunu utc +3 formatına çevrildi
    target_timezone = pytz.timezone("Europe/Istanbul")
    df["Datetime"] = df["Datetime"].apply(lambda x: x.replace(tzinfo=pytz.UTC).astimezone(target_timezone))
    # set timezome to europe istanbul
    df["Datetime"] = df["Datetime"].dt.tz_convert("Europe/Istanbul")
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.set_index("Datetime")
    # sütunları yeniden sıralama
    df = df[["Tarih", "Saat", "Toplam Blok Alış Miktarı ", "Eşleşen Blok Alış Miktarı", "Toplam Blok Satış Miktarı", "Eşleşen Blok Satış Miktarı"]]
    return df


def daily_market_summary(date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "compare/" + "market" + "?date=" + date + "&type=" + "DAILY"
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    json
    df = pd.DataFrame(json['body']["marketCompares"])
    df = df.loc[1]
    return df

def ptf(start_date,end_date):
    url = "market/" + "day-ahead-mcp" + "?startDate=" + start_date + "&endDate=" + end_date
    json = make_request(url)
    df = pd.DataFrame(json["body"]["dayAheadMCPList"])
    df.rename(index=str,columns={"date":"Tarih","price": "Fiyat (TL)", "priceUsd": "Fiyat (USD)", "priceEur": "Fiyat (EUR)" },inplace=True)
    df['Tarih'] = pd.to_datetime(df['Tarih']).dt.tz_localize(None)
    df = df.reset_index(drop=True)
    return df

def fiyat_max(row):
    if row['PTF'] > row['SMF']:
        return row['PTF']
    elif row['PTF'] < row['SMF']:
        return row['SMF']
    else:
        return row['PTF']
   
# Min Fiyat Bulan Fonksiyon #
def fiyat_min(row):
    if row['PTF'] > row['SMF']:
        return row['SMF']
    elif row['PTF'] < row['SMF']:
        return row['PTF']
    else:
        return row['PTF']

def change_currency(currency,df):
    date = df["Tarih"].iloc[0]
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    a = ptf(date,date)
    usd_tl = a["Fiyat (TL)"].loc[0] / a["Fiyat (USD)"].loc[0]
    eur_tl = a["Fiyat (TL)"].loc[0] / a["Fiyat (EUR)"].loc[0]

    if currency == "USD":
        table = df.copy()
        table["PTF"] = df["PTF"]/usd_tl
        table["SMF"] = df["SMF"]/usd_tl
        #Eğer df içerisinde +EDF (D-1) ve -EDF (D-1) sütunları varsa onları da döviz kuruna göre hesapla
        if len(df.columns) > 6:
            table["+EDF"] = df["+EDF"]/usd_tl
            table["-EDF"] = df["-EDF"]/usd_tl
        else:
            pass
    elif currency == "EUR":
        table = df.copy()
        table["PTF"] = df["PTF"]/eur_tl
        table["SMF"] = df["SMF"]/eur_tl
        if len(df.columns) > 6:
            table["+EDF"] = df["+EDF"]/eur_tl
            table["-EDF"] = df["-EDF"]/eur_tl
        else:
            pass
    else:
        pass
    # tüm değerleri 2 ondalık basamağa yuvarla
    table = table.round(2)

    return table

def get_euas_bilateral_sell_quantity(start_date,end_date):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    sub_url = "market/" + "bilateral-contract-sell" + "?startDate=" + start_date + "&endDate=" + end_date + "&eic=40X000000000195P"
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    df = pd.DataFrame(json["body"]["bilateralContractSellList"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date":"Tarih","quantity":"İA Satış Miktarı"})
    return df


