import json

from django.shortcuts import render
from web3 import Web3, HTTPProvider
import Database

# Create your views here.
def index(request):
    return render(request,'index.html')
def AdminAction(request):
    uname=request.POST['username']
    passw=request.POST['password']
    if uname == 'Admin' and passw == 'Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Admin Login Failed..!!'}
        return render(request,'index.html',context)

def home(request):
    return render(request,'AdminApp/AdminHome.html')
def AddStations(request):
    return render(request,'AdminApp/AddStations.html')


global details,tx_receipt
def saveDetails(data, type):
    global details,contract,tx_receipt

    blockchain_address='http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount= web3.eth.accounts[0]
    compile_contract_path='EV_SmartContract.json'
    deployed_contract_address='0x0B34131C0A8454898858fD7E075bCb0194640348'
    with open(compile_contract_path) as file:
        contract_json=json.load(file)
        contract_api=contract_json['abi']
    file.close()
    contract= web3.eth.contract(address=deployed_contract_address,abi=contract_api)
    if type == 'AddStation':
        details+=data
        msg=contract.functions.setEVData(details).transact()
        tx_receipt=web3.eth.waitForTransactionReceipt(msg)

global rdetails
def readDetails(contract_type):
    global rdetails
    rdetails = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'EV_SmartContract.json' #Blockchain SmartContract calling code
    deployed_contract_address = '0x0B34131C0A8454898858fD7E075bCb0194640348' #hash address to access Shared Data contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'AddStation':
        rdetails= contract.functions.getEVData().call()




def AddStationAction(request):
    global details
    sname=request.POST['sname']
    location=request.POST['location']
    no_of_c_ports=request.POST['no_of_c_ports']
    capacity=request.POST['capacity']
    charger_speed=request.POST['charger_speed']
    price=request.POST['price']




    readDetails('AddStation')
    status='none'
    for dd in rdetails:
        array=dd[1].split("#")

        if array[0]==sname and array[1]==location:
            status="This Location Station is Already Added"
            break
    if status=='none':
        details = ""
        data = sname+"#"+location+"#"+no_of_c_ports+"#"+capacity+"#"+charger_speed+"#"+price
        saveDetails(data,"AddStation")
        context = {'msg':'Station Registration Successful...!!'}
        return render(request,'AdminApp/AddStations.html',context)
    else:
        context={'msg':status}
        return render(request,'AdminApp/AddStations.html',context)

def ViewStations(request):
    strdata="<table class='table'><thead  class='thead-dark'>" \
            "<tr>" \
            "<th scope='col'>Station Name</th>" \
            "<th scope='col'>Station Location</th>" \
            "<th scope='col'>No.of Port Available</th>" \
            "<th scope='col'>Each Port Capacity</th>" \
            "<th scope='col'>Charger Speed</th>" \
            "<th scope='col'>Price/Hour</th>" \
            "</tr></thead>"



    readDetails('AddStation')
    print(rdetails)

    for dd in rdetails:
        array = dd[1].split("#")
        strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td><td>"+str(array[3])+" kW</td>" \
                  "<td>"+str(array[4])+" Kw/h</td><td>"+str(array[5])+" Rs</td></tr></tbody>"
    strdata += "</table>"
    context={"data":strdata}
    return render(request,'AdminApp/ViewAllStations.html',context)

def ViewUsedUsers(request):
    strdata="<table class='table'><thead  class='thead-dark'>" \
            "<tr>" \
            "<th scope='col'>UserEmail</th>" \
            "<th scope='col'>Station Name</th>" \
            "<th scope='col'>Station Location</th>" \
            "<th scope='col'>Booking Date</th>" \
            "<th scope='col'>Release Date</th>" \
            "<th scope='col'>Total Minutes</th>" \
            "<th scope='col'>Total Paid Amount</th>" \
            "<th scope='col'>Status</th>" \
            "</tr></thead>"



    conn = Database.connect()
    cur=conn.cursor()
    cur.execute("select * from  booking")
    d=cur.fetchall()

    for dd in d:

        strdata += "<tbody><tr><td>"+dd[1]+"</td><td>"+str(dd[2])+"</td><td>"+str(dd[3])+"</td><td>"+str(dd[5])+"</td>" \
                   "<td>"+str(dd[6])+"</td><td>"+str(dd[7])+"</td><td>"+str(dd[8])+"</td><td>"+str(dd[9])+"</td></tr></tbody>"
    strdata += "</table>"
    context={"data":strdata}
    return render(request,'AdminApp/ChargingStatus.html',context)

def ViewEnergyDemand(request):
    conn = Database.connect()
    cur=conn.cursor()
    cur.execute("select distinct location from  booking")
    d=cur.fetchall()
    data_points=[]
    for a in d:

        name=a[0]


        cur.execute("select sum(t_kw) from booking where location='"+name+"'")
        d1=cur.fetchall()
        for b in d1:
            amount=b[0]

            data_points.append({ "label":name,  "y": amount})
    print(data_points)
    return render(request, 'AdminApp/EnergyDemand.html', { "data_points" : data_points })

def TimeWiseDemand(request):
    conn = Database.connect()
    cur=conn.cursor()
    cur.execute("select distinct location from  booking")
    d=cur.fetchall()
    data_points=[]
    for a in d:

        name=a[0]


        cur.execute("select sum(total_hours) from booking where location='"+name+"'")
        d1=cur.fetchall()
        for b in d1:
            amount=b[0]

            data_points.append({ "label":name,  "y": amount})
    print(data_points)
    return render(request, 'AdminApp/TimeWiseDemand.html', { "data_points" : data_points })

def AmountWiseDemand(request):
    conn = Database.connect()
    cur=conn.cursor()
    cur.execute("select distinct location from  booking")
    d=cur.fetchall()
    data_points=[]
    for a in d:

        name=a[0]


        cur.execute("select sum(paid_amount) from booking where location='"+name+"'")
        d1=cur.fetchall()
        for b in d1:
            amount=b[0]

            data_points.append({ "label":name,  "y": amount})
    print(data_points)
    return render(request, 'AdminApp/AmountWiseDemand.html', { "data_points" : data_points })
