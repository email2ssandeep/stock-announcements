import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from "react-native";
import { COMPANIES } from "../config";

export default function FilterBar({ selected, onSelect, total }) {
  return (
    <View style={styles.wrapper}>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.row}
      >
        <Text style={styles.label}>Filter:</Text>
        {COMPANIES.map((c) => (
          <TouchableOpacity
            key={c}
            onPress={() => onSelect(c)}
            style={[styles.chip, selected === c && styles.chipActive]}
          >
            <Text style={[styles.chipText, selected === c && styles.chipTextActive]}>
              {c}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
      <Text style={styles.count}>{total} result{total !== 1 ? "s" : ""}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    backgroundColor: "#fff",
    borderBottomWidth: 1,
    borderBottomColor: "#e5e7eb",
    paddingVertical: 10,
  },
  row: {
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  label: {
    fontSize: 12,
    color: "#6b7280",
    fontWeight: "500",
    marginRight: 4,
  },
  chip: {
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "#d1d5db",
    backgroundColor: "#fff",
  },
  chipActive: {
    backgroundColor: "#00b386",
    borderColor: "#00b386",
  },
  chipText: {
    fontSize: 12,
    fontWeight: "500",
    color: "#4b5563",
  },
  chipTextActive: {
    color: "#fff",
  },
  count: {
    fontSize: 11,
    color: "#9ca3af",
    textAlign: "right",
    paddingHorizontal: 16,
    marginTop: 6,
  },
});
