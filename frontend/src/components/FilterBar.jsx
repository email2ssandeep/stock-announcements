const COMPANIES = ["All", "Infosys", "HCL", "Reliance", "TCS"];

export default function FilterBar({ selected, onSelect, total }) {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-4 flex-wrap">
        {/* Company filter chips */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-gray-500 font-medium mr-1">Filter:</span>
          {COMPANIES.map((c) => (
            <button
              key={c}
              onClick={() => onSelect(c)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                selected === c
                  ? "bg-teal text-white border-teal"
                  : "bg-white text-gray-600 border-gray-300 hover:border-teal hover:text-teal"
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        {/* Count */}
        <span className="text-xs text-gray-400">{total} announcement{total !== 1 ? "s" : ""}</span>
      </div>
    </div>
  );
}
