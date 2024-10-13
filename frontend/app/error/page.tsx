export default function Page({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  switch (searchParams.error) {
    case "auth-failed":
      return (
        <div>
          Error: Sometime went wrong when authenticating. Check the console for
          more details.
        </div>
      );
    case "email-verification-required":
      return <div>Error: Email verification required.</div>;
    default:
      return <div>Error</div>;
  }
}
