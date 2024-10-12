import React from "react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";

type GeneralPreferenceCardProps = {
	preference: boolean;
	onPreferenceChange: (value: boolean) => void;
};

export default function GeneralPreferenceCard({
	preference,
	onPreferenceChange,
}: GeneralPreferenceCardProps) {
	return (
		<Card className="md:col-span-2">
			<CardHeader>
				<CardTitle>General Preference</CardTitle>
				<CardDescription>
					Set your default call handling preference
				</CardDescription>
			</CardHeader>
			<CardContent>
				<div className="flex items-center space-x-2">
					<Switch
						id="general-preference"
						checked={preference}
						onCheckedChange={onPreferenceChange}
					/>
					<Label htmlFor="general-preference">
						Allow all calls by default (turn off to screen all calls unless a
						rule matches)
					</Label>
				</div>
			</CardContent>
		</Card>
	);
}
