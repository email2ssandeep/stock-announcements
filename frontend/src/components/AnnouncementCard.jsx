export default function AnnouncementCard({ date, title, sourceUrl }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      <p className="text-xs font-semibold text-brand-accent uppercase tracking-wide mb-1">
        {date || "N/A"}
      </p>
      <p className="text-sm text-gray-700 leading-snug">
        {sourceUrl ? (
          <a
            href={sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-brand-accent hover:underline"
          >
            {title}
          </a>
        ) : (
          title
        )}
      </p>
    </div>
  );
}
