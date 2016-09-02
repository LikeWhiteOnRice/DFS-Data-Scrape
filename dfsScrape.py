from bs4 import BeautifulSoupWeb 
import requests
import csv
import getpass
import datetime
import sys

def main():

	(position) = selection_menu()
	url = buildURL(position)

	if position == 1:
		end_filename = 'Quarterbacks'
	elif position == 2:
		end_filename = 'Runningbacks'
	elif position == 3:
		end_filename = 'Receivers'
	elif position == 4:
		end_filename = 'Tightends'
	elif position == 5:
		end_filename = 'Defenses'
		
	filename = 'DFS_data_' + end_filename + '_' + str(datetime.date.today()) + '.csv'
	ofile = open(filename, "wb")
	writer = csv.writer(ofile, delimiter = ',', escapechar = ' ')
	
	r  = requests.get("http://" +url)
	data = r.text
	soup = BeautifulSoup(data)
	
	statsList = soup.findAll('th', {'class':'Ta-end'})
	stats = ['Name', 'Team', 'Pos', 'Fantasy Team']
	for s in statsList:
		t = str(s.findAll(text=True))
		t = t[3:len(t)-2]
		stats.append(t.split(",")[0])
		try:
			stats.remove("Rankings")
		except:
			continue

	writer.writerow(stats)
	pageNum = 0
	
	while True:
		count = 0
		pageCount = str(pageNum * 25)
		print "Loading page",(pageNum+1)
		content = br.open(url + pageCount)
		soup = BeautifulSoup(content)
		players = soup.findAll('div', {'class':'ysf-player-name Nowrap Grid-u Relative Lh-xs Ta-start'})
		dataList = soup.findAll('td', {'class': 'Ta-end'})
		fantasyTeams = soup.findAll('div', {'style':'text-overflow: ellipsis; overflow: hidden;'})

		fanTeams = []
		for f in fantasyTeams:
			tmpf = str(f.findAll(text=True))[3:len(f)-3]
			fanTeams.append(fixText(tmpf))

		# Exit condition
		try:
			str(players[0].findAll(text=True))
		except:
			break

		for player in players:
			playerStats = []
			pNum = count*(len(stats)-4)
			playerData = str(player.findAll(text=True))
			name = getName(playerData)
			(team, pos) = getTeamAndPosition(playerData)
			fanTeam = fanTeams[count+1]
			playerStats.extend([name, team, pos, fanTeam])
			for i in range(0, len(stats)-4):
				tmp = str(dataList[pNum+i].findAll(text=True))
				tmp = tmp[3:len(tmp)-2]
				if tmp.find("/") != -1:
					playerStats.append("'" + tmp + "'")
				else:
					playerStats.append(tmp)
			writer.writerow(playerStats)
			count += 1
		pageNum += 1
		if pageNum >= maxPages: break
	ofile.close()
	
	
	
def selection_menu():
	# Selection Menu

	print "\nPosition:"
	print "-------------"
	print "1. Quarterbacks\n2. Runningbacks\n3. Receivers\n4. Tightends\n5. Defenses"
	print "-------------"
	try:
		position = input("Enter 1 - 5: ")
	except:
		print "Bad Selection. Exiting..."
		sys.exit()
	if (position < 1 or position > 5):
		print "Bad Selection. Exiting..."
		sys.exit()

	print 'Gathering Data...'
	return (position)
	
	
	
def buildURL(position):

	begin_url = 'http://baseball.fantasysports.yahoo.com/b1/' + str(leagueID) + '/players?status='
	end_url = '&myteam=0&sort=OR&sdir=1&count='

	return begin_url + end_url
	
	

def getName(data):
	if data[2] == '"':
		playerDataName = data.split('"')
	else:
		playerDataName = data.split("'")
	return fixText(playerDataName[1])

	
	
def getTeamAndPosition(data):
	playerData = data.split("'")
	if data[2] == '"':
		teampos = playerData[4]
	else:
		teampos = playerData[5]
	team = teampos[0:teampos.find("-")-1]
	pos = teampos[teampos.find("-")+2:len(teampos)]
	return (team, pos)


	
def fixText(str):
	s = str
	s = s.replace('\\xe1', 'a')
	s = s.replace('\\xe0', 'a')
	s = s.replace('\\xc1', 'A')
	s = s.replace('\\xe9', 'e')
	s = s.replace('\\xc9', 'E')
	s = s.replace('\\xed', 'i')
	s = s.replace('\\xcd', 'I')
	s = s.replace('\\xf3', 'o')
	s = s.replace('\\xd3', 'O')
	s = s.replace('\\xfa', 'u')
	s = s.replace('\\xda', 'U')
	s = s.replace('\\xf1', 'n')
	return s

	
	
if __name__ == "__main__":
	main()