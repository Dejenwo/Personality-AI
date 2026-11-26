import { ScrollView, Text } from "react-native";
import { styles } from "./HomeScreen";

export function DiscoverScreen() {
  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={styles.title}>Discover</Text>
      <Text style={styles.body}>Assessment marketplace: Quick Discovery, IPIP-50 Big Five, and original educational inventories.</Text>
    </ScrollView>
  );
}
