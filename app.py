from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

tbody = soup.find('tbody')
tr = tbody.find_all('tr')

temp = [] #initiating a tuple

#insert the scrapping process here
for i in range(len(tr)):
    row = tbody.find_all('tr')[i]
    
    #get bulan
    period = row.find_all('td')[0].text
    
    #get hari
    day = row.find_all('td')[1].text
    
    #get kurs
    kurs = row.find_all('td')[2].text
    
    temp.append((period,day,kurs))
    
temp = temp[::-1]

#change into dataframe

df = pd.DataFrame(temp)
df.columns = ["Date", "Day","Kurs"]

#insert data wrangling here
df['Kurs'] = df['Kurs'].str.replace(",","")
df['Kurs'] = df['Kurs'].str.replace(" IDR","")
df["Date"] = df["Date"].apply(pd.to_datetime)
df['Kurs'] = df['Kurs'].astype(float)

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["Kurs"].mean().round(2)}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
