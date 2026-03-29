const COMPANY_LABELS = {
  infosys: "Infosys Ltd.",
  hcl: "HCL Technologies Ltd.",
  reliance: "Reliance Industries Ltd.",
  tcs: "TCS Ltd.",
};

function PaperclipIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
    </svg>
  );
}

export default function AnnouncementRow({ ann }) {
  const companyLabel = COMPANY_LABELS[ann.company] || ann.company;

  // Split "Type — Description" into parts if applicable
  const [annType, ...rest] = ann.title.split(" — ");
  const description = rest.join(" — ");

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-sm transition-shadow">
      {/* Top row: date + buttons */}
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs text-gray-400 mb-1">{ann.cardDate}</p>
          <h3 className="font-semibold text-gray-900 text-sm leading-snug">{companyLabel}</h3>
        </div>
        <div className="flex items-center gap-2 shrink-0 mt-0.5">
          {ann.source_url && (
            <a
              href={ann.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium border border-gray-300 rounded text-gray-600 hover:border-teal hover:text-teal transition-colors"
            >
              <PaperclipIcon />
              File Link
            </a>
          )}
        </div>
      </div>

      {/* Announcement type */}
      <p className="mt-2 text-xs font-medium text-teal uppercase tracking-wide">
        {annType}
      </p>

      {/* Description */}
      {description && (
        <p className="mt-1.5 text-sm text-gray-600 leading-relaxed">
          {description}
        </p>
      )}
    </div>
  );
}
