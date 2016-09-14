from bs4 import BeautifulSoup
import urllib2
import requests

f = open('C:\Users\E134292\Desktop\DFS\outFile.txt', 'w')
errorFile = open('C:\Users\E134292\Desktop\DFS\errors.txt', 'w')



x = 0
while (x < 500):
	r  = requests.get('http://games.espn.com/ffl/tools/projections?startIndex=' +str(x))
	data = r.text
	#soup = BeautifulSoup(urllib2.urlopen('http://games.espn.com/ffl/tools/projections?startIndex=' +str(x).read(), 'html')
	soup = BeautifulSoup(data, "html.parser")
	tableStats = soup.find('table', attrs={'class' : 'playerTableTable tableBody'})
	for row in tableStats.findAll('tr')[2:]:
		col = row.findAll('td')
		
		try:
			name = col[0].a.string.strip() #a = link // stripping link text
			f.write(name + '\n')
			
		except Exception as e:
			errorFile.write (str(x) + ">>>>>>>>>>>>" + str(a) + "<<<<<<<<<<<<<<" + str(col) + '\n')
			pass
			
	x = x + 40
	
f.close
errorFile.close