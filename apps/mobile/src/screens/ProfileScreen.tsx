import { ScrollView, Text } from "react-native";
import { styles } from "./HomeScreen";

export function ProfileScreen() {
  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={styles.title}>Profile</Text>
      <Text style={styles.body}>Privacy, export, deletion, language, and subscription controls match the web portal.</Text>
    </ScrollView>
  );
}
