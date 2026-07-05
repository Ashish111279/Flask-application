import json
import os
from flask import Flask, jsonify, request, abort, render_template

app = Flask(__name__)
DATA_FILE = 'school_records.json'

DEFAULT_RECORDS = [
    {
        'id': 1,
        'name': 'John Doe',
        'grade': '10',
        'section': 'A',
        'marks': {'math': 85, 'science': 90, 'english': 88}
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'grade': '11',
        'section': 'B',
        'marks': {'math': 92, 'science': 89, 'english': 94}
    }
]


def load_records():
    if not os.path.exists(DATA_FILE):
        save_records(DEFAULT_RECORDS)
    with open(DATA_FILE, 'r', encoding='utf-8') as fp:
        return json.load(fp)


def save_records(records):
    with open(DATA_FILE, 'w', encoding='utf-8') as fp:
        json.dump(records, fp, indent=2)


def find_record(records, record_id):
    return next((record for record in records if record['id'] == record_id), None)


def get_next_id(records):
    if not records:
        return 1
    return max(record['id'] for record in records) + 1


@app.route('/')
def home():
    return jsonify(message='School Records API', version='1.0')


@app.route('/ui')
def ui():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify(status='healthy')


@app.route('/records', methods=['GET'])
def list_records():
    return jsonify(load_records())


@app.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    records = load_records()
    record = find_record(records, record_id)
    if record is None:
        abort(404, description='Record not found')
    return jsonify(record)


@app.route('/records', methods=['POST'])
def create_record():
    if not request.is_json:
        abort(400, description='JSON payload required')

    payload = request.get_json()
    required_fields = ['name', 'grade', 'section', 'marks']
    if not all(field in payload for field in required_fields):
        abort(400, description='Missing required fields')

    records = load_records()
    new_record = {
        'id': get_next_id(records),
        'name': payload['name'],
        'grade': payload['grade'],
        'section': payload['section'],
        'marks': payload['marks']
    }
    records.append(new_record)
    save_records(records)
    return jsonify(new_record), 201


@app.route('/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    if not request.is_json:
        abort(400, description='JSON payload required')

    payload = request.get_json()
    records = load_records()
    record = find_record(records, record_id)
    if record is None:
        abort(404, description='Record not found')

    if 'name' in payload:
        record['name'] = payload['name']
    if 'grade' in payload:
        record['grade'] = payload['grade']
    if 'section' in payload:
        record['section'] = payload['section']
    if 'marks' in payload:
        record['marks'] = payload['marks']

    save_records(records)
    return jsonify(record)


@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    records = load_records()
    record = find_record(records, record_id)
    if record is None:
        abort(404, description='Record not found')

    records = [item for item in records if item['id'] != record_id]
    save_records(records)
    return jsonify({'deleted': record_id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
