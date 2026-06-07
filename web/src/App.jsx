import React from "react";
import { BarList, DataTable, ErrorNotice, MetricCard, RatingBadge, SectionHeading } from "./components.jsx";
import { usePortfolioData } from "./data.js";

const TAXONOMY = [
  "Model performance risk",
  "Fairness and discrimination risk",
  "Consumer harm risk",
  "Hallucination and misinformation risk",
  "Explainability and transparency risk",
  "Robustness and drift risk",
  "Privacy and data access risk",
  "Prompt injection and adversarial misuse risk",
  "Agentic tool-use risk",
  "Governance and accountability risk",
];

const SEVERITY_SCALE = [
  "0: No material issue detected",
  "1: Minor control weakness or documentation gap",
  "2: Material supervisory concern requiring remediation",
  "3: High-impact risk affecting customers, governance, or safety",
];

const LIKELIHOOD_SCALE = [
  "1: Rare in tested scenarios",
  "2: Unlikely but plausible",
  "3: Occasional under realistic use",
  "4: Likely without added controls",
  "5: Recurrent or systemic",
];

function formatNumber(value, digits = 3) {
  return Number(value || 0).toFixed(digits);
}

function formatPercent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

function metricDisplay(metric) {
  if (metric.unit === "%") {
    return formatPercent(metric.value);
  }
  return String(metric.value);
}

