import { createClient } from "edgedb";
import { getBaseUrl } from "./base-url";

const client = createClient();
const baseUrl = getBaseUrl();

const SET_CONFIG = "CONFIGURE CURRENT BRANCH SET";
const RESET_CONFIG = "CONFIGURE CURRENT BRANCH RESET";
const INSERT_CONFIG = "CONFIGURE CURRENT BRANCH INSERT";

const RESET_AUTH_CONFIG = `
${RESET_CONFIG} ext::auth::ProviderConfig;
${RESET_CONFIG} ext::auth::AuthConfig;
${RESET_CONFIG} ext::auth::UIConfig;
${RESET_CONFIG} ext::auth::SMTPConfig;
`;

const SETUP_AUTH_CONFIG = `
${SET_CONFIG} ext::auth::AuthConfig::auth_signing_key := "${process.env.EDGEDB_AUTH_SIGNING_KEY}";
${SET_CONFIG} ext::auth::AuthConfig::app_name := "EdgeDB Next.js Starter";
${SET_CONFIG} ext::auth::AuthConfig::brand_color := "#0000EE";
${SET_CONFIG} ext::auth::AuthConfig::allowed_redirect_urls := {
  "${baseUrl}",
};
`;

const SETUP_UI_CONFIG = `
${INSERT_CONFIG} ext::auth::UIConfig {
  redirect_to := "${new URL("auth/builtin/callback", baseUrl)}",
  redirect_to_on_signup := "${new URL("auth/builtin/callback?isSignUp=true", baseUrl)}",
};
`;

const SETUP_EMAIL_PASSWORD_PROVIDER = `
${INSERT_CONFIG} ext::auth::EmailPasswordProviderConfig {
  require_verification := false,
};
  `;

async function main() {
  await client.execute(`
${RESET_AUTH_CONFIG}
${SETUP_AUTH_CONFIG}
${SETUP_UI_CONFIG}
${SETUP_EMAIL_PASSWORD_PROVIDER}
  `);
  console.log(
    "NOTE: Email password provider is configured, but SMTP is not set up. Please log into your EdgeDB UI and configure SMTP.",
  );
}

await main();
