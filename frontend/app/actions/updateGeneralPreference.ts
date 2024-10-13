"use server";

import { createClient } from "edgedb";

export async function updateGeneralPreference(preference: boolean) {
  const client = createClient();

  try {
    // Assuming you have a User type with a generalPreference field
    // and that the current user's ID is available (you might need to adjust this)
    const result = await client.query(
      `
      update User 
      filter .id = <uuid>$currentUserId
      set {
        generalPreference := <bool>$preference
      }
    `,
      {
        preference,
        currentUserId: "current-user-id-here", // You'll need to replace this with the actual user ID
      },
    );

    return { success: true };
  } catch (error) {
    console.error("Error updating general preference:", error);
    return { success: false, error: "Failed to update preference" };
  }
}
