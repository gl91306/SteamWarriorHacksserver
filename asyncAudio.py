import symbl

async def processFile(filepath, websocket):
  local_path = filepath
  conversation_object = symbl.Audio.process_file(
    #credentials={app_id: "554a4148557861676b793546515563316c777666714b4a6a7349466a46746566", app_secret: "53776d69466262387252455a56456d5f6976454a4f64765547626672627758666e535a2d324a624b61306b384a66396d5347676e5f4b702d4957503474647339"}, #Optional, Don't add this parameter if you have symbl.conf file in your home directory
      file_path=local_path
  )
  messageDict = conversation_object.get_messages().__dict__
  print(messageDict)
  transcript = ""
  topicDict = conversation_object.get_topics().__dict__
  for i in messageDict['_messages']:
    a = i.__dict__
    print(a.get('_text'))
    transcript = transcript + '\n' + a.get('_text')
  print(transcript)
  await websocket.send('robo:Transcript: ' + transcript)
  print("------------------")
  for i in topicDict['_topics']:
    a = i.__dict__
    print(a.get('_text'))
