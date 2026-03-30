import { View, Text, TouchableOpacity, Linking, StyleSheet } from "react-native";
import { COMPANY_LABELS } from "../config";

export default function AnnouncementCard({ ann }) {
  const companyLabel = COMPANY_LABELS[ann.company] || ann.company;
  const [annType, ...rest] = ann.title.split(" — ");
  const description = rest.join(" — ");

  const openLink = () => {
    if (ann.source_url) Linking.openURL(ann.source_url);
  };

  return (
    <View style={styles.card}>
      {/* Top row */}
      <View style={styles.topRow}>
        <View style={styles.meta}>
          <Text style={styles.date}>{ann.cardDate}</Text>
          <Text style={styles.company}>{companyLabel}</Text>
        </View>
        {ann.source_url && (
          <TouchableOpacity style={styles.fileBtn} onPress={openLink}>
            <Text style={styles.fileBtnText}>📎 File Link</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Announcement type */}
      <Text style={styles.annType}>{annType}</Text>

      {/* Description */}
      {description ? (
        <Text style={styles.description} numberOfLines={3}>
          {description}
        </Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fff",
    borderRadius: 10,
    padding: 16,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: "#e5e7eb",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.04,
    shadowRadius: 2,
    elevation: 1,
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 8,
  },
  meta: {
    flex: 1,
    marginRight: 8,
  },
  date: {
    fontSize: 11,
    color: "#9ca3af",
    marginBottom: 2,
  },
  company: {
    fontSize: 14,
    fontWeight: "600",
    color: "#111827",
  },
  fileBtn: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: "#d1d5db",
  },
  fileBtnText: {
    fontSize: 11,
    color: "#4b5563",
    fontWeight: "500",
  },
  annType: {
    fontSize: 11,
    fontWeight: "600",
    color: "#00b386",
    textTransform: "uppercase",
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  description: {
    fontSize: 13,
    color: "#4b5563",
    lineHeight: 19,
  },
});
