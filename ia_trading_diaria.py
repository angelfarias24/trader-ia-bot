
import requests
import pandas as pd
from datetime import datetime
from io import StringIO
from ta.trend import MACD

# ======= CONFIGURA TUS DATOS AQUI =======
TOKEN = "TU_TOKEN_TELEGRAM"
CHAT_ID = "TU_CHAT_ID"
API_KEY = "CW8ZHIC5A9DKYDVQ"
# ========================================

# Descargar datos diarios de USD/BRL
url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=BRL&apikey={API_KEY}&datatype=csv"
res = requests.get(url)
dados = pd.read_csv(StringIO(res.text))

# Preprocesamiento
dados.rename(columns={"timestamp": "Date", "close": "Close"}, inplace=True)
dados["Date"] = pd.to_datetime(dados["Date"])
dados.sort_values("Date", inplace=True)
dados.reset_index(drop=True, inplace=True)

# Calcular indicadores
dados["MM20"] = dados["Close"].rolling(window=20).mean()
dados["MM50"] = dados["Close"].rolling(window=50).mean()
dados["Volume_Medio"] = dados["volume"].rolling(window=20).mean()
macd_calc = MACD(dados["Close"])
dados["MACD"] = macd_calc.macd()
dados["MACD_Sinal"] = macd_calc.macd_signal()

# Función de decisión de IA
def decision_ia(row):
    if row["MACD"] > row["MACD_Sinal"] and row["Close"] > row["MM20"] and row["volume"] > row["Volume_Medio"]:
        return "📈 COMPRAR"
    elif row["MACD"] < row["MACD_Sinal"] and row["Close"] < row["MM20"] and row["volume"] > row["Volume_Medio"]:
        return "📉 VENDER"
    else:
        return "⏳ ESPERAR"

# Obtener la fila del día anterior
ultima = dados.iloc[-1]
recomendacion = decision_ia(ultima)
fecha = ultima["Date"].strftime("%d/%m/%Y")

# Formar mensaje
mensaje = (
    f"📆 Análisis IA para el {fecha}:
"
    f"🔍 Recomendación: {recomendacion}
"
    f"🕗 Ejecutar operación entre 09:00 y 18:00 (hora Brasilia)
"
    f"📌 Evaluar cerrar posición antes de las 23:59
"
    f"#USD #BRL #TraderAngelBot"
)

# Enviar a Telegram
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})
