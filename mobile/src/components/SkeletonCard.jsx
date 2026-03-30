import { View, StyleSheet, Animated, useEffect, useRef } from "react-native";
import { useEffect as useRNEffect, useRef as useRNRef } from "react";

export default function SkeletonCard() {
  const opacity = useRNRef(new Animated.Value(0.4)).current;

  useRNEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, { toValue: 1, duration: 700, useNativeDriver: true }),
        Animated.timing(opacity, { toValue: 0.4, duration: 700, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={[styles.card, { opacity }]}>
      <View style={styles.line1} />
      <View style={styles.line2} />
      <View style={styles.line3} />
    </Animated.View>
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
  },
  line1: { height: 10, backgroundColor: "#f3f4f6", borderRadius: 4, width: "30%", marginBottom: 8 },
  line2: { height: 14, backgroundColor: "#f3f4f6", borderRadius: 4, width: "55%", marginBottom: 10 },
  line3: { height: 10, backgroundColor: "#f3f4f6", borderRadius: 4, width: "90%" },
});
