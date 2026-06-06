import { useEffect, useState } from "react";

const DATA_FILES = {
  systems: "/data/system_inventory.json",
  keyMetrics: "/data/key_metrics.json",
  riskRegister: "/data/risk_register.json",
  genai: "/data/genai_eval_results.json",
  agentic: "/data/agentic_eval_results.json",
  credit: "/data/credit_model_metrics.json",
  failures: "/data/failure_examples.json",
};

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Missing static data file: ${path}`);
  }
  return response.json();
}

export function usePortfolioData() {
  const [state, setState] = useState({
    status: "loading",
    error: "",
    systems: [],
    keyMetrics: [],
    riskRegister: [],
    genai: { summary: {}, by_category: [] },
    agentic: { summary: {}, by_category: [] },
    credit: { models: {}, fairness: [], robustness: {}, explainability: [] },
    failures: [],
  });

  useEffect(() => {
    Promise.all(Object.values(DATA_FILES).map(fetchJson))
      .then(([systems, keyMetrics, riskRegister, genai, agentic, credit, failures]) => {
        setState({
          status: "ready",
          error: "",
          systems,
          keyMetrics,
          riskRegister,
          genai,
          agentic,
          credit,
          failures,
        });
      })
      .catch((error) => {
        setState((current) => ({
          ...current,
          status: "error",
          error: error.message,
        }));
      });
  }, []);

  return state;
}

