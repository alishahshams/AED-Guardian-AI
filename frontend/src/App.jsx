import { useEffect, useState } from "react";
import "./App.css";

// ============================================================
// AED Guardian AI - Frontend ↔ Backend Connection
// Backend: http://127.0.0.1:8000
// ============================================================

const API_URL = "http://127.0.0.1:8000";

// ============================================================
// FALLBACK DATA
// ============================================================

const fallbackStats = {
  duplicates: 0,
  not_duplicates: 92,
  uncertain: 3,
  unreviewed_pairs: 5,
  reviewed_pairs: 95,
  abstention_rate: 0.031578947368421054,
  status: "IN_REVIEW",
};

const fallbackReviews = {
  total_flagged_records: 100,
  records: [],
};

const fallbackModule = {
  status: "available",
  analyzed: true,
};

// ============================================================
// APP
// ============================================================

function App() {
  const [stats, setStats] = useState(fallbackStats);
  const [reviews, setReviews] = useState(fallbackReviews);

  const [operatingHours, setOperatingHours] =
    useState(fallbackModule);

  const [ambiguities, setAmbiguities] =
    useState(fallbackModule);

  const [backendConnected, setBackendConnected] =
    useState(false);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // ==========================================================
  // LOAD BACKEND DATA
  // ==========================================================

  useEffect(() => {
    async function loadDashboardData() {
      try {
        setLoading(true);

        const [
          statsResponse,
          reviewsResponse,
          hoursResponse,
          ambiguityResponse,
        ] = await Promise.all([
          fetch(`${API_URL}/api/stats`),
          fetch(`${API_URL}/api/reviews`),
          fetch(`${API_URL}/api/operating-hours`),
          fetch(`${API_URL}/api/ambiguities`),
        ]);

        if (
          !statsResponse.ok ||
          !reviewsResponse.ok ||
          !hoursResponse.ok ||
          !ambiguityResponse.ok
        ) {
          throw new Error(
            "One or more backend API requests failed."
          );
        }

        const statsData =
          await statsResponse.json();

        const reviewsData =
          await reviewsResponse.json();

        const hoursData =
          await hoursResponse.json();

        const ambiguityData =
          await ambiguityResponse.json();

        // Update with real backend data
        setStats(statsData);
        setReviews(reviewsData);
        setOperatingHours(hoursData);
        setAmbiguities(ambiguityData);

        setBackendConnected(true);
        setError("");
      } catch (err) {
        console.error(
          "Dashboard connection error:",
          err
        );

        setBackendConnected(false);

        setError(
          "Backend is not reachable. Showing fallback data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboardData();
  }, []);

  // ==========================================================
  // CALCULATIONS
  // ==========================================================

  const reviewedPairs = Number(
    stats?.reviewed_pairs ?? 0
  );

  const unreviewedPairs = Number(
    stats?.unreviewed_pairs ?? 0
  );

  const abstentionRate =
    Number(stats?.abstention_rate ?? 0) * 100;

  const isHoursAnalyzed =
    Boolean(operatingHours?.analyzed);

  const isAmbiguityAnalyzed =
    Boolean(ambiguities?.analyzed);

  const isReviewCompleted =
    unreviewedPairs === 0;

  const totalPairs =
    reviewedPairs + unreviewedPairs;

  const reviewProgress =
    totalPairs > 0
      ? Math.round(
          (reviewedPairs / totalPairs) * 100
        )
      : 0;

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div className="app">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="header">

        <div className="header-brand">

          <div className="brand-mark">
            <span>+</span>
          </div>

          <div>
            <h1>AED Guardian AI</h1>

            <p>
              AED Registry Quality Support System
            </p>
          </div>

        </div>

        <div
          className={
            backendConnected
              ? "status connected"
              : "status"
          }
        >
          <span className="status-dot"></span>

          {loading
            ? "Connecting..."
            : backendConnected
            ? "Backend Connected"
            : "Backend Offline"}
        </div>

      </header>

      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="dashboard">

        {/* ====================================================
            HERO
        ==================================================== */}

        <section className="hero">

          <div className="hero-content">

            <span className="badge">
              LANE 3 · REGISTRY QUALITY
            </span>

            <h2>
              Improve AED registry data quality
              with AI-assisted review.
            </h2>

            <p>
              Analyze duplicate records, uncertain
              matches, operating-hours quality, and
              indoor-location ambiguity.
            </p>

            <div className="hero-tags">

              <span>AI-Assisted</span>

              <span>
                Human-in-the-loop
              </span>

              <span>Safety-first</span>

            </div>

          </div>

          <div className="hero-visual">

            <div className="hero-circle circle-one"></div>

            <div className="hero-circle circle-two"></div>

            <div className="aed-card">

              <div className="aed-cross">
                +
              </div>

              <strong>AED</strong>

              <span>
                Guardian AI
              </span>

            </div>

          </div>

        </section>

        {/* ====================================================
            CONNECTION NOTICE
        ==================================================== */}

        {error && (
          <div className="error">

            <div className="error-icon">
              !
            </div>

            <div>

              <strong>
                Backend Connection Notice
              </strong>

              <span>
                {error}
              </span>

            </div>

          </div>
        )}

        {/* ====================================================
            STATISTICS
        ==================================================== */}

        <section className="stats-grid">

          {/* REVIEWED */}

          <div className="card">

            <div className="card-heading">

              <span>
                Reviewed Pairs
              </span>

              <div className="card-icon blue">
                R
              </div>

            </div>

            <strong>
              {reviewedPairs}
            </strong>

            <small>
              Human-reviewed candidate pairs
            </small>

          </div>

          {/* DUPLICATES */}

          <div className="card duplicate">

            <div className="card-heading">

              <span>
                Duplicates
              </span>

              <div className="card-icon red">
                D
              </div>

            </div>

            <strong>
              {stats.duplicates}
            </strong>

            <small>
              Confirmed duplicate pairs
            </small>

          </div>

          {/* NOT DUPLICATE */}

          <div className="card valid">

            <div className="card-heading">

              <span>
                Not Duplicate
              </span>

              <div className="card-icon green">
                ✓
              </div>

            </div>

            <strong>
              {stats.not_duplicates}
            </strong>

            <small>
              Confirmed distinct records
            </small>

          </div>

          {/* UNCERTAIN */}

          <div className="card uncertain">

            <div className="card-heading">

              <span>
                Uncertain
              </span>

              <div className="card-icon orange">
                ?
              </div>

            </div>

            <strong>
              {stats.uncertain}
            </strong>

            <small>
              Requires cautious interpretation
            </small>

          </div>

        </section>

        {/* ====================================================
            ANALYSIS
        ==================================================== */}

        <section className="analysis-grid">

          {/* HUMAN REVIEW */}

          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="section-label">
                  REVIEW WORKFLOW
                </span>

                <h3>
                  Human Review Status
                </h3>

              </div>

              <span className="complete">
                {stats.status}
              </span>

            </div>

            <div className="progress">

              <div
                className="progress-bar"
                style={{
                  width: `${reviewProgress}%`,
                }}
              ></div>

            </div>

            <p className="panel-description">

              {unreviewedPairs > 0
                ? `${unreviewedPairs} candidate pairs are still awaiting human review.`
                : "All candidate pairs in the review queue have been processed."}

            </p>

            <div className="review-info">

              <div>

                <strong>
                  {unreviewedPairs}
                </strong>

                <span>
                  Unreviewed
                </span>

              </div>

              <div>

                <strong>
                  {Math.round(abstentionRate)}%
                </strong>

                <span>
                  Abstention Rate
                </span>

              </div>

              <div>

                <strong>
                  {reviewedPairs}
                </strong>

                <span>
                  Reviewed
                </span>

              </div>

            </div>

          </div>

          {/* QUALITY ANALYSIS */}

          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="section-label">
                  DATA QUALITY
                </span>

                <h3>
                  Quality Analysis
                </h3>

              </div>

              <span className="module-count">
                4 MODULES
              </span>

            </div>

            <div className="quality-list">

              <div className="quality-item">

                <div className="quality-name">

                  <span className="quality-dot green-dot"></span>

                  Duplicate Detection

                </div>

                <b>
                  Completed
                </b>

              </div>

              <div className="quality-item">

                <div className="quality-name">

                  <span className="quality-dot blue-dot"></span>

                  Operating Hours

                </div>

                <b>
                  {isHoursAnalyzed
                    ? "Analyzed"
                    : "Pending"}
                </b>

              </div>

              <div className="quality-item">

                <div className="quality-name">

                  <span className="quality-dot orange-dot"></span>

                  Indoor Location

                </div>

                <b>
                  {isAmbiguityAnalyzed
                    ? "Analyzed"
                    : "Pending"}
                </b>

              </div>

              <div className="quality-item">

                <div className="quality-name">

                  <span className="quality-dot purple-dot"></span>

                  Human Review

                </div>

                <b>
                  {isReviewCompleted
                    ? "Completed"
                    : "In Review"}
                </b>

              </div>

            </div>

          </div>

        </section>

        {/* ====================================================
            BACKEND MODULES
        ==================================================== */}

        <section className="panel backend-summary">

          <div className="panel-header">

            <div>

              <span className="section-label">
                SYSTEM STATUS
              </span>

              <h3>
                Backend Analysis Modules
              </h3>

            </div>

            <span className="complete">

              {backendConnected
                ? "CONNECTED"
                : "OFFLINE"}

            </span>

          </div>

          <div className="module-grid">

            {/* DUPLICATE */}

            <div className="module">

              <div className="module-icon duplicate-icon">
                D
              </div>

              <div className="module-content">

                <strong>
                  Duplicate Detection
                </strong>

                <p>
                  Identifies potential duplicate
                  AED records.
                </p>

              </div>

              <span className="module-check">
                ✓
              </span>

            </div>

            {/* HOURS */}

            <div className="module">

              <div className="module-icon hours-icon">
                H
              </div>

              <div className="module-content">

                <strong>
                  Operating Hours
                </strong>

                <p>
                  Evaluates quality and
                  completeness of hours data.
                </p>

              </div>

              <span className="module-check">
                ✓
              </span>

            </div>

            {/* LOCATION */}

            <div className="module">

              <div className="module-icon location-icon">
                L
              </div>

              <div className="module-content">

                <strong>
                  Indoor Location
                </strong>

                <p>
                  Flags ambiguous indoor AED
                  locations.
                </p>

              </div>

              <span className="module-check">
                ✓
              </span>

            </div>

            {/* HUMAN REVIEW */}

            <div className="module">

              <div className="module-icon review-icon">
                ✓
              </div>

              <div className="module-content">

                <strong>
                  Human Review
                </strong>

                <p>
                  Supports cautious review of
                  uncertain records.
                </p>

              </div>

              <span className="module-check">
                ✓
              </span>

            </div>

          </div>

        </section>

        {/* ====================================================
            REVIEW QUEUE
        ==================================================== */}

        <section className="panel review-queue">

          <div className="panel-header">

            <div>

              <span className="section-label">
                HUMAN-IN-THE-LOOP
              </span>

              <h3>
                Duplicate Review Queue
              </h3>

              <p className="panel-description">
                Candidate AED pairs flagged for
                human duplicate review.
              </p>

            </div>

            <span className="flagged">

              {reviews.total_flagged_records} FLAGGED

            </span>

          </div>

          <div className="table-wrapper">

            <table>

              <thead>

                <tr>

                  <th>
                    Review ID
                  </th>

                  <th>
                    AED Pair
                  </th>

                  <th>
                    Building
                  </th>

                  <th>
                    Distance
                  </th>

                  <th>
                    Confidence
                  </th>

                  <th>
                    Human Label
                  </th>

                  <th>
                    Reason
                  </th>

                </tr>

              </thead>

              <tbody>

                {reviews.records.length === 0 ? (

                  <tr>

                    <td
                      colSpan="7"
                      style={{
                        textAlign: "center",
                        padding: "30px",
                      }}
                    >
                      No review records available.
                    </td>

                  </tr>

                ) : (

                  reviews.records.map(
                    (record) => (

                      <tr
                        key={record.review_id}
                      >

                        {/* REVIEW ID */}

                        <td>

                          <strong className="aed-id">
                            #{record.review_id}
                          </strong>

                        </td>

                        {/* AED IDS */}

                        <td>

                          <div className="location-cell">

                            <strong>
                              {record.AED_ID_1}
                            </strong>

                            <small>
                              ↔ {record.AED_ID_2}
                            </small>

                          </div>

                        </td>

                        {/* BUILDINGS */}

                        <td>

                          <div className="location-cell">

                            <strong>
                              {record.building_1 ||
                                "Not provided"}
                            </strong>

                            <small>
                              {record.building_2 ||
                                "Not provided"}
                            </small>

                          </div>

                        </td>

                        {/* DISTANCE */}

                        <td>

                          {record.distance_meters !==
                          undefined
                            ? `${record.distance_meters} m`
                            : "N/A"}

                        </td>

                        {/* CONFIDENCE */}

                        <td>

                          <span className="confidence">

                            {record.confidence ||
                              "N/A"}

                          </span>

                        </td>

                        {/* HUMAN LABEL */}

                        <td>

                          <span
                            className={`review-status ${
                              record.human_label ===
                              "DUPLICATE"
                                ? "duplicate-status"
                                : record.human_label ===
                                  "UNCERTAIN"
                                ? "uncertain-status"
                                : record.human_label ===
                                  "UNREVIEWED"
                                ? "unreviewed-status"
                                : "not-duplicate-status"
                            }`}
                          >

                            {record.human_label ||
                              "UNREVIEWED"}

                          </span>

                        </td>

                        {/* REASON */}

                        <td className="reason">

                          {record.reason ||
                            "No reason provided."}

                        </td>

                      </tr>

                    )
                  )

                )}

              </tbody>

            </table>

          </div>

          <div className="review-note">

            <span>ⓘ</span>

            <p>

              Candidate pairs are not confirmed
              duplicates. Human review is required
              before making a final duplicate
              determination.

            </p>

          </div>

        </section>

        {/* ====================================================
            SAFETY
        ==================================================== */}

        <section className="safety">

          <div className="safety-icon">
            !
          </div>

          <div>

            <h3>
              Safety Notice
            </h3>

            <p>

              AED Guardian AI is a registry-quality
              support system. Dataset records do
              not guarantee that an AED is currently
              present, accessible, functional, or
              medically ready for use. Always verify
              real-world availability through
              appropriate emergency services or
              authorized sources.

            </p>

          </div>

        </section>

        {/* ====================================================
            FOOTER
        ==================================================== */}

        <footer>

          <div className="footer-brand">

            <strong>
              AED Guardian AI
            </strong>

            <span>
              Registry Quality Support System
            </span>

          </div>

          <span>
            Phase 2 Evaluation · August 2026
          </span>

        </footer>

      </main>

    </div>
  );
}

export default App;