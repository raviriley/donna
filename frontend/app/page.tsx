import { auth } from "@/edgedb";
import Link from "next/link";
import { EdgeDB_Vercel } from "@/components/Logo";
import { Button } from "@/components/ui/button";

export default async function Home() {
  const session = auth.getSession();

  const signedIn = await session.isSignedIn();

  console.log("signedIn", signedIn);

  return (
    <div>
      <header className="absolute inset-x-0 top-0 z-50">
        <nav
          className="flex items-center justify-between p-6 lg:px-8"
          aria-label="Global"
        >
          <a
            className="contents font-bold"
            href="https://github.com/edgedb/nextjs-edgedb-auth-template"
            target="_blank"
            rel="noopener noreferrer"
          >
            Donna
          </a>
          <div>{signedIn ? "Signed in" : "Signed out"}</div>
          {!signedIn ? (
            <div className="space-x-4">
              {/* <Link
								href={auth.getBuiltinUIUrl()}
								prefetch={false}
								className="text-sm font-semibold leading-6 text-gray-800"
							>
								<button className="ring-2 ring-inset ring-primary bg-primarylight px-4 py-2 rounded-md">
									Sign in
								</button>
							</Link> */}
              <Link
                href={auth.getBuiltinUISignUpUrl()}
                prefetch={false}
                className="text-sm font-semibold leading-6 text-gray-900"
              >
                <Button className="bg-primary px-4 py-2 rounded-md text-white">
                  Sign up
                </Button>
              </Link>
            </div>
          ) : (
            <Link
              href="dashboard"
              className="text-sm font-semibold leading-6 text-gray-900"
            >
              <Button className="bg-primary px-4 py-2 rounded-md text-white">
                Dashboard
              </Button>
            </Link>
          )}
        </nav>
      </header>
    </div>
  );
}
