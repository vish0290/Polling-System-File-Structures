import matplotlib.pyplot as plt
import eel

eel.init("web")

userid = [] 


@eel.expose
def login(uid,upass):
    get = open("data.txt", "r")
    temp = get.readlines()
    udata = []
    
    for i in range(len(temp)):
        if temp[i].startswith(uid):
            udata = temp[i].split("|")     
    #print(udata)
    if udata[2] != upass:   
        return "false"
    else:
        if udata[0].startswith("vt"):
            return udata,"voter"
        elif udata[0].startswith("ca"):
            return udata,"candidate"
        elif udata[0].startswith("st"):
            return udata,"staff"
    get.close()

def vsort():
    get = open("data.txt", "r")
    get.seek(0)
    temp = get.readlines()
    
    v = []
    c = []
    s = []
    l = ""
    
    for i in range(len(temp)):
        if temp[i].startswith("vt"):
            v.append(temp[i])
        if temp[i].startswith("st"):
            s.append(temp[i])
        if temp[i].startswith("ca"):
            c.append(temp[i])
        if temp[i].startswith("system"):
            l = temp[i]
    
    fout = open("data.txt", "w")
    v.sort()
    c.sort()
    s.sort()
    for j in range(len(c)):
        final = f"{c[j]}"
        fout.write(final)
    for j in range(len(s)):
        final = f"{s[j]}"
        fout.write(final)
    for j in range(len(v)):
        final = f"{v[j]}"
        fout.write(final)
    fout.write(l)
    fout.close()
    
    fin1 = open("data.txt","r")
    fin2 = open("index.txt","w")
    fin1.seek(0)
    
    details = fin1.readlines()
    for i in range(len(details)):
        data = details[i].split("|")
        fin2.write(f"{i}|{data[0]}|\n")
    fin1.close()
    
    fin2.close()
    get.close()


@eel.expose
def display_teams():
    gets = open("data.txt", "r")
    temp = gets.readlines()
    clist = []
    iget = open("index.txt","r")
    index = iget.readlines()
    cid=[]
    fdata = []
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith("ca"):
            cid.append(data[0])
    
    for i in cid:
        i=int(i)
        clist.append(temp[i])
    
    for i in range(len(clist)):
        data = clist[i].split("|")
        fdata.append(f"{data[0]}|{data[1]}|{data[3]}|")
    print(fdata)
    gets.close()
    iget.close()
    return fdata
        
@eel.expose
def display_voter(uid):
    gets = open("data.txt", "r")
    temp = gets.readlines()
    clist = []
    iget = open("index.txt","r")
    index = iget.readlines()
    cid=[]
    fdata = []
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith(uid):
            cid.append(data[0])    
    for i in cid:
        i=int(i)
        clist.append(temp[i])
    for i in range(len(clist)):
        data = clist[i].split("|")
        fdata = data
    gets.close()
    iget.close()
    return fdata
       


def system_status():
    data = []
    get = open("data.txt","r")
    temp = get.readlines()
    for i in range(len(temp)):
        if temp[i].startswith("system"):
            data = temp[i].split("|")
    if data[1]=="true":
        return True
    elif data[1]=="false":
        return False
    get.close()


    
@eel.expose
def cast_vote(cid,uid):
    iget=open("index.txt","r")
    index = iget.readlines()
    get = open("data.txt","r")
    temp = get.readlines()
    cindex = ""
    vindex = ""
    cdata = []
    vdata = []
        
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith(cid):
            cindex = data[0]
        if data[1].startswith(uid):
            vindex = data[0]       
            
            
    vidx =int(vindex)
    cidx =int(cindex)        
    vdata = temp[vidx].split("|")
    cdata = temp[cidx].split("|")
    val = system_status()    
        
    if val:
        if vdata[5] == "false":
            vote = int(cdata[4])
            vote += 1
            cdata[4] = vote
            vdata[5] = "true"
            cupdate = f"{cdata[0]}|{cdata[1]}|{cdata[2]}|{cdata[3]}|{cdata[4]}|\n"
            vupdate = f"{vdata[0]}|{vdata[1]}|{vdata[2]}|{vdata[3]}|{vdata[4]}|{vdata[5]}|\n"
            fout = open("data.txt","w")
            for i in range(len(temp)):
                if temp[i].startswith(vdata[0]):
                    temp[i] = vupdate
                if temp[i].startswith(cdata[0]):
                    temp[i] = cupdate    
            for i in range(len(temp)):
                fout.write(temp[i])
            fout.close()
            iget.close()
            get.close()
            return "voted successfully"
        else:
            iget.close()
            get.close()
            return "it seems you have already voted"
    else:
        return("Vote System is Inactive")    
    
    
