import pandas as pd
import re
import json
import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

df = pd.read_csv("seizou-data.csv")
print(df.head())

def normalize(text):
    return re.sub(r"\s+", "", str(text)).upper()

df["受注No"] = df["受注No"].astype(str).apply(normalize)
df["製品名"] = df["製品名"].astype(str).apply(normalize)

@app.route("/search_order", methods=["GET"])
@app.route("/search_order/", methods=["GET"])  # ← スラッシュありにも対応
def search_order():
    keyword = request.args.get("keyword", "")
    keyword_norm = normalize(keyword)

    mask = df["受注No"].str.contains(keyword_norm) | df["製品名"].str.contains(keyword_norm)
    result = df[mask]

    if result.empty:
        return app.response_class(
            response=json.dumps({"result": "ごめんね、まつかりん。該当データは見つからなかったよ。"}, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )

    row = result.iloc[0]
    output = {df.columns[i]: str(row[i]) for i in range(18)}

    return app.response_class(
        response=json.dumps({"result": output}, ensure_ascii=False),
        status=200,
        mimetype="application/json"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
