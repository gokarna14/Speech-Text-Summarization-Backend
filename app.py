from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
# from security import authenticate, identity
from dbInteractor import Text as TextDB
from dbInteractor import Summary as SummaryDB
from flask_cors import CORS, cross_origin

from model import extractandfeature, get_abs


app = Flask(__name__)
app.secret_key = 'super-secret'
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*",
            "allow_headers": "*", "expose_headers": "*"}})


texts = [
    {"text": "text1"},
    {"text": "text1"},
    {"text": "text1"},
]


class Text(Resource):
    def get(self):
        return TextDB.get_max_id()[0]

    def post(self):
        request_data = request.get_json()
        if not request_data["text"]:
            return {"mes": "No text received !!"}

        # TextDB.add_text(request_data["text"])

        # jsonify is not really necessary when using Flask-restful
        return {"message": "Added", "Text": request_data["text"]}, 201


class TextList(Resource):
    def get(self):
        texts = TextDB.get_all()

        return {'texts': texts}, 200


class TextByID(Resource):
    def get(self, text_id):
        # TextDB.find_by_text_id(text_id)
        return {'text': TextDB.find_by_text_id(text_id)}, 200

    def post(self, text_id):
        request_data = request.get_json()

        if not request_data["text_id"]:
            return {"mes": "No text_id received !!"}

        # jsonify is not really necessary when using Flask-restful
        return {'text': TextDB.find_by_text_id(request_data['text_id'])}, 201


class Summarization(Resource):

    def post(self):
        request_data = request.get_json()

        summary = request_data['summary']
        compression_ratio = request_data["compression_ratio"]

        # print("\n\n\n")
        # print(compression_ratio)

        text_id = request_data["text_id"]

        SummaryDB.add_summary(summary, compression_ratio, text_id)

        # jsonify is not really necessary when using Flask-restful
        return {"message": "Summary adding Task Successful", "summary": request_data['summary']}, 201


class SummaryList(Resource):
    def get(self):
        summaries = SummaryDB.get_all()

        return {'summaries': summaries}, 200

    def post(self):
        request_data = request.get_json()

        if "text_id" in request_data.keys():
            id_of = "text_id"
        else:
            id_of = "summarization_id"

        id_ = request_data[id_of]

        # jsonify is not really necessary when using Flask-restful
        return {"summaries": SummaryDB.get_by_Id(id_, id_of)}, 201


class GenerateSummary(Resource):
    def post(self):
        request_data = request.get_json()

        print("\n\nRequest Data:\n")

        print(request_data)

        summary = extractandfeature(
            request_data["text"], request_data["compression_ratio"])

        print("\n\n")

        print(summary)
        print("\n\n")

        return summary, 201



class GenerateAbsSummary(Resource):
    def get(self):
        print("Inside get")

        return {"message" : "This is the return"}
    def post(self):
        request_data = request.get_json()

        print("\n\nRequest Data:\n")

        print(request_data)

        # summary = extractandfeature(
        #     request_data["text"], request_data["compression_ratio"])

        summary = get_abs(request_data["text"])

        print("\n\n")

        print(summary)
        print("\n\n")

        return {"summary": summary}, 201


@app.route('/')
def hello():
    return 'Hello, World!'


# @app.route('/generateSummary', methods=['POST'])
# def generateSummary():
#     extractandfeature(text, compression_ratio)


api.add_resource(Text, '/text')
api.add_resource(TextList, '/texts')
api.add_resource(TextByID, '/textByID/<string:text_id>')

api.add_resource(Summarization, '/summary')
api.add_resource(SummaryList, '/summaries')

api.add_resource(GenerateSummary, '/generate_summary')
api.add_resource(GenerateAbsSummary, '/generateAbs_summary')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
