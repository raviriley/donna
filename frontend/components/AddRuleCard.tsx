import React, { useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Rule } from "./Dashboard";

type AddRuleCardProps = {
  onAddRule: (rule: Omit<Rule, "id">) => void;
};

export default function AddRuleCard({ onAddRule }: AddRuleCardProps) {
  const [newRule, setNewRule] = useState("");
  const [isNewRuleImportant, setIsNewRuleImportant] = useState(false);
  const [expiryDate, setExpiryDate] = useState("");

  const handleAddRule = () => {
    if (newRule.trim() !== "") {
      onAddRule({
        description: newRule,
        isImportant: isNewRuleImportant,
        expiryDate: expiryDate || null,
      });
      setNewRule("");
      setIsNewRuleImportant(false);
      setExpiryDate("");
    }
  };

  return (
    <Card className="flex flex-col">
      <CardHeader>
        <CardTitle>Add New Rule</CardTitle>
        <CardDescription>Create a new rule for call screening</CardDescription>
      </CardHeader>
      <CardContent className="flex-grow">
        <div className="flex flex-col space-y-4">
          <Input
            type="text"
            placeholder="Enter rule description"
            value={newRule}
            onChange={(e) => setNewRule(e.target.value)}
          />
          <div className="flex items-center space-x-2">
            <Switch
              id="new-rule-important"
              checked={isNewRuleImportant}
              onCheckedChange={setIsNewRuleImportant}
            />
            <Label htmlFor="new-rule-important">Important</Label>
          </div>
          <div className="flex flex-col space-y-2">
            <Label htmlFor="expiry-date">Expiry Date (optional)</Label>
            <Input
              type="date"
              id="expiry-date"
              value={expiryDate}
              onChange={(e) => setExpiryDate(e.target.value)}
            />
          </div>
        </div>
      </CardContent>
      <CardFooter className="mt-auto">
        <Button onClick={handleAddRule} className="w-full">
          <Plus className="mr-2 h-4 w-4" /> Add Rule
        </Button>
      </CardFooter>
    </Card>
  );
}
