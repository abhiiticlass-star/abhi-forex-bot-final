from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

from data_fetcher import (
    get_market_data
)

from signal_engine import (
    generate_signal
)

from request_tracker import (
    can_make_request,
    record_request,
    get_status
)

from trade_logger import log_signal

app = Flask(__name__)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


@app.route("/api/requests")
def request_status():

    return jsonify(
        get_status()
    )


@app.route("/api/signal")
def signal():

    pair = request.args.get(
        "pair",
        "EUR/USD"
    )

    timeframe = request.args.get(
        "timeframe",
        "1min"
    )

    if not can_make_request():

        return jsonify({

            "signal":
            "DAILY LIMIT CROSSED",

            "confidence": 0,

            "trend":
            "STOPPED",

            "score": 0,

            "support": None,

            "resistance": None,

            "remaining": 0,

            "reasons": [
                "Daily API Limit Reached"
            ]
        })

    try:

        market_data = (
            get_market_data(
                pair,
                timeframe
            )
        )

        result = (
            generate_signal(
                market_data["current"],
                market_data["higher"]
            )
        )

        record_request()

        status = get_status()

        result["remaining"] = (
            status["remaining"]
        )

        result["used"] = (
            status["used"]
        )

        result["limit"] = (
            status["limit"]
        )

        return jsonify(
            result
        )

    except Exception as e:

        return jsonify({

            "signal": "ERROR",

            "confidence": 0,

            "trend": "UNKNOWN",

            "score": 0,

            "support": None,

            "resistance": None,

            "remaining":
            get_status()["remaining"],

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
