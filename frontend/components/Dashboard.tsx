"use client";

import React, { useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AddRuleCard from "./AddRuleCard";
import PhoneNumberCard from "./PhoneNumberCard";
import ExistingRulesCard from "./ExistingRulesCard";
import GeneralPreferenceCard from "./GeneralPreferenceCard";
import EditRuleModal from "./EditRuleModal";
import Navbar from "./Navbar";

export type Rule = {
	id: number;
	description: string;
	isImportant: boolean;
	expiryDate: string | null;
};

export default function Dashboard() {
	const [rules, setRules] = useState<Rule[]>([
		{
			id: 1,
			description: "Important call from family",
			isImportant: true,
			expiryDate: null,
		},
		{
			id: 2,
			description: "Work emergency",
			isImportant: true,
			expiryDate: null,
		},
	]);
	const [generalPreference, setGeneralPreference] = useState(false);
	const [editingRule, setEditingRule] = useState<Rule | null>(null);
	const [isModalOpen, setIsModalOpen] = useState(false);

	const addRule = (newRule: Omit<Rule, "id">) => {
		setRules((prevRules) => [...prevRules, { ...newRule, id: Date.now() }]);
		toast.success("New rule added successfully!");
	};

	const deleteRule = (id: number) => {
		setRules((prevRules) => prevRules.filter((rule) => rule.id !== id));
		toast.info("Rule deleted successfully!");
	};

	const openEditModal = (rule: Rule) => {
		setEditingRule(rule);
		setIsModalOpen(true);
	};

	const saveEditedRule = (editedRule: Rule) => {
		setRules((prevRules) =>
			prevRules.map((rule) => (rule.id === editedRule.id ? editedRule : rule))
		);
		setIsModalOpen(false);
		setEditingRule(null);
		toast.success("Rule updated successfully!");
	};

	return (
		<div className="min-h-screen flex flex-col">
			<Navbar />
			<div className="flex-grow container mx-auto p-6 space-y-6 pb-12">
				<h1 className="text-2xl font-bold mb-6">
					AI Call Screener Configuration
				</h1>

				{/* <Button onClick={testFunction}>Test</Button> */}
				<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
					<AddRuleCard onAddRule={addRule} />
					<PhoneNumberCard />
					<ExistingRulesCard
						rules={rules}
						onDeleteRule={deleteRule}
						onEditRule={openEditModal}
					/>
					<GeneralPreferenceCard
						preference={generalPreference}
						onPreferenceChange={setGeneralPreference}
					/>
				</div>

				{editingRule && (
					<EditRuleModal
						isOpen={isModalOpen}
						onClose={() => setIsModalOpen(false)}
						rule={editingRule}
						onSave={saveEditedRule}
					/>
				)}

				<ToastContainer position="bottom-right" />
			</div>
		</div>
	);
}