@eel.expose    
def profile(vid):
    print(vid)
    iget = open("index.txt","r")
    index = iget.readlines()
    get = open("data.txt","r")
    temp = get.readlines()
    pid = ""
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1] == vid:
            pid = data[0]
    pid = int(pid)
    user_data = temp[pid].split("|")
    print(user_data)
    get.close()
    iget.close()
    return user_data,"true"
@eel.expose
def winner():
    cid = []
    c_teams = []
    c_votes = []
    iget = open("index.txt","r")
    get = open("data.txt","r")
    index = iget.readlines()
    temp = get.readlines()
    
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith("ca"):
            cid.append(data[0])         
    
    for i in cid:
        i=int(i)
        data = temp[i].split("|")
        c_teams.append(data[3])
        c_votes.append(int(data[4]))
    num = max(c_votes)
    id = c_votes.index(num)
    name = c_teams[id]    
    plt.bar(c_teams,c_votes)
    plt.savefig("web\output1", facecolor='w', bbox_inches="tight",pad_inches=0.3, transparent=True)
    plt.title('winner')
    plt.xlabel('teams')
    plt.ylabel('Votes')
    get.close()
    iget.close()
    return name
        
@eel.expose
def system_mod(uid,override_key):
    sid = []
    iget = open("index.txt","r")
    get = open("data.txt","r")
    index = iget.readlines()
    temp = get.readlines()
    details = temp
    flag = False
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith("st"):
            sid.append(data[0])         
    for i in sid:
        i = int(i)
        data = temp[i].split("|")
        if data[0].startswith(uid):
            if data[3].startswith(override_key):
                flag = True
    if flag:
        for i in range(len(details)):
            if details[i].startswith("system"):
                s_data = details[i].split("|")
                if s_data[1] == "true":
                    s_data[1] = "false"
                    s_final = f"{s_data[0]}|{s_data[1]}|"
                    for j in range(len(details)):
                        if details[j].startswith("system"):
                            details[j] = s_final
                    fout = open("data.txt", "r+")
                    for k in range(len(details)):
                        op = f"{details[k]}"
                        fout.write(op)
                    fout.close()
                    vsort()
                    return "System is Inactive"
                    
                elif s_data[1] == "false":
                    s_data[1] = "true"
                    s_final = f"{s_data[0]}|{s_data[1]}|"
                    for j in range(len(details)):
                        if details[j].startswith("system"):
                            details[j] = ""
                            details[j] = s_final
                    fout = open("data.txt", "r+")
                    for k in range(len(details)):
                        op = f"{details[k]}"
                        fout.write(op)
                    fout.close()  
                    vsort()
                    return "system is active"        
    

                    
        
