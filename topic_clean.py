import re
def remove_tags(text):
    #clean unnescessary tag
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

number = []
docid = []
url = []

data = open('/content/anserini/src/main/resources/topics-and-qrels/topics.backgroundlinking19.txt', 'r')
for line in data:
    #print("\\")
    y = remove_tags(line)
    if (y.strip()):
      topic = y.strip()
      #print(topic)
      if("Number" in topic):
        #print(topic)
        a = topic.split(": ")
        #print(a[1])
        number.append(a[1])
      elif("https" in topic):
        #print(topic)
        url.append(topic)
      else:
        docid.append(topic)
    #print(y)