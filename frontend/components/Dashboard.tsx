"use client";

import React, { useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AddRuleCard from "@/components/AddRuleCard";
import PhoneNumberCard from "@/components/PhoneNumberCard";
import ExistingRulesCard from "@/components/ExistingRulesCard";
import GeneralPreferenceCard from "@/components/GeneralPreferenceCard";
import EditRuleModal from "@/components/EditRuleModal";

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
		setRules([...rules, { ...newRule, id: Date.now() }]);
		toast.success("New rule added successfully!");
	};

	const deleteRule = (id: number) => {
		setRules(rules.filter((rule) => rule.id !== id));
		toast.info("Rule deleted successfully!");
	};

	const openEditModal = (rule: Rule) => {
		setEditingRule(rule);
		setIsModalOpen(true);
	};

	const saveEditedRule = (editedRule: Rule) => {
		setRules(
			rules.map((rule) => (rule.id === editedRule.id ? editedRule : rule))
		);
		setIsModalOpen(false);
		setEditingRule(null);
		toast.success("Rule updated successfully!");
	};

	return (
		<div className="container mx-auto p-4">
			<h1 className="text-2xl font-bold mb-4">
				AI Call Screener Configuration
			</h1>

			<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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

			<EditRuleModal
				isOpen={isModalOpen}
				onClose={() => setIsModalOpen(false)}
				rule={editingRule}
				onSave={saveEditedRule}
			/>

			<ToastContainer position="bottom-right" />
		</div>
	);
}
