import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const FALLBACK_DATA = {
  project: {
    title: "AI Supervisory Review Simulator for Financial Services",
    bank: "Emerald Credit Bank",
    summary: "Run the Python pipeline to generate current supervisory evidence.",
  },
  inventory: [],
  creditMetrics: {},
  fairness: [],
  robustness: {},
  genaiSummary: { cases: 0, passRate: 0, failedCases: 0, highestSeverity: 0 },
  agenticSummary: { cases: 0, passRate: 0, failedCases: 0, highestSeverity: 0 },
  riskRegister: [],
  explainability: [],
};

function formatPercent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

function formatNumber(value, digits = 3) {
  return Number(value || 0).toFixed(digits);
}

function ratingClass(rating) {
  return `rating rating-${String(rating || "low").toLowerCase()}`;
}

function MetricCard({ label, value, detail }) {
  return (
    <section className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {detail ? <small>{detail}</small> : null}
    </section>
  );
}

function DataTable({ rows, columns, empty = "No data available yet." }) {
  if (!rows?.length) {
    return <p className="empty">{empty}</p>;
  }
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>{column.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row.id || row.system || row.feature || index}>
              {columns.map((column) => (
                <td key={column.key}>{column.render ? column.render(row[column.key], row) : row[column.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function App() {
  const [data, setData] = useState(FALLBACK_DATA);
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    fetch("/dashboard_data.json")
      .then((response) => {
        if (!response.ok) throw new Error("dashboard_data.json not found");
        return response.json();
      })
      .then((payload) => {
        setData(payload);
        setStatus("ready");
      })
      .catch(() => {
        setStatus("missing");
      });
  }, []);

  const championMetrics = data.creditMetrics?.random_forest || data.creditMetrics?.logistic_regression || {};
  const highRisks = useMemo(
    () => (data.riskRegister || []).filter((risk) => ["critical", "high"].includes(String(risk.rating).toLowerCase())),
    [data.riskRegister],
  );

  return (
    <main>
      <header className="hero">
        <div>
          <p className="eyebrow">Fictional supervisory review</p>
          <h1>{data.project.title}</h1>
          <p>{data.project.summary}</p>
        </div>
        <aside className="hero-panel">
          <span>Institution</span>
          <strong>{data.project.bank}</strong>
          <small>{status === "ready" ? "Evidence loaded from generated pipeline artifacts." : "Run the pipeline to refresh evidence."}</small>
        </aside>
      </header>

      {status === "missing" ? (
        <section className="notice">Run <code>python3 -m src.reporting.generate_report</code> to generate the React dashboard data.</section>
      ) : null}

      <section className="metrics-grid">
        <MetricCard label="Credit AUC" value={formatNumber(championMetrics.auc)} detail="Champion model discrimination" />
        <MetricCard label="Brier Score" value={formatNumber(championMetrics.brier_score)} detail="Calibration error proxy" />
        <MetricCard label="GenAI Pass Rate" value={formatPercent(data.genaiSummary.passRate)} detail={`${data.genaiSummary.cases} safety cases`} />
        <MetricCard label="Agentic Pass Rate" value={formatPercent(data.agenticSummary.passRate)} detail={`${data.agenticSummary.cases} tool-use cases`} />
      </section>

      <section>
        <div className="section-heading">
          <p className="eyebrow">Inventory</p>
          <h2>AI Systems Under Review</h2>
        </div>
        <DataTable
          rows={data.inventory}
          columns={[
            { key: "system", label: "System" },
            { key: "purpose", label: "Purpose" },
            { key: "evidence", label: "Evidence" },
          ]}
        />
      </section>

      <section className="two-column">
        <div>
          <div className="section-heading">
            <p className="eyebrow">Model evidence</p>
            <h2>Credit Model Metrics</h2>
          </div>
          <DataTable
            rows={Object.entries(data.creditMetrics || {}).map(([model, metrics]) => ({ model, ...metrics }))}
            columns={[
              { key: "model", label: "Model" },
              { key: "auc", label: "AUC", render: (value) => formatNumber(value) },
              { key: "precision", label: "Precision", render: (value) => formatNumber(value) },
              { key: "recall", label: "Recall", render: (value) => formatNumber(value) },
              { key: "f1", label: "F1", render: (value) => formatNumber(value) },
            ]}
          />
        </div>
        <div>
          <div className="section-heading">
            <p className="eyebrow">Explainability</p>
            <h2>Top Feature Importance</h2>
          </div>
          <DataTable
            rows={(data.explainability || []).slice(0, 8)}
            columns={[
              { key: "feature", label: "Feature" },
              { key: "importance", label: "Importance", render: (value) => formatNumber(value, 4) },
            ]}
          />
        </div>
      </section>

      <section className="two-column">
        <div>
          <div className="section-heading">
            <p className="eyebrow">Fairness</p>
            <h2>Protected Proxy Group Metrics</h2>
          </div>
          <DataTable
            rows={data.fairness}
            columns={[
              { key: "group", label: "Group" },
              { key: "n", label: "N" },
              { key: "approval_rate", label: "Approval", render: (value) => formatPercent(value) },
              { key: "false_positive_rate", label: "FPR", render: (value) => formatPercent(value) },
            ]}
          />
        </div>
        <div>
          <div className="section-heading">
            <p className="eyebrow">Stress testing</p>
            <h2>Robustness Summary</h2>
          </div>
          <div className="stress-grid">
            {Object.entries(data.robustness || {}).map(([key, value]) => (
              <div className="stress-item" key={key}>
                <span>{key.replaceAll("_", " ")}</span>
                <strong>{formatNumber(value)}</strong>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section>
        <div className="section-heading">
          <p className="eyebrow">Supervisory risk register</p>
          <h2>Top Critical And High Findings</h2>
        </div>
        <DataTable
          rows={highRisks.length ? highRisks : data.riskRegister}
          columns={[
            { key: "system", label: "System" },
            { key: "category", label: "Category" },
            { key: "rating", label: "Rating", render: (value) => <span className={ratingClass(value)}>{value}</span> },
            { key: "finding", label: "Finding" },
            { key: "mitigation", label: "Mitigation" },
          ]}
        />
      </section>

      <section className="download-band">
        <div>
          <p className="eyebrow">Evidence pack</p>
          <h2>Generated Supervisory Artifacts</h2>
          <p>Open the generated Markdown reports in <code>outputs/reports</code> for the full supervisory evidence pack and mock letter.</p>
        </div>
        <a href="/supervisory_evidence_pack.md">View Evidence Pack</a>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
