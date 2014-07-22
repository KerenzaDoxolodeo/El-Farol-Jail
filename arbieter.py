import sys
import subprocess

happyness=[]
fight=[]
status=[]
listOfWork=[]
e=len(sys.argv)
name= sys.argv[e-1].split(",")
for x in xrange (len(name)):
    happyness.append(0)
    fight.append([0,False,0,0,0]) #Fight, Consecutive Fight, Violation, Consecutive not going to gym, Error
    status.append(0)

while len(name)-status.count("E") > 2: #While at least 3 player survived
    decision=[]
    for y in xrange(len(name)):
        if status[y]=="E": # Checking if player is eliminated
            decision.append("E")
        elif status[y]>0: # Checking if playes is in quarantine
            decision.append("Q")
            status[y]-=1
        else:
            command=str(y+1)+" "+",".join(listOfWork)
            process=subprocess.Popen([sys.executable,name[y]],stdout=subprocess.PIPE)
            res=process.communicate(command)
            z=res[0].strip("\n").strip("\r")
            if z not in ["G","L"]: #Checking illegal order
                decision.append("Q")
                (fight[y])[4]+=1
                print z
            else:
                decision.append(z)
    leftPlayer=len(name)-decision.count("E")
    treshHold=leftPlayer * 60.0 / 100 #60% of people of prisoner
    gymVisitor=decision.count("G")
    doesChaosOccur= treshHold < gymVisitor
    for y in xrange(len(name)):
        if decision[y]=="L":
            happyness[y]+=leftPlayer
            (fight[y])[3]+=1
            (fight[y])[1]= False
        elif decision[y]=="G":
            (fight[y])[3]=0
            if doesChaosOccur == False:
                happyness[y]+=3*leftPlayer-(2*gymVisitor)
                (fight[y])[1]=False
            else:
                (fight[y])[0]+=1
                if (fight[y])[1]==True or (fight[y])[0]==30: #Checking for red card
                    status[y]=3
                    (fight[y])[2]+=1
                (fight[y])[1]= True
        else:
            (fight[y])[1]=False
            (fight[y])[3]+=1
        if (fight[y])[3]==30 or (fight[y])[2]==4:
            status[y]="E"
            happyness[y]=="E"
    with open("file.txt","a") as f:
        f.write(" ".join(str(o) for o in decision)+"\n")
        f.write(" ".join(str(o) for o in happyness)+"\n")
    listOfWork.append("".join(decision))
    decision=[]
    print command
