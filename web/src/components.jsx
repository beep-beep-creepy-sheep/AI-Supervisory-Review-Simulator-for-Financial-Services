import React from "react";

export function SectionHeading({ eyebrow, title, children }) {
  return (
    <div className="section-heading">
      <p className="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      {children ? <p>{children}</p> : null}
    </div>
  );
}

export function MetricCard({ label, value, detail, tone = "default" }) {
  return (
    <article className={`metric-card metric-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}

export function RatingBadge({ rating }) {
  return <span className={`rating rating-${String(rating || "low").toLowerCase()}`}>{rating}</span>;
}

export function DataTable({ rows, columns, empty = "No data available." }) {
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
            <tr key={row.risk_id || row.id || row.name || row.system || row.risk_category || index}>
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

export function BarList({ rows, labelKey, valueKey, valueFormatter }) {
  if (!rows?.length) {
    return <p className="empty">No chart data available.</p>;
  }
  const max = Math.max(...rows.map((row) => Number(row[valueKey] || 0)), 0.01);
  return (
    <div className="bar-list">
      {rows.map((row, index) => {
        const value = Number(row[valueKey] || 0);
        return (
          <div className="bar-row" key={`${row[labelKey]}-${index}`}>
            <div className="bar-label">
              <span>{String(row[labelKey]).replaceAll("_", " ")}</span>
              <strong>{valueFormatter ? valueFormatter(value) : value}</strong>
            </div>
            <div className="bar-track">
              <div className="bar-fill" style={{ width: `${Math.max((value / max) * 100, 3)}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function ErrorNotice({ message }) {
  return (
    <section className="notice">
      <strong>Static data could not be loaded.</strong>
      <p>{message}</p>
      <p>
        Run <code>python3 -m src.reporting.generate_report</code> from the repository root, or verify that the files exist under{" "}
        <code>web/public/data</code>.
      </p>
    </section>
  );
}