function App() {
  const data = usePortfolioData();
  const champion = data.credit.models?.random_forest || {};
  const highRisks = data.riskRegister.filter((risk) => ["critical", "high"].includes(String(risk.rating).toLowerCase()));
  const materialFindings = highRisks.length ? highRisks : data.riskRegister.slice(0, 4);

  return (
    <main>
      <nav className="top-nav" aria-label="Primary navigation">
        <a href="#home">Home</a>
        <a href="#systems">AI Systems</a>
        <a href="#methodology">Methodology</a>
        <a href="#results">Results</a>
        <a href="#risk-register">Risk Register</a>
        <a href="#evidence-pack">Evidence Pack</a>
        <a href="#run-locally">Run Locally</a>
      </nav>

      <section className="hero" id="home">
        <div>
          <p className="eyebrow">Regulatory AI risk review simulator for financial services</p>
          <h1>AI Supervisory Review Simulator for Financial Services</h1>
          <p>
            A regulator-style AI review simulator for a fictional bank, connecting model evidence, GenAI safety testing,
            agentic tool-use controls, and supervisory risk findings.
          </p>
          <div className="hero-actions">
            <a href="#results">View review results</a>
            <a href="#methodology">Read methodology</a>
            <a href="/supervisory_evidence_pack.md">Evidence pack</a>
            <a href="#run-locally">Project notes</a>
          </div>
        </div>
        <aside className="hero-panel">
          <span>Fictional institution</span>
          <strong>Emerald Credit Bank</strong>
          <small>Credit ML, GenAI support, and agentic lending workflow review</small>
        </aside>
      </section>

      {data.status === "error" ? <ErrorNotice message={data.error} /> : null}

      <section className="metrics-grid" aria-label="Key metrics">
        {data.keyMetrics.map((metric) => (
          <MetricCard key={metric.label} label={metric.label} value={metricDisplay(metric)} detail={metric.detail} />
        ))}
      </section>

      <section className="panel" id="why">
        <SectionHeading eyebrow="Why this matters" title="Financial AI Supervision Needs Evidence, Not Product Demos">
          This project demonstrates how an AI risk analyst can turn technical tests into supervisory evidence: measurable
          model performance, fairness gaps, prompt-injection results, tool-call logs, and mitigation actions that a regulator
          or model-risk committee can review.
        </SectionHeading>
      </section>

      <section id="systems">
        <SectionHeading eyebrow="AI system inventory" title="Systems Under Review">
          Three fictional Emerald Credit Bank systems are assessed using a common risk taxonomy and evidence standard.
        </SectionHeading>
        <div className="system-grid">
          {data.systems.map((system) => (
            <article className="system-card" key={system.id}>
              <div className="card-title-row">
                <h3>{system.name}</h3>
                <RatingBadge rating={system.risk_level} />
              </div>
              <p>{system.purpose}</p>
              <dl>
                <dt>Users affected</dt>
                <dd>{system.users_affected}</dd>
                <dt>Evaluated risks</dt>
                <dd>{system.evaluated_risks?.join(", ")}</dd>
              </dl>
              <ul>
                {system.key_findings?.map((finding) => (
                  <li key={finding}>{finding}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section id="methodology">
        <SectionHeading eyebrow="Evaluation methodology" title="Risk Taxonomy, Protocol, And Scoring">
          The methodology combines deterministic synthetic data, statistical model evaluation, structured GenAI test cases,
          agentic tool-use scenarios, and a severity-likelihood-detectability scoring model.
        </SectionHeading>
        <div className="method-grid">
          <article className="panel">
            <h3>Risk Taxonomy</h3>
            <ul className="compact-list">
              {TAXONOMY.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article className="panel">
            <h3>Evaluation Protocol</h3>
            <ol className="compact-list">
              <li>Generate synthetic credit data with affordability, credit history, and proxy-risk features.</li>
              <li>Train Logistic Regression and Random Forest benchmark models.</li>
              <li>Evaluate AUC, precision, recall, F1, Brier score, calibration, fairness, and stress robustness.</li>
              <li>Run 120 GenAI safety cases and 50 agentic tool-use cases.</li>
              <li>Translate failures into a risk register and evidence pack.</li>
            </ol>
          </article>
          <article className="panel">
            <h3>Test Case Design</h3>
            <p>
              Test cases include counterfactual fairness prompts, vulnerable consumer personas, harmful advice requests,
              misleading certainty probes, prompt injection attacks, privacy leakage attempts, and escalation scenarios.
            </p>
          </article>
          <article className="panel">
            <h3>Scoring Rubric</h3>
            <p>Final rating uses severity, likelihood, detectability, and evidence strength.</p>
            <ul className="compact-list">
              {SEVERITY_SCALE.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article className="panel">
            <h3>Likelihood Scale</h3>
            <ul className="compact-list">
              {LIKELIHOOD_SCALE.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article className="panel">
            <h3>Evidence Strength And Limitations</h3>
            <p>
              Evidence strength is low, medium, or high based on repeatability and coverage. Automated evaluation supports
              triage and regression testing, but does not replace independent validation, legal review, or real customer
              monitoring.
            </p>
          </article>
        </div>
      </section>

      <section id="results">
        <SectionHeading eyebrow="Review results" title="Evaluation Results And Supervisory Signals">
          Static JSON files power this simulator, so the public website can be deployed without a backend.
        </SectionHeading>
        <div className="results-layout">
          <article className="panel">
            <h3>Credit Model Metrics</h3>
            <DataTable
              rows={Object.entries(data.credit.models || {}).map(([model, metrics]) => ({ model, ...metrics }))}
              columns={[
                { key: "model", label: "Model" },
                { key: "auc", label: "AUC", render: (value) => formatNumber(value) },
                { key: "precision", label: "Precision", render: (value) => formatNumber(value) },
                { key: "recall", label: "Recall", render: (value) => formatNumber(value) },
                { key: "f1", label: "F1", render: (value) => formatNumber(value) },
                { key: "brier_score", label: "Brier", render: (value) => formatNumber(value) },
              ]}
            />
          </article>
          <article className="panel">
            <h3>Fairness Gaps</h3>
            <DataTable
              rows={data.credit.fairness}
              columns={[
                { key: "group", label: "Group" },
                { key: "n", label: "N" },
                { key: "approval_rate", label: "Approval", render: formatPercent },
                { key: "false_positive_rate", label: "FPR", render: formatPercent },
              ]}
            />
          </article>
          <article className="panel">
            <h3>Calibration And Robustness</h3>
            <div className="stress-grid">
              {Object.entries(data.credit.robustness || {}).map(([key, value]) => (
                <div className="stress-item" key={key}>
                  <span>{key.replaceAll("_", " ")}</span>
                  <strong>{formatNumber(value)}</strong>
                </div>
              ))}
            </div>
          </article>
          <article className="panel">
            <h3>GenAI Risk Rates</h3>
            <div className="mini-metrics">
              <MetricCard label="Harmful advice rate" value={formatPercent(data.genai.summary.harmful_advice_rate)} detail="Failed harmful-advice checks" />
              <MetricCard label="Hallucination rate" value={formatPercent(data.genai.summary.hallucination_rate)} detail="Unsupported claim failures" />
              <MetricCard label="Injection success" value={formatPercent(data.genai.summary.prompt_injection_success_rate)} detail="Prompt bypass failures" />
            </div>
          </article>
          <article className="panel">
            <h3>Agentic Tool-Use Risk</h3>
            <div className="mini-metrics">
              <MetricCard label="Tool misuse rate" value={formatPercent(data.agentic.summary.tool_misuse_rate)} detail="Failed agentic controls" />
              <MetricCard label="Unauthorized use" value={formatPercent(data.agentic.summary.unauthorized_tool_use_failure_rate)} detail="Profile-purpose failures" />
              <MetricCard label="Injection success" value={formatPercent(data.agentic.summary.prompt_injection_success_rate)} detail="Agent prompt bypass failures" />
            </div>
          </article>
          <article className="panel">
            <h3>Failures By Category</h3>
            <BarList rows={[...(data.genai.by_category || []), ...(data.agentic.by_category || [])]} labelKey="risk_category" valueKey="failure_rate" valueFormatter={formatPercent} />
          </article>
        </div>
        <article className="panel critical-examples">
          <h3>Critical Failure Examples</h3>
          <DataTable
            rows={data.failures}
            columns={[
              { key: "id", label: "ID" },
              { key: "system", label: "System" },
              { key: "risk_category", label: "Risk" },
              { key: "severity", label: "Severity" },
              { key: "failure", label: "Failure" },
              { key: "expected_control", label: "Expected control" },
            ]}
          />
        </article>
      </section>

      <section id="risk-register">
        <SectionHeading eyebrow="Risk register" title="Supervisory Findings And Mitigation Plan">
          The register translates test evidence into accountable remediation work.
        </SectionHeading>
        <DataTable
          rows={data.riskRegister}
          columns={[
            { key: "risk_id", label: "Risk ID" },
            { key: "system", label: "System" },
            { key: "category", label: "Risk category" },
            { key: "severity", label: "Severity" },
            { key: "likelihood", label: "Likelihood" },
            { key: "rating", label: "Rating", render: (value) => <RatingBadge rating={value} /> },
            { key: "evidence", label: "Evidence" },
            { key: "mitigation", label: "Mitigation" },
            { key: "owner", label: "Owner" },
          ]}
        />
      </section>

      <section id="evidence-pack">
        <SectionHeading eyebrow="Supervisory evidence pack" title="Executive Summary And Supervisory Letter">
          This section mirrors the evidence pack a regulator-style review might send to a supervised institution.
        </SectionHeading>
        <div className="evidence-grid">
          <article className="panel">
            <h3>Executive Summary</h3>
            <p>
              Emerald Credit Bank's fictional AI estate shows credible evaluation coverage but material residual risks in
              fairness monitoring, agentic authorization, and release-gated GenAI safety testing.
            </p>
          </article>
          <article className="panel">
            <h3>Material Findings</h3>
            <ul className="compact-list">
              {materialFindings.map((risk) => (
                <li key={risk.risk_id}>{risk.finding}</li>
              ))}
            </ul>
          </article>
          <article className="panel">
            <h3>Required Remediation Actions</h3>
            <ul className="compact-list">
              <li>Define management thresholds for fairness gaps, calibration drift, and robustness degradation.</li>
              <li>Expand refusal behavior tests for harmful financial advice and policy-bypass prompts.</li>
              <li>Restrict agentic tools by purpose, consent, and customer-risk context.</li>
              <li>Require human escalation for vulnerable consumers and high-impact lending outcomes.</li>
            </ul>
          </article>
          <article className="panel">
            <h3>Monitoring Recommendations</h3>
            <ul className="compact-list">
              <li>Monthly fairness and calibration MI for the credit model.</li>
              <li>Release-gate regression suite for GenAI prompt injection and vulnerable customer handling.</li>
              <li>Tool-call audit log review for agentic workflow authorization.</li>
              <li>Board-level AI risk register with named owners and due dates.</li>
            </ul>
          </article>
        </div>
        <article className="letter panel">
          <h3>Mock Supervisory Letter Excerpt</h3>
          <p>
            To the Board Risk Committee and Chief Risk Officer of Emerald Credit Bank: the review identified material AI
            governance issues requiring documented remediation within 30, 60, and 90 day supervisory milestones. The bank
            should evidence accountable ownership, monitoring thresholds, independent validation, and human escalation
            controls before expanding automated AI-supported lending workflows.
          </p>
          <a href="/supervisory_evidence_pack.md">Open full generated evidence pack</a>
        </article>
      </section>

      <section id="run-locally">
        <SectionHeading eyebrow="About / run locally" title="Tech Stack, Repository Structure, And Deployment">
          The website is a deployable Vite React app backed by static JSON files. The Python package remains the evaluation
          engine that can regenerate the website evidence layer.
        </SectionHeading>
        <div className="method-grid">
          <article className="panel">
            <h3>Tech Stack</h3>
            <ul className="compact-list">
              <li>React 19 and Vite for the public website.</li>
              <li>Static JSON files under <code>web/public/data</code>.</li>
              <li>Python, pandas, scikit-learn, matplotlib, and pytest for evaluation evidence.</li>
            </ul>
          </article>
          <article className="panel">
            <h3>Repository Structure</h3>
            <pre>{`src/                 Python evaluation pipeline
web/                 React review simulator
web/public/data/     Static JSON website data
outputs/reports/     Evidence pack and supervisory letter
tests/               Pytest coverage`}</pre>
          </article>
          <article className="panel">
            <h3>Run React Site Locally</h3>
            <pre>{`cd web
npm install
npm run dev`}</pre>
          </article>
          <article className="panel">
            <h3>Run Evaluation Pipeline</h3>
            <pre>{`python3 -m src.reporting.generate_report
pytest`}</pre>
          </article>
          <article className="panel">
            <h3>Deploy</h3>
            <p>
              Primary target: Vercel. Build command: <code>npm run build</code>. Output directory: <code>dist</code>.
              Alternative targets: Netlify and GitHub Pages.
            </p>
          </article>
          <article className="panel">
            <h3>GitHub About Link</h3>
            <p>
              After deployment, paste the Vercel URL into the GitHub repository <strong>About</strong> website field so
              reviewers can open this demo directly.
            </p>
          </article>
        </div>
      </section>
    </main>
  );
}

export default App;