@eel.expose
def reset(uid,override_key):
    sid = []
    key = str(override_key)
    iget = open("index.txt","r")
    get = open("data.txt","r")
    index = iget.readlines()
    temp = get.readlines()
    details = temp
    flag = False
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith("st"):
            sid.append(data[0])         
    for i in sid:
        i = int(i)
        data = temp[i].split("|")
        if data[0].startswith(uid):
            if data[3].startswith(key):
                flag = True
                print("pass")
    if flag:
        for i in range(len(details)):
            if details[i].startswith("vt"):
                data = details[i].split("|")
                data[5] = "false"
                vupdate = f"{data[0]}|{data[1]}|{data[2]}|{data[3]}|{data[4]}|{data[5]}|\n"
                for i in range(len(details)):
                    if details[i].startswith(data[0]):
                        details[i] = vupdate
                fout = open("data.txt", "w")
                for j in range(len(details)):
                    op = f"{details[j]}"
                    fout.write(op)
                fout.close()

            if details[i].startswith("ca"):
                cdata = details[i].split("|")
                cdata[4] = 0
                cupdate = f"{cdata[0]}|{cdata[1]}|{cdata[2]}|{cdata[3]}|{cdata[4]}|\n"
                for i in range(len(details)):
                    if details[i].startswith(cdata[0]):
                        details[i] = cupdate
                fout = open("data.txt", "w")
                for j in range(len(details)):
                    op = f"{details[j]}"
                    fout.write(op)
                fout.close()
        vsort()
        return "System Data is been formated"
    else:
        return "Failed"
    
@eel.expose
def add_voter(name,password,age,ano):
    get = open("data.txt","r")
    details = get.readlines()
    count = 0
    voters = []
    for i in range(len(details)):
        if details[i].startswith("vt"):
            data = details[i].split("|")
            if data[4] == ano:
                return "person already exsist"
            
    for i in range(len(details)):
        if details[i].startswith("vt"):
            voters.append(details[i])
    temp = voters[-1].split("|")
    id = temp[0]
    count = id[2:]
    b =  int(count)
    count = b            
    if count < 9:
        count = count+1
        vid = "000"+str(count)
    elif count<99:
        count+=1
        vid = "00"+str(count)
    elif count<999:
        count+=1
        vid = "0"+str(count)
    else:
        vid = str(count)
        
    id = "vt"+vid
    status = "false"
    final = f"{id}|{name}|{password}|{age}|{ano}|{status}|\n"
    details.append(final)
    fout = open("data.txt", "w")
    for j in range(len(details)):
        op = f"{details[j]}"
        fout.write(op)
    fout.close()
    vsort()
    get.close()
    return "Voter added successfully"

@eel.expose
def remove_voter(uid):
    if uid[0:2] == "vt":
        data = []  
        get = open("data.txt","r")
        details = get.readlines()
        for i in range(len(details)):
            if details[i].startswith(uid):
                clear = ""
                data=details[i].split("|")
                details[i] = clear
                fout = open("data.txt", "r+")
                for j in range(len(details)):
                    op = f"{details[j]}"
                    fout.write(op)
                fout.close()
        vsort()
        get.close()
        return f"{data[1]}"
    else:
        return "false"

@eel.expose  
def modify_voter(uid,name,password,age,ano):
    vid = []
    get = open("data.txt","r")
    iget = open("index.txt","r")
    details=get.readlines()
    index = iget.readlines()
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith(uid):
            vid = data[0]
    vid = int(vid)
    v_data = details[vid].split("|")
    v_data[1] = name
    v_data[2] = password
    v_data[3] = age
    v_data[4] = ano
    vupdate = f"{v_data[0]}|{v_data[1]}|{v_data[2]}|{v_data[3]}|{v_data[4]}|{v_data[5]}|\n"
    for i in range(len(details)):
        if details[i].startswith(v_data[0]):
            details[i]=vupdate
    fout = open("data.txt", "r+")
    for j in range(len(details)):
        op = f"{details[j]}"
        fout.write(op)
    fout.close()
    get.close()
    iget.close()
    vsort()
    return "data Modified"
   
