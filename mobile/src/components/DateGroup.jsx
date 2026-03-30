import { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import AnnouncementCard from "./AnnouncementCard";

export default function DateGroup({ label, items }) {
  const [open, setOpen] = useState(true);

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.header} onPress={() => setOpen((v) => !v)}>
        <Text style={styles.label}>{label}</Text>
        <View style={styles.right}>
          <Text style={styles.count}>
            {items.length} announcement{items.length !== 1 ? "s" : ""}
          </Text>
          <Text style={styles.chevron}>{open ? "▲" : "▼"}</Text>
        </View>
      </TouchableOpacity>

      {open && (
        <View style={styles.cards}>
          {items.map((ann, i) => (
            <AnnouncementCard key={i} ann={ann} />
          ))}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
  },
  header: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#e5e7eb",
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: "#1a1a1a",
  },
  right: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  count: {
    fontSize: 11,
    color: "#9ca3af",
  },
  chevron: {
    fontSize: 10,
    color: "#9ca3af",
  },
  cards: {
    gap: 0,
  },
});
