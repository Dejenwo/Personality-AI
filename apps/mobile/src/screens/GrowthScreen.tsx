import { ScrollView, Text } from "react-native";
import { styles } from "./HomeScreen";

export function GrowthScreen() {
  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={styles.title}>Growth</Text>
      <Text style={styles.body}>Programs, habits, goals, and a private journal. No shame-based streaks.</Text>
    </ScrollView>
  );
}
