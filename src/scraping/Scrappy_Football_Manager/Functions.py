import os
import time 
import os
def del_duplicates():
    players = []
    arch=open("players.txt","r")
    links_players = arch.readlines()
    for link in links_players:
        if link.strip("\n") not in players:
            players.append(link.strip("\n"))
    arch.close()
    arch=open("players.txt","w")
    for player in players:
        arch.write(player+"\n")
    arch.close

def Setter():
    arch=open("football_manager_2024.3.csv","w")
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
    for key in player.keys():
        arch.write(key+",")
    arch.write("\n")
    arch.close()

def rerun_scrapy():
    caidas=0
    while True:
        print("Caidas: ",caidas)
        os.system("python3 scrapy.py")
        caidas+=1
        time.sleep(10)
        if count_lines("football_manager_2024.3.csv") == count_lines("players.txt"):
            break


def count_lines(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return len(lines)

def xd():
    arch = open("football_manager_2024.3.csv",encoding="utf8")
    arch1 = arch.readlines()
    lista=[]
    for i in arch1:
        lista.append(i.split(";"))
    arch.close()

    arch = open("football_manager_2024_3.csv","a",encoding="utf8")
    for i in lista:
        i.pop(-1)
        arch.write(";".join(i)+"\n")
    arch.close()

#xd()
rerun_scrapy()
