from flask import Flask, request, jsonify, render_template
from scipy import stats

app = Flask(__name__)

def one_sample_t_test(data, pop_mean, hypothesis):
    t_stat, p_val = stats.ttest_1samp(
        data,
        pop_mean,
        alternative=hypothesis
    )

    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_val)
    }

@app.route("/")
def home():
    return render_template("app.html")

@app.route("/run_test", methods=["POST"])
def run_test():

    data = request.json["data"]
    pop_mean = float(request.json["pop_mean"])
    hypothesis = request.json["hypothesis"]

    result = one_sample_t_test(data, pop_mean, hypothesis)

    decision = "Reject Null Hypothesis (p < 0.05)" if result["p_value"] < 0.05 else "Fail to Reject Null Hypothesis (p ≥ 0.05)"

    return jsonify({
        "t_statistic": result["t_statistic"],
        "p_value": result["p_value"],
        "decision": decision
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
