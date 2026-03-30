const MONTHS = {
  jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
  jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
};

export function parseScreenerDate(dateStr) {
  if (!dateStr || dateStr === "N/A") return null;
  const now = new Date();
  const s = dateStr.trim().toLowerCase();

  const daysAgo = s.match(/^(\d+)d$/);
  if (daysAgo) {
    const d = new Date(now);
    d.setDate(d.getDate() - parseInt(daysAgo[1]));
    return d;
  }

  const hoursAgo = s.match(/^(\d+)h$/);
  if (hoursAgo) {
    const d = new Date(now);
    d.setHours(d.getHours() - parseInt(hoursAgo[1]));
    return d;
  }

  const parts = s.split(/\s+/);
  if (parts.length >= 2) {
    const day = parseInt(parts[0]);
    const month = MONTHS[parts[1].slice(0, 3)];
    const year = parts[2] ? parseInt(parts[2]) : now.getFullYear();
    if (!isNaN(day) && month !== undefined) return new Date(year, month, day);
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
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  return `${ordinal(date.getDate())} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

export function formatCardDate(date, raw) {
  if (!date) return raw || "N/A";
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  return `${ordinal(date.getDate())} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

export function groupByDate(items) {
  const groups = {};
  items.forEach((ann) => {
    const key = ann.groupKey || "unknown";
    if (!groups[key]) groups[key] = { label: ann.groupLabel, date: ann.parsedDate, items: [] };
    groups[key].items.push(ann);
  });
  return Object.values(groups).sort((a, b) => {
    if (!a.date) return 1;
    if (!b.date) return -1;
    return b.date - a.date;
  });
}

export function flattenAndEnrich(apiData, tickerMap) {
  const flat = [];
  Object.entries(apiData).forEach(([ticker, items]) => {
    items.forEach((item) => {
      const parsedDate = parseScreenerDate(item.date);
      flat.push({
        ...item,
        company: ticker,
        companyLabel: tickerMap[ticker] || ticker,
        parsedDate,
        groupKey: parsedDate ? parsedDate.toDateString() : "unknown",
        groupLabel: formatGroupDate(parsedDate),
        cardDate: formatCardDate(parsedDate, item.date),
      });
    });
  });
  return flat.sort((a, b) => {
    if (!a.parsedDate) return 1;
    if (!b.parsedDate) return -1;
    return b.parsedDate - a.parsedDate;
  });
}
