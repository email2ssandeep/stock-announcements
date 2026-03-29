import { useState } from "react";
import AnnouncementRow from "./AnnouncementRow";

function ChevronIcon({ up }) {
  return (
    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d={up ? "M5 15l7-7 7 7" : "M19 9l-7 7-7-7"} />
    </svg>
  );
}

export default function DateGroup({ label, items }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="mb-4">
      {/* Date header */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between bg-white border border-gray-200 rounded-lg px-5 py-3 hover:bg-gray-50 transition-colors"
      >
        <span className="font-semibold text-gray-800 text-sm">{label}</span>
        <div className="flex items-center gap-1">
          <span className="text-xs text-gray-400 mr-2">{items.length} announcement{items.length !== 1 ? "s" : ""}</span>
          <ChevronIcon up={open} />
          <ChevronIcon up={!open} />
        </div>
      </button>

      {/* Cards */}
      {open && (
        <div className="mt-2 space-y-2 pl-0">
          {items.map((ann, i) => (
            <AnnouncementRow key={i} ann={ann} />
          ))}
        </div>
      )}
    </div>
  );
}
