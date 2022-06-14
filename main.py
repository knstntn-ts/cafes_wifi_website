from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}





@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=cafes)


@app.route('/random', methods=["POST", "GET"])
def random_cafe_fun():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all', methods=["POST", "GET"])
def all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route('/search', methods=["GET"])
def search():
    location = request.args.get('loc')
    located_cafes = db.session.query(Cafe).filter_by(location=location).first()

    if located_cafes:
        return jsonify(cafe=located_cafes.to_dict())
    else:
        return jsonify(error='Not found')


## HTTP GET - Read Record

## HTTP POST - Create Record
@app.route("/add", methods=["POST", "GET"])
def post_new_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url='map img',
            img_url=request.form.get("img_url"),
            location='somewhere',
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=True,
            seats=25,
            coffee_price=4,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html')

## Update cafe info
@app.route('/update_info/<cafe_id>', methods=['GET', 'POST'])
def update_info_cafe(cafe_id):

    cafe_to_update = db.session.query(Cafe).get(int(cafe_id))

    if request.method == 'POST':
        if request.form['name']:
            cafe_to_update.name = request.form['name']
        if request.form['img_url']:
            cafe_to_update.img_rl = request.form['img_url']
        if request.form['has_sockets']:
            cafe_to_update.has_sockets = bool(request.form['has_sockets'])
        if request.form['has_wifi']:
            cafe_to_update.has_wifi = bool(request.form['has_wifi'])
        if request.form['has_toilet']:
            cafe_to_update.has_toilet = bool(request.form['has_toilet'])
        db.session.commit()
        print(f'updated cafe {cafe_to_update}')
        cafes = db.session.query(Cafe).all()
        return redirect('/')

    else:
        if cafe_to_update:
            return render_template('update_info.html', cafe=cafe_to_update)
        else:
            return render_template('index.html')



## HTTP DELETE - Delete Record
# @app.route("/report-closed/<cafe_id>", methods=["DELETE"])
@app.route('/report-closed/<cafe_id>', methods=['GET', 'POST'])
def delete_cafe(cafe_id):

    if request.method == 'GET':
        cafe_to_delete = db.session.query(Cafe).get(int(cafe_id))
        print(cafe_to_delete)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()

    else:
        print('error deleting')

    return redirect('/')

    # api_key = request.args.get('api-key')
    # if api_key == 'secret_key':
    #     cafe_to_delete = db.session.query(Cafe).get(int(cafe_id))
    #     if cafe_to_delete:
    #         db.session.delete(cafe_to_delete)
    #         db.session.commit()
    #         return jsonify(response={"success": "updated the coffee price"})
    #     else:
    #         return jsonify(error={'error': 'this id does not exist'})
    # else:
    #     return jsonify(error={'error': 'Sorry you do not have access to do this'})


if __name__ == '__main__':
    app.run(debug=True)
