import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator

# Descargar datos de PETR4 desde enero 2024 hasta hoy
dados = yf.download("PETR4.SA", start="2024-01-01")

# Calcular media móvil de 20 días
dados["Media_20"] = dados["Close"].rolling(window=20).mean()

# Asegurar que sea una Serie válida
close_series = dados["Close"].squeeze()


# Calcular RSI de 14 días
rsi_calc = RSIIndicator(close=close_series, window=14)
dados["RSI"] = rsi_calc.rsi()

# --- GRÁFICO 1: Preço + Média Móvel ---
plt.figure(figsize=(12, 6))
plt.plot(dados["Close"], label="Preço de Fechamento")
plt.plot(dados["Media_20"], label="Média Móvel 20 dias", linestyle="--")
plt.title("PETR4 - Análise com Média Móvel")
plt.xlabel("Data")
plt.ylabel("Preço (R$)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- GRÁFICO 2: RSI ---
plt.figure(figsize=(12, 4))
plt.plot(dados["RSI"], label="RSI 14 dias", color="purple")
plt.axhline(70, linestyle='--', color='red', label='Sobrecompra (70)')
plt.axhline(30, linestyle='--', color='green', label='Sobrevenda (30)')
plt.title("PETR4 - Índice de Força Relativa (RSI)")
plt.xlabel("Data")
plt.ylabel("RSI")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()





