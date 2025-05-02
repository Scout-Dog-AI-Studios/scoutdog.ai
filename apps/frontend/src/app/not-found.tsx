import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6 text-center">
      <h1 className="text-5xl font-extrabold mb-4">404</h1>
      <p className="text-xl text-gray-600 mb-6">Oops! Page not found.</p>
      <Link
        href="/"
        className="text-scoutdog-blue hover:text-scoutdog-blue/80 font-medium underline"
      >
        Return to Home
      </Link>
    </div>
  );
} 