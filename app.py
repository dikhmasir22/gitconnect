from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://dava:123@cluster0.67ahwvv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbwishlist

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    wishlist = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num' : num,
        'bucket' : wishlist,
        'done' : 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data Saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num' : int(num_receive) },
        {'$set' : {'done' : 1 }}
    )
    return jsonify({'msg': 'Data diperbarui!'})


@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num' : int(num_receive) },
        {'$set' : {'done' : 2 }}
    )
    db.bucket.delete_one({'done': 2})
    return jsonify({'msg': 'Data dihapus!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    wish_list = list(db.bucket.find({}, {'_id' : False}))
    return jsonify({'wishlist': wish_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

# https://cloud.mongodb.com/    url 