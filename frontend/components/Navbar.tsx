import React from "react";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

export default function Navbar() {
	const handleLogout = () => {
		// Implement logout logic here
		console.log("Logout clicked");
	};

	return (
		<nav className="bg-primary text-primary-foreground py-4 px-6 flex justify-between items-center sticky top-0 z-10">
			<div className="text-lg font-semibold">AI Call Screener</div>
			<Button variant="secondary" onClick={handleLogout}>
				<LogOut className="mr-2 h-4 w-4" /> Log out
			</Button>
		</nav>
	);
}
