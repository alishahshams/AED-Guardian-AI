import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# ============================================================
# AED Guardian AI - Backend API
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
QUEUE_PATH = BASE_DIR / "duplicate_review_queue.json"

PORT = 8000


# ============================================================
# JSON HELPERS
# ============================================================

def load_queue():
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(data):
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# STATISTICS
# ============================================================

def calculate_stats():
    data = load_queue()

    queue = data.get("review_queue", [])

    duplicates = 0
    not_duplicates = 0
    uncertain = 0
    unreviewed = 0

    for item in queue:

        label = item.get("human_label", "")

        if label == "DUPLICATE":
            duplicates += 1

        elif label == "NOT_DUPLICATE":
            not_duplicates += 1

        elif label == "UNCERTAIN":
            uncertain += 1

        else:
            unreviewed += 1

    reviewed = (
        duplicates
        + not_duplicates
        + uncertain
    )

    if reviewed > 0:
        abstention_rate = uncertain / reviewed
    else:
        abstention_rate = 0

    if unreviewed == 0:
        status = "COMPLETE"
    else:
        status = "IN_REVIEW"

    return {
        "duplicates": duplicates,
        "not_duplicates": not_duplicates,
        "uncertain": uncertain,
        "unreviewed_pairs": unreviewed,
        "reviewed_pairs": reviewed,
        "abstention_rate": abstention_rate,
        "status": status
    }


# ============================================================
# HTTP HANDLER
# ============================================================

class Handler(BaseHTTPRequestHandler):

    # --------------------------------------------------------
    # SEND JSON
    # --------------------------------------------------------

    def send_json(self, data, status=200):

        encoded = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.send_header(
            "Content-Length",
            str(len(encoded))
        )

        self.end_headers()

        self.wfile.write(encoded)


    # --------------------------------------------------------
    # SEND HTML
    # --------------------------------------------------------

    def send_html(self, content):

        encoded = content.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(encoded))
        )

        self.end_headers()

        self.wfile.write(encoded)


    # ========================================================
    # GET REQUESTS
    # ========================================================

    def do_GET(self):

        # ----------------------------------------------------
        # HOME
        # ----------------------------------------------------

        if self.path == "/":

            html = """
            <!DOCTYPE html>

            <html>

            <head>

                <title>AED Guardian AI</title>

                <meta charset="UTF-8">

            </head>

            <body
                style="
                    font-family: Arial;
                    padding: 40px;
                "
            >

                <h1>AED Guardian AI</h1>

                <h2>Backend is running successfully.</h2>

                <p>Available API endpoints:</p>

                <ul>

                    <li>
                        <a href="/api/stats">
                            /api/stats
                        </a>
                    </li>

                    <li>
                        <a href="/api/reviews">
                            /api/reviews
                        </a>
                    </li>

                    <li>
                        <a href="/api/operating-hours">
                            /api/operating-hours
                        </a>
                    </li>

                    <li>
                        <a href="/api/ambiguities">
                            /api/ambiguities
                        </a>
                    </li>

                </ul>

            </body>

            </html>
            """

            self.send_html(html)

            return


        # ----------------------------------------------------
        # STATS
        # ----------------------------------------------------

        if self.path == "/api/stats":

            try:

                stats = calculate_stats()

                self.send_json(stats)

            except Exception as e:

                self.send_json(
                    {
                        "error": str(e)
                    },
                    500
                )

            return


        # ----------------------------------------------------
        # REVIEWS
        # ----------------------------------------------------

        if self.path == "/api/reviews":

            try:

                data = load_queue()

                queue = data.get(
                    "review_queue",
                    []
                )

                self.send_json(
                    {
                        "total_flagged_records": len(queue),
                        "records": queue
                    }
                )

            except Exception as e:

                self.send_json(
                    {
                        "error": str(e)
                    },
                    500
                )

            return


        # ----------------------------------------------------
        # OPERATING HOURS
        # ----------------------------------------------------

        if self.path == "/api/operating-hours":

            self.send_json(
                {
                    "status": "available",
                    "module": "Operating Hours",
                    "analyzed": True,
                    "message":
                        "Operating-hours quality "
                        "analysis module available."
                }
            )

            return


        # ----------------------------------------------------
        # INDOOR LOCATION
        # ----------------------------------------------------

        if self.path == "/api/ambiguities":

            self.send_json(
                {
                    "status": "available",
                    "module": "Indoor Location",
                    "analyzed": True,
                    "message":
                        "Indoor-location ambiguity "
                        "analysis module available."
                }
            )

            return


        # ----------------------------------------------------
        # OLD DATA ENDPOINT
        # ----------------------------------------------------

        if self.path == "/data":

            try:

                data = load_queue()

                queue = data.get(
                    "review_queue",
                    []
                )

                self.send_json(queue)

            except Exception as e:

                self.send_json(
                    {
                        "error": str(e)
                    },
                    500
                )

            return


        # ----------------------------------------------------
        # NOT FOUND
        # ----------------------------------------------------

        self.send_json(
            {
                "error": "Endpoint not found",
                "path": self.path
            },
            404
        )


    # ========================================================
    # POST REQUESTS
    # ========================================================

    def do_POST(self):

        # ----------------------------------------------------
        # HUMAN REVIEW LABEL
        # ----------------------------------------------------

        if self.path == "/label":

            try:

                length = int(
                    self.headers.get(
                        "Content-Length",
                        0
                    )
                )

                body = self.rfile.read(
                    length
                ).decode("utf-8")

                params = parse_qs(body)

                review_id = int(
                    params["review_id"][0]
                )

                label = params["label"][0]

                allowed_labels = {
                    "DUPLICATE",
                    "NOT_DUPLICATE",
                    "UNCERTAIN"
                }

                if label not in allowed_labels:

                    self.send_json(
                        {
                            "error":
                                "Invalid review label"
                        },
                        400
                    )

                    return


                data = load_queue()

                found = False


                for item in data.get(
                    "review_queue",
                    []
                ):

                    if item.get(
                        "review_id"
                    ) == review_id:

                        item[
                            "human_label"
                        ] = label

                        found = True

                        break


                if not found:

                    self.send_json(
                        {
                            "error":
                                "Review ID not found"
                        },
                        404
                    )

                    return


                save_queue(data)


                self.send_json(
                    {
                        "status": "saved",
                        "review_id": review_id,
                        "label": label
                    }
                )

            except Exception as e:

                self.send_json(
                    {
                        "error": str(e)
                    },
                    500
                )

            return


        # ----------------------------------------------------
        # API REVIEW
        # ----------------------------------------------------

        if self.path == "/api/review":

            self.send_json(
                {
                    "error":
                        "Use POST /label "
                        "for review decisions."
                },
                400
            )

            return


        # ----------------------------------------------------
        # NOT FOUND
        # ----------------------------------------------------

        self.send_json(
            {
                "error": "Endpoint not found",
                "path": self.path
            },
            404
        )


    # ========================================================
    # OPTIONS / CORS
    # ========================================================

    def do_OPTIONS(self):

        self.send_response(204)

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" AED Guardian AI - Backend API")
    print("======================================")
    print()

    print("Backend running at:")
    print("http://localhost:8000")

    print()

    print("API endpoints:")

    print(
        "http://localhost:8000/api/stats"
    )

    print(
        "http://localhost:8000/api/reviews"
    )

    print(
        "http://localhost:8000/api/operating-hours"
    )

    print(
        "http://localhost:8000/api/ambiguities"
    )

    print()

    print("Press CTRL+C to stop the server.")

    print()


    server = HTTPServer(
        ("localhost", PORT),
        Handler
    )

    server.serve_forever()