# Requires pymongo
import pymongo
from sets import Set

from pymongo import MongoClient


########## MongoHQ databases ##############
# Need to modify this so that the user and password are stored separately
ideagenstest = {'url': "kahana.mongohq.com",
                'port': 10056,
                'dbName': 'IdeaGensTest',
                'user': 'sandbox',
                'pswd': 'protolab1' }
# user and paswd are incorrect (do not want to commit secure info
ideagens = {'url': "kahana.mongohq.com",
            'port': 10075,
            'dbName': 'IdeaGens',
            'user': 'experimenter',
            'pswd': 'protolab1' }

def get_uniq_part ():
  db = get_mongodb(ideagenstest['url'],
                   ideagenstest['port'],
                   ideagenstest['dbName'],
                   ideagenstest['user'],
                   ideagenstest['pswd'])
  parts = db.participants.find()
  users = Set([])

  for part in parts:
      print "user: %s" % (part['user'])


def get_mongodb(dbUrl, dbPort, dbName, dbUser, dbPswd):
  """
  takes db parameters and returns a connected db object usign those
  parameters

  """
  dbURI = "mongodb://" + dbUser + ":" + dbPswd + "@" + dbUrl + ":" + \
      str(dbPort) + "/" + dbName
  client = MongoClient(dbURI)
  return client[dbName]


if __name__ == '__main__':
  dbUrl = "kahana.mongohq.com"
  dbPort = '10056'
  dbName = 'IdeaGensTest'
  dbUser = 'sandbox'
  dbPswd = 'protolab1'
  db = get_mongodb(ideagenstest['url'],
                   ideagenstest['port'],
                   ideagenstest['dbName'],
                   ideagenstest['user'],
                   ideagenstest['pswd'])

  parts = db.participants.find()

  for part in parts:
      print "id: %s" % (part['_id'])
      print "verification: %i" % (part['verifyCode'])
