import { ScrollView, Text, StyleSheet } from "react-native";

export function HomeScreen() {
  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={styles.kicker}>PersonalityDNA AI</Text>
      <Text style={styles.title}>Your pattern, not a prison.</Text>
      <Text style={styles.body}>
        Complete the Big Five on the web or in a later native assessment flow. This Expo shell uses the same five-tab
        information architecture as the web app.
      </Text>
    </ScrollView>
  );
}

export const styles = StyleSheet.create({
  wrap: { padding: 24, gap: 12 },
  kicker: { color: "#14B8A6", letterSpacing: 2, textTransform: "uppercase", fontSize: 12 },
  title: { fontSize: 32, fontWeight: "700", color: "#101828" },
  body: { fontSize: 16, color: "#475569", lineHeight: 24 },
});
