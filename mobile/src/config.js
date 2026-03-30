// ── Update API_BASE_URL with your Railway public URL ──────────────────────
// e.g. "https://stock-announcements.up.railway.app"
// Leave as localhost for local development (run backend on port 8000)
export const API_BASE_URL = "https://stock-announcements.up.railway.app";

export const ENDPOINTS = {
  announcements: `${API_BASE_URL}/api/announcements`,
  health: `${API_BASE_URL}/api/health`,
};

export const COMPANY_LABELS = {
  infosys: "Infosys Ltd.",
  hcl: "HCL Technologies Ltd.",
  reliance: "Reliance Industries Ltd.",
  tcs: "TCS Ltd.",
};

export const COMPANIES = ["All", "Infosys", "HCL", "Reliance", "TCS"];

export const TICKER_MAP = {
  infosys: "Infosys",
  hcl: "HCL",
  reliance: "Reliance",
  tcs: "TCS",
};
