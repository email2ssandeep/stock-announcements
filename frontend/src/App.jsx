import { useState, useEffect, useMemo } from "react";
import Header from "./components/Header";
import FilterBar from "./components/FilterBar";
import DateGroup from "./components/DateGroup";
import { parseScreenerDate, formatGroupDate, formatCardDate, groupByDate } from "./utils/dateUtils";

const TICKER_MAP = {
  infosys: "Infosys",
  hcl: "HCL",
  reliance: "Reliance",
  tcs: "TCS",
};

function flattenAndEnrich(apiData) {
  const flat = [];
  Object.entries(apiData).forEach(([ticker, items]) => {
    items.forEach((item) => {
      const parsedDate = parseScreenerDate(item.date);
      flat.push({
        ...item,
        company: ticker,
        companyLabel: TICKER_MAP[ticker] || ticker,
        parsedDate,
        groupKey: parsedDate ? parsedDate.toDateString() : "unknown",
        groupLabel: formatGroupDate(parsedDate),
        cardDate: formatCardDate(parsedDate, item.date),
      });
    });
  });

  // Sort all items newest-first
  flat.sort((a, b) => {
    if (!a.parsedDate) return 1;
    if (!b.parsedDate) return -1;
    return b.parsedDate - a.parsedDate;
  });

  return flat;
}

export default function App() {
  const [apiData, setApiData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState("All");

  useEffect(() => {
    fetch("/api/announcements")
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((d) => { setApiData(d); setLoading(false); })
      .catch(() => { setError(true); setLoading(false); });
  }, []);

  const allAnnouncements = useMemo(() => flattenAndEnrich(apiData), [apiData]);

  const filtered = useMemo(() => {
    if (selectedCompany === "All") return allAnnouncements;
    const key = Object.entries(TICKER_MAP).find(([, v]) => v === selectedCompany)?.[0];
    return allAnnouncements.filter((a) => a.company === key);
  }, [allAnnouncements, selectedCompany]);

  const groups = useMemo(() => groupByDate(filtered), [filtered]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <FilterBar
        selected={selectedCompany}
        onSelect={setSelectedCompany}
        total={filtered.length}
      />

      <main className="max-w-6xl mx-auto px-6 py-6">
        {/* Page title */}
        <div className="mb-5">
          <h1 className="text-lg font-bold text-gray-800">Announcement Alerts</h1>
          <p className="text-xs text-gray-400 mt-0.5">
            Infosys · HCL · Reliance · TCS — sourced from Screener.in · refreshes every 30 min
          </p>
        </div>

        {loading && (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-lg border border-gray-200 p-5 animate-pulse">
                <div className="h-3 bg-gray-100 rounded w-24 mb-3" />
                <div className="h-4 bg-gray-100 rounded w-48 mb-2" />
                <div className="h-3 bg-gray-100 rounded w-full" />
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-5 text-sm text-red-600">
            Could not load announcements. Please check the backend is running and try again.
          </div>
        )}

        {!loading && !error && groups.length === 0 && (
          <div className="text-center py-16 text-gray-400 text-sm">
            No announcements found.
          </div>
        )}

        {!loading && !error && groups.map((group) => (
          <DateGroup
            key={group.label}
            label={group.label}
            items={group.items}
          />
        ))}
      </main>
    </div>
  );
}
