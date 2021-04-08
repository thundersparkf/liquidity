from flask import Flask, Response
from flask_restx import Resource, Api
from core.liquidity import LiquidityCalc
from datetime import date
app = Flask(__name__)
api = Api(app)

@api.route('/liquidity')
class Liquidity(Resource):
    @staticmethod
    def get():
        a = LiquidityCalc()
        df = a.getVol()
        dt = date.today()
        dt = str(dt.day)+'-'+str(dt.month)+'-'+str(dt.year)
        print(df)
        return Response(
                df.to_csv(),
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename="+dt+".csv"})
@api.route('/liquidity/today')
class Liquidity(Resource):
    @staticmethod
    def get():
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
