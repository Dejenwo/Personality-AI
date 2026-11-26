import { AppShell } from "@/components/AppShell";
import { Success } from "@/components/State";

export default function PaySuccess() {
  return (
    <AppShell title="Payment confirmation">
      <Success message="If a live payment provider is connected, this page confirms entitlement restoration. Locally, use the development grant." />
    </AppShell>
  );
}
