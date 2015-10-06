import urllib
import boto3
import json
import codecs

s3 = boto3.resource('s3')

def upload_to_s3(filename):
    s3.Object('images.munchcal.com', filename).put(Body=open(filename), ContentType='image/jpeg') 

def download_image(url, filename):
    testfile = urllib.URLopener()
    testfile.retrieve(url, filename)

# load preprocessed json
count = 0
start_at = 0 
with codecs.open('preprocessed.json', encoding='utf-8') as f:
    for line in f:
        if start_at > count:
            count = count + 1
        else:
            j = json.loads(line)
            filename = 'recipes/%s.jpg' % j['id']
            try:
                download_image(j['image'], filename)
                upload_to_s3(filename)
                count = count + 1
                print 'uploaded %s, latest: %s' % (count, j['id'])
            except IOError as e:
                print e
                print 'skipping %s' % j['id']

