from flask import Flask, Response
from flask_restx import Resource, Api
from core.liquidity import LiquidityCalc
from datetime import date
app = Flask(__name__)
api = Api(app)

@api.route('/liquidity')
class Liquidity(Resource):
    def get(self):
        a = LiquidityCalc()
        df = a.getVol()
        print(df)
        return Response(
                df.to_csv(),
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=df.csv"})
@api.route('/liquidity/today')
class Liquidity(Resource):
    def get(self):
        a = LiquidityCalc()
        df = a.getVol()
        print("HAHA")
        print(df)
        return Response(
                df.to_csv(),
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=df.csv"})

if __name__ == '__main__':
    app.run(debug=True)
