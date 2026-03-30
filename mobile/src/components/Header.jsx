import { View, Text, StyleSheet } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function Header() {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.container, { paddingTop: insets.top + 10 }]}>
      <View style={styles.logo}>
        <View style={styles.logoIcon}>
          <Text style={styles.logoText}>SA</Text>
        </View>
        <Text style={styles.logoLabel}>StockAlerts</Text>
      </View>
      <Text style={styles.subtitle}>Infosys · HCL · Reliance · TCS</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#fff",
    paddingHorizontal: 16,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#e5e7eb",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  logo: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  logoIcon: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: "#00b386",
    alignItems: "center",
    justifyContent: "center",
  },
  logoText: {
    color: "#fff",
    fontWeight: "700",
    fontSize: 11,
  },
  logoLabel: {
    fontWeight: "700",
    fontSize: 16,
    color: "#1a1a1a",
  },
  subtitle: {
    fontSize: 11,
    color: "#9ca3af",
  },
});
