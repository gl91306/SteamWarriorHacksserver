import json # 
import asyncio # oh hi guys im working on the speech bubbles in the site repl
import websockets
import symbl
import datetime
import asyncAudio
import time
dinnertime= ""
lunchtime = ""
breakfast = ""

async def startthing(type, data, websocket, user): # This bacicly does whatever with the data
# WILSON hi ur code goes here
    if type == 'settings':
      if 'setdomcom:' in data:
        print('settingdomcomcodee')
        domcom = data.split('setdomcom:')[1]
        print(domcom)
        with open('data.json', 'r') as openfile: # opens auth file containing username, token, and password
          json_object = json.load(openfile)
        with open('data.json', 'w') as outfile: # opens auth file containing username, token, and password
          json_object['users_pass'][user]['domcom'] = domcom
          json.dump(json_object, outfile)

    if type == 'tracker':
      if 'insulin:' in data:
        finaldata = data.split('insulin:')[1]
        print(finaldata)
        if 'set dinner to' in finaldata:
          mytime = finaldata.split('set dinner to')[1]
          if 'p.m.' in mytime:
            dinnertime = mytime.split('pm')[0]
            await websocket.send('dinner:' + dinnertime)
          elif 'a.m.' in mytime:
            dinnertime = mytime.split('am')[0]
            await websocket.send('dinner:' + dinnertime)
          else:
            print('invalid time spoken')
            await websocket.send('robo:Invalid dinner data!')

        elif 'set lunch to' in finaldata:
          mytime = finaldata.split('set lunch to')[1]
          if 'p.m.' in mytime:
            lunchtime = mytime.split('pm')[0]
            await websocket.send('lunch:' + lunchtime)
          elif 'a.m.' in mytime:
            lunchtime = mytime.split('am')[0]
            await websocket.send('lunch:' + lunchtime)
          else:
            print('invalid time spoken')
            await websocket.send('robo:Invalid lunch data!')

        elif 'set breakfast to' in finaldata:
          mytime = finaldata.split('set breakfast to')[1]
          if 'p.m.' in mytime:
            breakfast = mytime.split('pm')[0]
            await websocket.send('breakfast:' + breakfast)
          elif 'a.m.' in mytime:
            breakfast = mytime.split('am')[0]
            await websocket.send('breakfast:' + breakfast)
          else:
            print('invalid time spoken')
            await websocket.send('robo:Invalid breakfast data!') # so bacicly what happens is that when the person says "set breakfast to, it will send a server request and will send back the time"

    if type == 'emergency': # This would be idle mode for instance
        if 'sad' in data: # The data would be like 'happy' or 'sad' or somthing
            await websocket.send('HAPPE MUSIC') # Sends a signal back for that action
    if type == 'domvio':
      print('EMERGENCY!!!!')
      await websocket.send('robo:Calling 911')
      await websocket.send('robo:Hello 911, what is ur emergency?')
      await websocket.send('robo:Ill report the authorities')
      await websocket.send('robo:They are coming right now')
      await websocket.send('robo:A transcipt of your recording will be sent to ur emergency contacts')
      await websocket.send('robo:Recording start')
      await websocket.send('record:start')
      print(data)
      blob = await websocket.recv()
      newFile = open("recording.mp3", "wb")
      newFileByteArray = bytes(blob)
      newFile.write(newFileByteArray)
      time.sleep(3)
      print('done writing data')
      await asyncAudio.processFile('recording.mp3', websocket)
    print('socket cycle done!!!')

async def echo(websocket):
    input = await websocket.recv() # triggers when somthing is sent
    print("< {}".format(input)) # logs input, dev only
    loggedon = False # variable to check auth key status
    with open('data.json', 'r') as openfile: # opens auth file containing username, token, and password
        json_object = json.load(openfile)
    user = ''
    for i in json_object['users_pass']: # loops though the accounts looking for auth match
        if 'token' in json_object['users_pass'][i]:
            if json_object['users_pass'][i]['token'] == input.split(',')[0]:
              user = i
              loggedon = True # If matched, it sets it to true
    if loggedon == False:
        print('wrong')
        await websocket.send('WRONG TOKEN YOU HAVE') # If else, it sends an 'INCORRECT' response
    elif loggedon == True:
        print('right')
        await websocket.send('CORRECT!') # auth token matches
        await startthing(input.split(',')[1], input.split(',')[2], websocket, user) # starts the function to handle ai response and stuff

async def main():
    async with websockets.serve(echo, "0.0.0.0", 6969):
        await asyncio.Future()  # run forever

asyncio.run(main()) # async stuff :P