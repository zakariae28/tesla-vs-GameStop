import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import warnings
import matplotlib.pyplot as plt
# Ignorer toutes les alertes
warnings.filterwarnings("ignore", category=FutureWarning)
def download_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Page web téléchargée avec succès.")
        return response.text
    else:
        print(f"Échec du téléchargement de la page. Code d'état : {response.status_code}")
        return None
def parse_revenue_table(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find('table')
    revenue_data = pd.read_html(str(table))[0]
    revenue_data.columns = ['Date', 'Revenue']
    revenue_data['Revenue'] = revenue_data['Revenue'].replace('[\$,]', '', regex=True).astype(float)
    return revenue_data
def plot_stock_and_revenue(stock_data, revenue_data, stock):
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Date'], stock_data['Close'].astype("float"), label="Cours de l'action")
    plt.title("Historique du cours de l'action")
    plt.xlabel("Date")
    plt.ylabel("Prix ($US)")
    plt.subplot(2, 1, 2)
    plt.plot(revenue_data['Date'], revenue_data['Revenue'].astype("float"), label="Revenus")
    plt.title("Historique des revenus")
    plt.xlabel("Date")
    plt.ylabel("Revenus ($US Millions)")
    plt.tight_layout()
    plt.suptitle(stock, y=1.02, fontsize=16)
    plt.show()
def plot_revenue(x_data, y_data, stock):
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, label=stock)
    plt.title(stock)
    plt.xlabel("Date")
    plt.ylabel("Revenue ($US Millions)")
    plt.show()
# Créer un objet Ticker pour Tesla
tesla_ticker = yf.Ticker("TSLA")
# Obtenir les données historiques de Tesla pour la dernière année
tesla_data_1y = tesla_ticker.history(period="1y")
# Obtenir les données historiques de Tesla pour la période maximale disponible
tesla_data_max = tesla_ticker.history(period="max")
# Sauvegarder les données historiques dans un DataFrame nommé 'tesla_data'
tesla_data_max.to_csv('tesla_data.csv', encoding='utf-8')
# Réinitialiser l'index du DataFrame tesla_data sur place
tesla_data_max.reset_index(inplace=True)
# URL de la page web
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
# Télécharger le contenu de la page web
html_data = download_webpage(url)
if html_data:
    # Analyser le tableau de revenus
    tesla_revenue = parse_revenue_table(html_data)
    # Afficher le DataFrame résultant
    print("Test revenu est :", tesla_revenue.tail())
    # Enregistrer le DataFrame dans un fichier CSV
    tesla_revenue.to_csv('tesla_revenue.csv', index=False)
    # Utiliser la fonction plot_stock_and_revenue avec les données de Tesla
    plot_stock_and_revenue(tesla_data_max, tesla_revenue, 'TSLA')
    # Utiliser la fonction plot_revenue avec les données de Tesla
    plot_revenue(tesla_revenue['Date'], tesla_revenue['Revenue'], 'Tesla Revenue')
# Créer un objet Ticker pour GameStop (GME)
gme_ticker = yf.Ticker("GME")
# Obtenir les données historiques de GameStop pour la période maximale disponible
gme_data = gme_ticker.history(period="max")
# Réinitialiser l'index du DataFrame gme_data sur place
gme_data.reset_index(inplace=True)
# Afficher les cinq premières lignes du DataFrame gme_data
print(gme_data.head())
# URL de la page web pour les revenus de GameStop
url_gme_revenue = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
# Envoyer une requête GET à l'URL
response_gme_revenue = requests.get(url_gme_revenue)
# Vérifier si la requête a réussi (code d'état 200)
if response_gme_revenue.status_code == 200:
    # Récupérer le contenu HTML de la réponse
    html_data_gme_revenue = response_gme_revenue.text
    print("Page web téléchargée avec succès.")
else:
    print(f"Échec du téléchargement de la page. Code d'état : {response_gme_revenue.status_code}")
# Créer un objet BeautifulSoup pour les revenus de GameStop
soup_gme_revenue = BeautifulSoup(html_data_gme_revenue, 'html.parser')
# Trouver le tablea avec les données souhaitées (supposons que c'est le premier tableau)
table_gme_revenue = soup_gme_revenue.find('table')
# Utiliser la fonction read_html pour analyser le tableau HTML et le transformer en DataFrame
gme_revenue = pd.read_html(str(table_gme_revenue))[0]
# Renommer les colonnes en 'Date' et 'Revenue'
gme_revenue.columns = ['Date', 'Revenue']
# Retirer les virgules et les signes de dollar de la colonne 'Revenue'
gme_revenue['Revenue'] = gme_revenue['Revenue'].replace('[\$,]', '', regex=True).astype(float)
# Afficher le DataFrame résultant
print(gme_revenue)
# Filtrer les données de GameStop jusqu'à juin 2021
gme_data_specific = gme_data[gme_data['Date'] <= '2021-06-30']
# Utiliser la fonction make_graph avec les données de GameStop
plot_stock_and_revenue(gme_data_specific, gme_revenue, 'GameStop')
# Utiliser la fonction plot_revenue avec les données de GameStop
plot_revenue(gme_revenue['Date'], gme_revenue['Revenue'], 'GameStop')



