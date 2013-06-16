import redis
import simplejson
import random
import HTMLParser
from terms import get_terms
from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def terms():
    return get_terms(request.form['text'])

@app.route("/profile", methods=['POST'])
def profile():
    if request.method == 'POST':
        r = get_redis_conn()
        id = request.form['id']        
        if not r.get(id):
            print "set", id
            r.set(id, request.form['profile'])
        
    return 'OK'

@app.route("/rate", methods=['POST'])
def rate_profile():
    r = get_redis_conn()
    id = request.form['id']
    rating = request.form['rating']
    
    r.set('rating-'+id, float(rating))
    update_rankings(r, id, rating)
    
    return 'OK'

@app.route("/rank", methods=['GET'])
def rank():
    ids = simplejson.loads(request.args.get('ids', '[]'))
    id_ranks = {}

    r = get_redis_conn()
    for i in ids:
        rating = r.get('rating-'+i)
        if rating:
            id_ranks[i] = rating
        else:
            id_ranks[i] = random.random()

    return simplejson.dumps(id_ranks)

@app.route("/skills", methods=['GET'])
def skills():
    r = get_redis_conn()
    skills = r.keys('skill-*')
    return simplejson.dumps(zip(skills, r.mget(skills)))

def update_rankings(r, id, rating):
    profile = simplejson.loads(r.get(id))
    for skill in profile['content']['Skills']['skillsMpr']['skills']:
        skill = skill['fmt__skill_name']
        r.incr('skill-'+skill, rating)

def get_redis_conn():
    return redis.StrictRedis(host='localhost', port=6379, db=10)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
