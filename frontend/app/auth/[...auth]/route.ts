import { redirect } from "next/navigation";
import { auth } from "@/edgedb";

export const { GET, POST } = auth.createAuthRouteHandlers({
  async onBuiltinUICallback({ error, tokenData, isSignUp }) {
    if (error) {
      console.error("Authentication failed: ", error);
      redirect("/error?error=auth-failed");
    }

    if (!tokenData) {
      console.error("Email verification required.");
      redirect("/error?error=email-verification-required");
    }

    if (isSignUp) {
      const client = auth.getSession().client;

      const emailData = await client.querySingle<{ email: string }>(`
        SELECT ext::auth::EmailFactor {
          email
        } FILTER .identity = (global ext::auth::ClientTokenIdentity)
      `);

      await client.query(`
        INSERT User {
          name := '',
          email := '${emailData?.email}',
          userRole := 'user',
          identity := (global ext::auth::ClientTokenIdentity)
        }
      `);
    }
    redirect("/");
  },
  onSignout() {
    redirect("/");
  },
});
