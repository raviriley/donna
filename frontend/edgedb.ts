import { createClient } from "edgedb";
import createAuth from "@edgedb/auth-nextjs/app";

import { getBaseUrl } from "./base-url";

export const client = createClient({
  tlsSecurity: "default",
});

export const auth = createAuth(client, {
  baseUrl: getBaseUrl(),
});
