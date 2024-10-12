import React, { useState, useEffect } from "react";
import { X, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
	DialogFooter,
} from "@/components/ui/dialog";
import { Rule } from "./Dashboard";

type EditRuleModalProps = {
	isOpen: boolean;
	onClose: () => void;
	rule: Rule | null;
	onSave: (rule: Rule) => void;
};

export default function EditRuleModal({
	isOpen,
	onClose,
	rule,
	onSave,
}: EditRuleModalProps) {
	const [editedRule, setEditedRule] = useState<Rule | null>(null);

	useEffect(() => {
		setEditedRule(rule);
	}, [rule]);

	if (!editedRule) return null;

	return (
		<Dialog open={isOpen} onOpenChange={onClose}>
			<DialogContent>
				<DialogHeader>
					<DialogTitle>Edit Rule</DialogTitle>
				</DialogHeader>
				<Textarea
					value={editedRule.description}
					onChange={(e) =>
						setEditedRule({ ...editedRule, description: e.target.value })
					}
					rows={4}
				/>
				<div className="flex items-center space-x-2 mt-4">
					<Switch
						id="edit-rule-important"
						checked={editedRule.isImportant}
						onCheckedChange={(checked) =>
							setEditedRule({ ...editedRule, isImportant: checked })
						}
					/>
					<Label htmlFor="edit-rule-important">Important</Label>
				</div>
				<div className="flex flex-col space-y-2 mt-4">
					<Label htmlFor="edit-expiry-date">Expiry Date (optional)</Label>
					<Input
						type="date"
						id="edit-expiry-date"
						value={editedRule.expiryDate || ""}
						onChange={(e) =>
							setEditedRule({
								...editedRule,
								expiryDate: e.target.value || null,
							})
						}
					/>
				</div>
				<DialogFooter>
					<Button variant="outline" onClick={onClose}>
						<X className="mr-2 h-4 w-4" /> Cancel
					</Button>
					<Button onClick={() => onSave(editedRule)}>
						<Save className="mr-2 h-4 w-4" /> Save Changes
					</Button>
				</DialogFooter>
			</DialogContent>
		</Dialog>
	);
}
