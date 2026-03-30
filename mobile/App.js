import { SafeAreaProvider } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import { View, StyleSheet } from "react-native";
import Header from "./src/components/Header";
import HomeScreen from "./src/screens/HomeScreen";

export default function App() {
  return (
    <SafeAreaProvider>
      <StatusBar style="dark" backgroundColor="#fff" />
      <View style={styles.container}>
        <Header />
        <HomeScreen />
      </View>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f4f6f8",
  },
});
