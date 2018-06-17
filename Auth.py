import rsa
import base64
from rsa import PublicKey, PrivateKey
import uuid
from tinydb import TinyDB, Query
from pprint import pprint


db   = TinyDB('user.json')
User = Query()


(pubkey, privkey) = None



def createToken(name, sig):
    sig = base64.urlsafe_b64decode(sig)
    if(rsa.verify(name.encode('utf-8'), sig, pubkey)):
        token_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode()
        entry = {
            'token_id':token_id,
            'name':name,
            'collected':False
        }
        db.insert(entry)
        return [token_id]


def collectToken(token_id):
    entry = db.search((User['token_id'] == token_id) and (User.collected == False))
    pprint(entry)
    entry = entry[0]
    entry['collected'] = True
    db.update(entry, doc_ids=[entry.doc_id])
    return entry
    

def lookupToken(token_id):
    res = db.get(User.token_id == token_id and User.collected == True)
    return res
