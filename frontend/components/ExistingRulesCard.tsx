import React from "react";
import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Rule } from "./Dashboard";

type ExistingRulesCardProps = {
  rules: Rule[];
  onDeleteRule: (id: number) => void;
  onEditRule: (rule: Rule) => void;
};

export default function ExistingRulesCard({
  rules,
  onDeleteRule,
  onEditRule,
}: ExistingRulesCardProps) {
  return (
    <Card className="md:col-span-2">
      <CardHeader>
        <CardTitle>Existing Rules</CardTitle>
        <CardDescription>
          Manage your current call screening rules
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {rules.map((rule) => (
            <li
              key={rule.id}
              className="flex items-center justify-between p-2 bg-secondary rounded cursor-pointer hover:bg-secondary/80 transition-colors"
              onClick={() => onEditRule(rule)}
            >
              <span>
                {rule.description}
                {rule.isImportant && (
                  <span className="text-primary ml-2">(Important)</span>
                )}
                {rule.expiryDate && (
                  <span className="text-muted-foreground ml-2">
                    (Expires: {rule.expiryDate})
                  </span>
                )}
              </span>
              <Button
                variant="destructive"
                size="icon"
                onClick={(e) => {
                  e.stopPropagation();
                  onDeleteRule(rule.id);
                }}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
