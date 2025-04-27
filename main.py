from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re

app = Flask(__name__)
CORS(app)

EXCEL_FILE = "seizou-data.xlsx"


def normalize(text):
    return re.sub(r'\s+', '', str(text)).upper()


@app.route("/search_order/", methods=["GET"])
def search_order():
    keyword = request.args.get("keyword", "")
    if not keyword:
        return jsonify({"matches": []})

    try:
        df = pd.read_excel(EXCEL_FILE)
        # 受注Noと製品名の両方を正規化する
        df["受注No"] = df["受注No"].astype(str).apply(normalize)
        df["製品名"] = df["製品名"].astype(str).apply(normalize)

        keyword_norm = normalize(keyword)

        # 受注Noまたは製品名のどちらかに一致するデータを探す
        matches = df[(df["受注No"].str.contains(keyword_norm, na=False)) |
                     (df["製品名"].str.contains(keyword_norm, na=False))]

        result = matches.to_dict(orient="records")
        return jsonify({"matches": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "API is working. Please use /search_order?keyword=XXXX"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
