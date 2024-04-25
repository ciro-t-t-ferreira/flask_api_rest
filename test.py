import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":10  , "name": "Flask is fun"          , "views": 137137},
        {"likes":1013, "name": "Flask is sometimes fun", "views": 1377  },
        {"likes":102 , "name": "Is Django also fun?"   , "views": 987198},
        {"likes":324 , "name": "Hmm, not sure"         , "views": 5321  }]

'''
for i in range(len(data)):
    response = requests.put(BASE + 'video/' + str(i), data[i])
    print(response.json())

response = requests.patch(BASE + 'video/2', {"views": 111})
print(response.json())
response = requests.get(BASE + 'video/2')
print(response.json())
'''

response = requests.delete(BASE + 'video/3')
print("Press enter to see all videos")
input()

#print all videos (only until it finds a empty id)
istherevideo = True
i = 0
while istherevideo:
    response = requests.get(BASE + 'video/' + str(i))
    if not response:
        istherevideo = False
    print(response.json())
    i += 1

