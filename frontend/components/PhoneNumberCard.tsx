import React, { useState } from "react";
import { Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { toast } from "react-toastify";

export default function PhoneNumberCard() {
  const [phoneNumber, setPhoneNumber] = useState("");

  const savePhoneNumber = () => {
    toast.success(`Phone number ${phoneNumber} saved successfully!`);
  };

  return (
    <Card className="flex flex-col">
      <CardHeader>
        <CardTitle>Your Phone Number</CardTitle>
        <CardDescription>Enter the number to forward calls to</CardDescription>
      </CardHeader>
      <CardContent className="flex-grow">
        <div className="flex flex-col space-y-4">
          <Input
            type="tel"
            placeholder="Enter your phone number"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
          />
        </div>
      </CardContent>
      <CardFooter className="mt-auto">
        <Button onClick={savePhoneNumber} className="w-full">
          <Save className="mr-2 h-4 w-4" /> Save Number
        </Button>
      </CardFooter>
    </Card>
  );
}
