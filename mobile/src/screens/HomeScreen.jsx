import { useState, useEffect, useMemo, useCallback } from "react";
import {
  View, Text, FlatList, RefreshControl,
  StyleSheet, TouchableOpacity,
} from "react-native";
import { ENDPOINTS, TICKER_MAP, COMPANIES } from "../config";
import { flattenAndEnrich, groupByDate } from "../utils/dateUtils";
import DateGroup from "../components/DateGroup";
import FilterBar from "../components/FilterBar";
import SkeletonCard from "../components/SkeletonCard";

export default function HomeScreen() {
  const [apiData, setApiData] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState("All");

  const fetchData = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    setError(false);
    try {
      const res = await fetch(ENDPOINTS.announcements);
      if (!res.ok) throw new Error("API error");
      const json = await res.json();
      setApiData(json);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const allAnnouncements = useMemo(
    () => flattenAndEnrich(apiData, TICKER_MAP),
    [apiData]
  );

  const filtered = useMemo(() => {
    if (selectedCompany === "All") return allAnnouncements;
    const key = Object.entries(TICKER_MAP).find(([, v]) => v === selectedCompany)?.[0];
    return allAnnouncements.filter((a) => a.company === key);
  }, [allAnnouncements, selectedCompany]);

  const groups = useMemo(() => groupByDate(filtered), [filtered]);

  const renderGroup = ({ item }) => (
    <DateGroup label={item.label} items={item.items} />
  );

  const ListHeader = (
    <View>
      <FilterBar
        selected={selectedCompany}
        onSelect={setSelectedCompany}
        total={filtered.length}
      />
      <View style={styles.titleRow}>
        <Text style={styles.title}>Announcement Alerts</Text>
        <Text style={styles.subtitle}>Sourced from Screener.in · refreshes every 30 min</Text>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.skeletonContainer}>
        <FilterBar selected="All" onSelect={() => {}} total={0} />
        <View style={styles.content}>
          {[1, 2, 3].map((i) => <SkeletonCard key={i} />)}
        </View>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorTitle}>Could not load announcements</Text>
        <Text style={styles.errorSub}>Check your connection and try again.</Text>
        <TouchableOpacity style={styles.retryBtn} onPress={() => fetchData()}>
          <Text style={styles.retryText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <FlatList
      style={styles.list}
      data={groups}
      keyExtractor={(item) => item.label}
      renderItem={renderGroup}
      ListHeaderComponent={ListHeader}
      ListEmptyComponent={
        <View style={styles.centered}>
          <Text style={styles.emptyText}>No announcements found.</Text>
        </View>
      }
      contentContainerStyle={styles.content}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={() => fetchData(true)}
          tintColor="#00b386"
          colors={["#00b386"]}
        />
      }
    />
  );
}

const styles = StyleSheet.create({
  list: {
    flex: 1,
    backgroundColor: "#f4f6f8",
  },
  content: {
    padding: 16,
    paddingTop: 0,
  },
  titleRow: {
    paddingVertical: 14,
  },
  title: {
    fontSize: 18,
    fontWeight: "700",
    color: "#1a1a1a",
    marginBottom: 2,
  },
  subtitle: {
    fontSize: 11,
    color: "#9ca3af",
  },
  skeletonContainer: {
    flex: 1,
    backgroundColor: "#f4f6f8",
  },
  centered: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 32,
    marginTop: 80,
  },
  errorTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#dc2626",
    marginBottom: 6,
  },
  errorSub: {
    fontSize: 13,
    color: "#6b7280",
    textAlign: "center",
    marginBottom: 20,
  },
  retryBtn: {
    backgroundColor: "#00b386",
    paddingHorizontal: 28,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 14,
  },
  emptyText: {
    fontSize: 14,
    color: "#9ca3af",
  },
});
