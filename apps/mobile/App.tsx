import { StatusBar } from "react-native";
import { NavigationContainer, DefaultTheme } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { HomeScreen } from "./src/screens/HomeScreen";
import { DiscoverScreen } from "./src/screens/DiscoverScreen";
import { CoachScreen } from "./src/screens/CoachScreen";
import { GrowthScreen } from "./src/screens/GrowthScreen";
import { ProfileScreen } from "./src/screens/ProfileScreen";

const Tab = createBottomTabNavigator();

const theme = {
  ...DefaultTheme,
  colors: { ...DefaultTheme.colors, background: "#F8FAFC", primary: "#6366F1", card: "#FFFFFF", text: "#0F172A" },
};

export default function App() {
  return (
    <NavigationContainer theme={theme}>
      <StatusBar barStyle="dark-content" />
      <Tab.Navigator screenOptions={{ headerTitleStyle: { fontWeight: "700" } }}>
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Discover" component={DiscoverScreen} />
        <Tab.Screen name="AI Coach" component={CoachScreen} />
        <Tab.Screen name="Growth" component={GrowthScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
