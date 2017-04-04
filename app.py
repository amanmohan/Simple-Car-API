#!flask/bin/python
import json

from flask import Flask, jsonify,request,abort
from functools import wraps

from sql_crud import DataOperations


app = Flask(__name__)
data_op = DataOperations()
data_op.create_connection()


def delete_ratings_too(f):
    @wraps(f)
    def decorated_function(**k):
        result = delete_rating(k['car_id'])
        if result:
            return f(**k)
        abort(404)
    return decorated_function

@app.route('/api/cars', methods=['GET'])
def get_cars():
    result = data_op.give_cars()
    return jsonify({'result':result})

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    result = data_op.give_ratings()
    return jsonify({'result':result})

@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    result = data_op.give_car(car_id)
    if result == None:
        return jsonify({'result': 'no data'})
    return jsonify({'result':result})

@app.route('/api/ratings/<int:car_id>', methods=['GET'])
def get_rating(car_id):
    result = data_op.give_rating(car_id)
    if result == None:
        return jsonify({'result': 'no data'})
    return jsonify({'result':result})

@app.route('/api/cars', methods=['POST'])
def create_car():
    if not request.json:
        abort(400)
    lst = ['model','year','make']
    for i in lst:
        if not i in request.json:
            abort(400)
    car_info = [
        data_op.return_new_id() + 1,
        request.json['make'],
        request.json['year'],
        request.json['model']
    ]
    responce = data_op.push_car(car_info)
    if responce:
        return jsonify({'results': car_info}), 201
    return jsonify({'results': 'bad data'})

@app.route('/api/ratings', methods=['POST'])
def create_rating():
    if not request.json or not 'id' in request.json:
        abort(400)
    car_id = data_op.give_car(request.json['id'])
    if car_id == 'null' :
        return jsonify({'results': 'no car found'})
    car_rating = [
        request.json['id'],
        request.json['reviewedBy'],
        request.json['performance'],
        request.json['technology'],
        request.json['interior'],
        request.json['reliablity'],
        request.json['Overall']
    ]
    responce = data_op.push_rating(car_rating)
    if responce:
        return jsonify({'results': car_rating}), 201
    return jsonify({'results': 'bad data'})

@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    result = json.loads(data_op.give_car(car_id))
    if not request.json:
        abort(400)
    lst = ['model','year','make']
    for i in lst:
        if i in request.json and type(request.json[i]) is not unicode:
            abort(400)
    car_info = [
                car_id,
                request.json['make'],
                request.json['year'],
                request.json['model']
                ]
    responce = data_op.modify_car(car_info)
    return jsonify({'results': responce})

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
@delete_ratings_too
def delete_car(car_id):
    result = json.loads(data_op.give_car(car_id))
    responce = data_op.remove_car(car_id)
    return jsonify({'result': responce})

@app.route('/api/ratings/<int:car_id>', methods=['PUT'])
def update_rating(car_id):
    result = json.loads(data_op.give_rating(car_id))
    if not request.json:
        abort(400)
    lst = ['Overall','interior','performance','reliablity','reviewedBy','technology']
    for i in lst:
        if i in request.json and type(request.json[i]) is not unicode:
            abort(400)
    rating_info = [
                car_id,
                request.json['Overall'],
                request.json['interior'],
                request.json['performance'],
                request.json['reliablity'],
                request.json['reviewedBy'],
                request.json['technology']
                ]
    responce = data_op.modify_rating(rating_info)
    return jsonify({'results': responce})


@app.route('/api/ratings/<int:car_id>', methods=['DELETE'])
def delete_rating(car_id):
    result = json.loads(data_op.give_rating(car_id))
    responce = data_op.remove_rating(car_id)
    return jsonify({'result': responce})

if __name__ == '__main__':
    app.run(debug=True)
    