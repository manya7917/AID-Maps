from flask import Flask,render_template,request,session
from graphh import GraphHopper
import folium
import requests
import os
from otp import *
from twilio.rest import Client
import pandas as pd

app=Flask(__name__)

app.secret_key = "manya7917"


# login page
@app.route('/')
def inputs():
    return render_template('new.html')


@app.route('/input_data',methods=['POST'])
def process_input():
    u=request.form['user']
    p=request.form['pass']
    
    print(u)
    print(p)
    return render_template("index.html")

# input page
@app.route('/details')
def detail():
    return render_template('index.html')

@app.route('/detail1',methods=['POST'])
def deatils():
    fn=request.form['fname']
    ln=request.form['lname']
    em=request.form['email']
    ph=request.form['phone']
    ages=request.form['age']
    bld=request.form['blood']
    host=request.form['hosting']
    add=request.form['address']
    cit=request.form['city']
    z=request.form['zip']
    algre=request.form['alg']
    com=request.form['comment']
    m=request.form['med']
    print(fn,ln,em,ph,ages,bld,host,add,cit,z,algre,com,m)
    
    return render_template("email.html")


#maps
@app.route('/map')
def map():
    return render_template('maps.html')


@app.route('/map_data',methods=['POST'])
def maps(): 

    star=request.form['start']
    ed=request.form['end']

    endpoint = "https://graphhopper.com/api/1/route"
    map_key = GraphHopper("API key")
    origin = map_key.address_to_latlong(star)
    dest = map_key.address_to_latlong(ed)
    dist = map_key.distance([origin, dest], unit ='km')
    router = map_key.route([origin, dest])
    
    lat1 = router['paths'][0]['bbox'][1]
    long1 = router['paths'][0]['bbox'][0]
    lat2 = router['paths'][0]['bbox'][3]
    long2 = router['paths'][0]['bbox'][2]
    #print(lat1, long1, " : " ,lat2, long2)
    
    m = folium.Map(location =[lat1, long1], zoom_start = 12)
    
    st = str(lat1)+", "+ str(long1)
    en = str(lat2)+", "+ str(long2)
    print("Start : ", st)
    print("End : ", en)
    
    params = {
    "key": "API key",
    "point": [st, en],
    "points_encoded": "false",
    "vehicle": "car",
    "locale": "en-US",
    "instructions": "false",
    "calc_points": "true"
    }

    # Send request to GraphHopper API
    response = requests.get(endpoint, params=params)

    #Get coordinates from Source to Destination
    data = response.json()    
    path = data['paths'][0]['points']['coordinates']
    pth=[]
    for i in range(len(path)):
        lon = path[i][0]
        laty = path[i][1]
        pth.append([laty, lon])

    #Making the map and saving it
    folium.Marker(location=[lat1, long1], popup='Start', icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(location=[lat2, long2], popup='End', icon=folium.features.CustomIcon(icon_image="static\images\car.png", icon_size=(50, 50))).add_to(m)

    folium.PolyLine(locations=pth, line_opacity = 0.5, color='red').add_to(m)
    # m.save('car2.html')
    directory_path = "C:/Users/XXXXXXX/Desktop/AID MAPS FINAL/templates"
    file_path = os.path.join(directory_path, "car2.html")
    m.save(file_path)


    #Printing ETA and Distance
    route_data = response.json()['paths'][0]
    
    distance = round(route_data['distance'] / 1000, 2)
    # print('Distance:', distance, 'km')
    time = round(route_data['time'] / 60000, 2)
    if(time > 60):
        print('Time:', time/60, 'Hours')
    else:
        print('Time:', time, 'Minutes')    
    return render_template("maps.html",distance=distance,time=time,st=st,en=en)




@app.route('/emer')
def emer():
    return render_template('car2.html')

#email
@app.route('/mail')  
def index():  
    return render_template("email.html")  

@app.route('/verify',methods = ["POST"])  
def verify():  
    rec_email = request.form["email"]
    current_otp = sendEmailVerificationRequest(receiver=rec_email) # this function sends otp to the receiver and also returns the same otp for our session storage
    session['current_otp'] = current_otp
    return render_template('verify.html')  

@app.route('/validate',methods=["POST"])   
def validate():  
    # Actual OTP which was sent to the receiver
    current_user_otp = session['current_otp']
    print("Current User OTP",current_user_otp)
    
    # OTP Entered by the User
    user_otp = request.form['otp'] 
    print("User OTP : ", user_otp)
     
    if int(current_user_otp) == int(user_otp):
        return render_template("sos.html")  
    else:
        return render_template("email.html",msg="Oops! Email Verification Failure, OTP does not match.")   



#sos
@app.route('/sos')
def sos():
    return render_template('sos.html')

@app.route('/soscall',methods=["POST"])
def soscall():
    
    from twilio.rest import Client

   
    account_sid = 'ID'
    auth_token = 'TOKEN'

    
    client = Client(account_sid, auth_token)

 
    to_phone_number = '+91XXXXXXXX'  

    from_phone_number = '+XXXXXXXXX' 

    # Make the call
    call = client.calls.create(
        to=to_phone_number,
        from_=from_phone_number,
        url='http://demo.twilio.com/docs/voice.xml'  
    )

    print('Call SID:', call.sid)  
    return render_template("sos.html",sos_msg="Your call has been forwarded.")

@app.route('/msg')
def msg():
    return ("msg")

@app.route('/msgsend',methods=["POST"])
def msgsend():
    # Your Twilio account SID and auth token
    account_sid = 'YOUR_ACCOUNT_SID'
    auth_token = 'YOUR_AUTH_TOKEN'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # The number you want to send the message to
    to_number = '+91XXXXXXX'

    # The number your Twilio account is associated with
    from_number = '+91XXXXXXXXX'

    # The message you want to send
    message = 'Hello from Twilio!'

    # Send the message using the Twilio API
    message = client.messages.create(
        to=to_number, 
        from_=from_number,
        body=message)

    # Print the message ID
    print(f"Message ID: {message.sid}")
    return

if __name__=="__main__":
    app.run(debug=True)
