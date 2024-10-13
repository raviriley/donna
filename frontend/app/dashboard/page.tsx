import { auth } from "@/edgedb";
import Dashboard from "@/components/Dashboard";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
	const session = auth.getSession();
	const signedIn = await session.isSignedIn();

	if (!signedIn) {
		redirect("/");
	}

	return <Dashboard />;
}
