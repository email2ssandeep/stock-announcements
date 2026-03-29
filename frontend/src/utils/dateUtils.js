// Convert Screener.in date strings to sortable + displayable format
// Input examples: "2d", "1d", "25 Mar", "18 Mar", "16 Mar 2025"

const MONTHS = {
  jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
  jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
};

export function parseScreenerDate(dateStr) {
  if (!dateStr || dateStr === "N/A") return null;

  const now = new Date();
  const s = dateStr.trim().toLowerCase();

  // "2d" or "1d"
  const daysAgo = s.match(/^(\d+)d$/);
  if (daysAgo) {
    const d = new Date(now);
    d.setDate(d.getDate() - parseInt(daysAgo[1]));
    return d;
  }

  // "3h" hours ago
  const hoursAgo = s.match(/^(\d+)h$/);
  if (hoursAgo) {
    const d = new Date(now);
    d.setHours(d.getHours() - parseInt(hoursAgo[1]));
    return d;
  }

  // "25 Mar" or "25 Mar 2025"
  const parts = s.split(/\s+/);
  if (parts.length >= 2) {
    const day = parseInt(parts[0]);
    const month = MONTHS[parts[1].slice(0, 3)];
    const year = parts[2] ? parseInt(parts[2]) : now.getFullYear();
    if (!isNaN(day) && month !== undefined) {
      return new Date(year, month, day);
    }
  }

  return null;
}

function ordinal(n) {
  const s = ["th", "st", "nd", "rd"];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

export function formatGroupDate(date) {
  if (!date) return "Unknown Date";
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return `${ordinal(date.getDate())} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

export function formatCardDate(date, rawDate) {
  if (!date) return rawDate || "N/A";
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return `${ordinal(date.getDate())} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

export function groupByDate(announcements) {
  const groups = {};

  announcements.forEach((ann) => {
    const key = ann.groupKey || "unknown";
    if (!groups[key]) {
      groups[key] = { label: ann.groupLabel, date: ann.parsedDate, items: [] };
    }
    groups[key].items.push(ann);
  });

  // Sort groups newest-first
  return Object.values(groups).sort((a, b) => {
    if (!a.date) return 1;
    if (!b.date) return -1;
    return b.date - a.date;
  });
}