@eel.expose
def add_candidate(name,password,teamname):
    get = open("data.txt","r")
    details = get.readlines()
    count = 0
    candi=[]
    for i in range(len(details)):
        if details[i].startswith("ca"): 
            data = details[i].split("|")
            if data[1] == name or data[3] == teamname:
                return "team already exsist" 
                
    for i in range(len(details)):
        if details[i].startswith("ca"):
            candi.append(details[i])
    temp = candi[-1].split("|")
    id = temp[0]
    count = id[2:]
    b =  int(count)
    count = b  
    if count < 9:
        count = count+1
        vid = "000"+str(count)
    elif count<99:
        count+=1
        vid = "00"+str(count)
    elif count<999:
        count+=1
        vid = "0"+str(count)
    else:
        vid = str(count)
    
    id = "ca"+vid
    votes = 0
    final = f"{id}|{name}|{password}|{teamname}|{votes}|\n"
    details.append(final)
    fout = open("data.txt", "w")
    for j in range(len(details)):
        op = f"{details[j]}"
        fout.write(op)
    fout.close()
    vsort()
    get.close()
    return "Team Added Succesfully"

@eel.expose
def remove_candidate(uid):
    get = open("data.txt","r")
    details = get.readlines()
    for i in range(len(details)):
        if details[i].startswith(uid):
            clear = ""
            data = details[i].split("|")
            details[i] = clear
            fout = open("data.txt", "r+")
            for j in range(len(details)):
                op = f"{details[j]}"
                fout.write(op)
            fout.close()
    vsort()
    get.close()
    return data[3]
@eel.expose
def display_candidate(vid):
    gets = open("data.txt", "r")
    temp = gets.readlines()
    clist = []
    iget = open("index.txt","r")
    index = iget.readlines()
    cid=[]
    fdata = []
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith(vid):
            cid.append(data[0])
    
    for i in cid:
        i=int(i)
        clist.append(temp[i])
    for i in range(len(clist)):
        data = clist[i].split("|")
        fdata = data
    #print(fdata)
    gets.close()
    iget.close()
    return fdata

@eel.expose
def modify_candidate(uid,name,password,teamname):
    vid = []
    get = open("data.txt","r")
    iget = open("index.txt","r")
    details=get.readlines()
    index = iget.readlines()
    for i in range(len(index)):
        data = index[i].split("|")
        if data[1].startswith(uid):
            vid = data[0]
    vid = int(vid)
    v_data = details[vid].split("|")
    v_data[1] = name
    v_data[2] = password
    v_data[3] = teamname
    vupdate = f"{v_data[0]}|{v_data[1]}|{v_data[2]}|{v_data[3]}|{v_data[4]}|\n"
    for i in range(len(details)):
        if details[i].startswith(v_data[0]):
            details[i]=vupdate
    fout = open("data.txt", "r+")
    for j in range(len(details)):
        op = f"{details[j]}"
        fout.write(op)
    fout.close()
    get.close()
    iget.close()
    vsort()
    return "Modified Successfully"

@eel.expose
def allvoter():
    get = open("data.txt","r")
    get.seek(0)
    temp = get.readlines()
    voters = []
    for i in range(len(temp)):
        if temp[i].startswith("vt"):
            voters.append(temp[i])
    get.close()
    count = len(voters)
    return voters,count


@eel.expose
def allcandidate():
    get = open("data.txt","r")
    get.seek(0)
    temp = get.readlines()
    candidate = []
    for i in range(len(temp)):
        if temp[i].startswith("ca"):
            candidate.append(temp[i])
    get.close()
    count = len(candidate)
    return candidate,count


eel.start("index.html")
#if __name__ == '__main__':
    #allvoter()
    #vsort()
    #login("vt1001","1001")
    #cast_vote("ca1001","vt1008")
    #profile("vt1001")
    #profile("ca0002")
    #profile("st1002")
    #display_teams()
    # val = display_voter("vt0002")
    # print(val)
    #system_status()
    #val=winner()
    #print(val)
    #system_mod("st1001","5656")
    #val=reset("st0001","5656")
    #print(val)
    #add_voter("pheonix","20","2101","1010")
    #remove_voter("vt0004")
    #modify_voter("vt1009","breach","25","1009","3102")
    #add_candidate("thanos","1004","genysis")
    #remove_candidate("ca0003")
    #modify_candidate("ca1003","brimstone","1003","valo")
