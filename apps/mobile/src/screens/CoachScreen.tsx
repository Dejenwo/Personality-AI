import { ScrollView, Text } from "react-native";
import { styles } from "./HomeScreen";

export function CoachScreen() {
  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={styles.title}>AI Coach</Text>
      <Text style={styles.body}>Educational only. Not a therapist. Crisis: US 988 or iasp.info/suicidalthoughts</Text>
    </ScrollView>
  );
}
