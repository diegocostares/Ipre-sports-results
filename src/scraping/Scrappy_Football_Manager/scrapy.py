from playwright.sync_api import sync_playwright

# ###Get all the clubs of a league
# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=False)
#     page = browser.new_page()
#     page.goto('https://fminside.net/clubs',timeout=200000)

#     league = page.query_selector('[placeholder="League"]')
#     league.type("LaLiga")
#     league.press("Enter")

#     filter = page.wait_for_selector(f'//div[@class="active-filter" and text()="League: LaLiga"]',timeout=10000)

#     arch=open("clubs.txt","w")
#     clubs = page.query_selector_all('//ul[@class="club"]')
#     for club in clubs:
#         arch.write("https://fminside.net/"+club.query_selector("a").get_attribute("href")+"\n")
#     browser.close()
#     arch.close()
#     print("Termino de obtener todos los clubes")
#     print("------------")

#links_clubs=["https://fminside.net/clubs/5-fm-243/1736-real-madrid"]

###Get all the players of the clubs
# arch=open("clubs.txt","r")
# links_clubs = arch.readlines()
# arch.close()

# arch=open("players.txt","a")
# for link in links_clubs:
#     with sync_playwright() as p:
#         browser = p.firefox.launch(headless=False)
#         page = browser.new_page()
#         page.goto(link.strip("\n"),timeout=200000)
        
#         players = page.query_selector_all('//ul[@class="player show"]')
#         for player in players:
#             try:
#                 link_player = "https://fminside.net/"+player.query_selector("a").get_attribute("href")
#             except:
#                 print("player not found")
#                 continue
#             arch.write(link_player+"\n")

#         print("Jugadores obtenidos del club: ",link)
#         browser.close()
# arch.close()
# print("Termino de obtener todos los jugadores")


# ###Get the attributes of the players
arch=open("players.txt","r")
links_players = arch.readlines()
arch.close()

arch=open("football_manager_2024_3.csv","r")
actual = len(arch.readlines())-1
links_players=links_players[actual:]
print("Llevamos",actual, " Jugadores. Quedan: ",len(links_players))

arch.close()

#links_players=["https://fminside.net/players/5-fm-243/67293621-juanmi-latasa"]
last_team=""
for link in links_players:
    print("Obteniendo datos del jugador: ",link)
    player={ "Name":"-" ,"Age":"-","Position":"-","Foot":"-","Length":"-","Weight":"-",
            "Caps / Goals":"-","Ability":"-","Potential":"-","Team":"-","Nationality":"-","On loan at":"-",
            "On loan from":"-","Loan ends":"-","Sell value":"-","Wages":"-","Contract end":"-","Rel. clause":"-",
            "Role1":"-","Value1":"-","Role2":"-","Value2":"-","Role3":"-","Value3":"-","Role4":"-","Value4":"-",
            "Role5":"-","Value5":"-","Corners":"-","Crossing":"-","Dribbling":"-","Finishing":"-",
            "First Touch":"-","Free Kick Taking":"-","Heading":"-","Long Shots":"-","Long Throws":"-",
            "Marking":"-","Passing":"-","Penalty Taking":"-","Tackling":"-","Technique":"-","Aggression":"-",
            "Anticipation":"-","Bravery":"-","Composure":"-","Concentration":"-","Decisions":"-","Determination":"-",
            "Flair":"-","Leadership":"-","Off the Ball":"-","Positioning":"-","Teamwork":"-","Vision":"-",
            "Work Rate":"-","Acceleration":"-","Agility":"-","Balance":"-","Jumping Reach":"-","Natural Fitness":"-",
            "Pace":"-","Stamina":"-","Strength":"-","Aerial Reach":"-","Command of Area":"-","Communication":"-",
            "Eccentricity":"-","First Touch":"-","Handling":"-","Kicking":"-","One on Ones":"-","Passing":"-",
            "Punching (Tendency)":"-","Reflexes":"-","Rushing Out (Tendency)":"-","Throwing":"-"}

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(link,timeout=90000)
        #Get the attributes of the players

        info = page.query_selector('//div[@class="meta"]')
        ability = info.query_selector('//span[@id="ability"]')
        potential = info.query_selector('//span[@id="potential"]')
        player["Ability"]=ability.inner_text()
        player["Potential"]=potential.inner_text()
        values = info.query_selector_all('//span[@class="value"]')
        keys=["Team","Nationality","Position"]
        for val in values:
            if len(values)==5:
                values.pop(1)
                values.pop(1)
            try:
                if "," in val.inner_text():
                    player[keys.pop(0)]=val.inner_text().replace(",",".")
                else:
                    player[keys.pop(0)]=val.inner_text()
            except:
                print("Error #1")



        attributes = page.query_selector_all('//div[@class="column"]')
        attributes.pop(-1)
        attributes.pop(-1)
        
        for attribute in attributes:
            #attribute is a div with a ul inside that have N li with the attribute key and value
           
            #Get the value
            try: #for player info, contract, best roles
                section = attribute.query_selector("//h2")

                values = attribute.query_selector_all("//li")

                if "ROLES" in section.inner_text():

                    keys=["Role1","Value1","Role2","Value2","Role3","Value3","Role4","Value4","Role5","Value5"]
                    for val in values:
                        val = val.query_selector_all("//span")
                        try:
                            player[keys.pop(0)]= val[0].inner_text()
                            player[keys.pop(0)]= val[1].inner_text()

                        except:
                            
                            break
                else:
                    for val in values:
                        val = val.query_selector_all("//span")
                        try:
                            if val[1].inner_text()=="":
                                val[1]=val[3]
                            player[val[0].inner_text()]= val[1].inner_text().replace(",",".")
                        except:
                            
                            break


            except: #mental, physical, technical, goalkeeping


                values = attribute.query_selector_all("//tr")


                for val in values:

                    val = val.query_selector_all("//td")
                    try:
                        player[val[0].inner_text()]= val[1].inner_text().replace(",",".")
                    except:
                        print("Problema leyendo los atributos")
                        break

        browser.close()


    arch=open("football_manager_2024_3.csv","a")
    for key in player.keys():
        arch.write(player[key]+";")
    arch.write("\n")
    arch.close()

print("Termino de obtener todos los datos de los jugadores")
