import os
import requests
import pandas as pd
from datetime import datetime
from io import StringIO
from ta.trend import MACD

# Obtener las variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Descargar datos del par USD/BRL desde el Banco Central (o fuente alternativa)
url = "https://raw.githubusercontent.com/datasets/exchange-rates/master/data/usd-brl.csv"
data = requests.get(url).text
df = pd.read_csv(StringIO(data))

# Asegurar nombres consistentes
df.rename(columns={"Date": "Date", "Value": "Close"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# Calcular MACD
macd = MACD(close=df["Close"])
df["MACD"] = macd.macd()
df["MACD_Signal"] = macd.macd_signal()

# Medias móviles
df["MM20"] = df["Close"].rolling(window=20).mean()
df["Volume"] = 1000  # valor fijo simulado
df["Volume_Mean"] = df["Volume"].rolling(window=20).mean()

# Función de decisión
def decision(row):
    if row["MACD"] > row["MACD_Signal"] and row["Close"] > row["MM20"] and row["Volume"] > row["Volume_Mean"]:
        return "📈 Comprar"
    elif row["MACD"] < row["MACD_Signal"] and row["Close"] < row["MM20"] and row["Volume"] > row["Volume_Mean"]:
        return "📉 Vender"
    else:
        return "⏳ Esperar"

# Aplicar decisión a la última fila
ultima = df.iloc[-1]
recomendacion = decision(ultima)
fecha = ultima.name.strftime("%Y-%m-%d")

# Formar mensaje
mensaje = f"📊 Análisis IA para el {fecha}:\n👉 {recomendacion}"

# Enviar mensaje al bot
url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
res = requests.post(url_api, data={"chat_id": CHAT_ID, "text": mensaje})

# Mostrar resultado
print("✅ Enviado:", res.ok)
print("📨 Respuesta:", res.json())
