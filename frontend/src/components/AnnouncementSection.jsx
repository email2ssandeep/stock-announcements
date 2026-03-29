import AnnouncementCard from "./AnnouncementCard";

const COMPANY_LABELS = {
  infosys: "Infosys",
  hcl: "HCL",
  reliance: "Reliance",
  tcs: "TCS",
};

function CompanyPanel({ ticker, announcements }) {
  const label = COMPANY_LABELS[ticker] || ticker.toUpperCase();

  return (
    <div className="bg-brand-light rounded-xl p-5">
      <h3 className="text-base font-bold text-brand-blue mb-3 border-b border-blue-200 pb-2">
        {label}
      </h3>
      {announcements.length === 0 ? (
        <p className="text-sm text-gray-400 italic">No announcements available.</p>
      ) : (
        <div className="space-y-3">
          {announcements.map((ann, i) => (
            <AnnouncementCard
              key={i}
              date={ann.date}
              title={ann.title}
              sourceUrl={ann.source_url}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function AnnouncementSection({ data, loading, error }) {
  const companies = ["infosys", "hcl", "reliance", "tcs"];

  return (
    <section className="mt-8">
      <h2 className="text-xl font-bold text-brand-blue mb-6 flex items-center gap-2">
        <span className="inline-block w-2 h-6 bg-brand-accent rounded-sm"></span>
        Announcement Alerts
      </h2>

      {loading && (
        <p className="text-sm text-gray-500 animate-pulse">Loading announcements…</p>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-600">
          Could not load announcements. Please try again later.
        </div>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
          {companies.map((ticker) => (
            <CompanyPanel
              key={ticker}
              ticker={ticker}
              announcements={data[ticker] || []}
            />
          ))}
        </div>
      )}
    </section>
  );
}
