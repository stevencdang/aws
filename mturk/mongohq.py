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
                'pswd': 'protolab1' 
                }
# user and paswd are incorrect (do not want to commit secure info
ideagens = {'url': "kahana.mongohq.com",
            'port': 10075,
            'dbName': 'IdeaGens',
            'user': 'experimenter',
            'pswd': '1#dJ3VYSf8Sn5iE9'
            }

# Info for connecting to a local instance of meteor's mongo. 
# Meteor must be running to connect
local_meteor = {'url': "localhost",
                'port': 3001,
                'dbName': 'meteor'
}

def get_db (db=None):
  """
  Returns a handle to an open connection to the mongo db

  """
  if ('user' in db.keys()):
    print "connecting with username and password"
    return get_mongodb(db['url'],
                      db['port'],
                      db['dbName'],
                      db['user'],
                      db['pswd'])
  else:
    print "connecting without username and password"
    return get_mongodb(db['url'],
                      db['port'],
                      db['dbName'])
    


def get_uniq_part (db):
  parts = db.participants.find()
  users = Set()
  # Get set of unique usernames in list of participants
  for part in parts:
    if (part.has_key('user')):
      user = part['user']
      if user != '':
        users.add(user['name'])
  # Perform operations on each username
  # print len(users)
  # for user in users:
      # print user
  return users

def add_excl_parts(db, usernames):
  """
  Add a list of excluded participants based on a set of usernames.
  Can't base on user_id because there are duplicate user_id's with
  the same user name

  """
  desc = "Replicating the effect " + \
          "of priming with common vs rare ideas in individual " + \
          "brainstorming with revised interface"
  exp_id= 'tN33ATDiCukWfj5G7'
  # exps = db.experiments.find()
  exp = db.experiments.find_one({'_id': exp_id})
   
  db.experiments.update({'_id': exp_id},
      {'$set': {'excludeUsers': list(usernames), 'description': desc}})
  # exp['excludeUsers'] = list(usernames)
  exp = db.experiments.find_one({'_id': exp_id})
  print exp['excludeUsers']
  print exp['description']

     



def get_mongodb(dbUrl, dbPort, dbName, dbUser=None, dbPswd=None):
  """
  takes db parameters and returns a connected db object usign those
  parameters

  """
  if ((dbUser != None) and (dbPswd != None)):
    dbURI = "mongodb://" + dbUser + ":" + dbPswd + "@" + dbUrl + ":" + \
        str(dbPort) + "/" + dbName
    print "using uri: " + dbURI
  else:
    dbURI = "mongodb://" + dbUrl + ":" + \
        str(dbPort) + "/" + dbName
    print "using uri: " + dbURI
    
  client = MongoClient(dbURI)
  return client[dbName]


if __name__ == '__main__':
  db = get_db(local_meteor)
  # usernames = get_uniq_part(db)
  # add_excl_parts(db, usernames)
  # db = get_mongodb(ideagenstest['url'],
                   # ideagenstest['port'],
                   # ideagenstest['dbName'],
                   # ideagenstest['user'],
                   # ideagenstest['pswd'])
 
  parts = db.participants.find()

  for part in parts:
      print "id: %s" % (part['_id'])
      print "verification: %i" % (part['verifyCode'])
