"use client"; // This component must be a Client Component

import { Auth0Provider } from "@auth0/auth0-react";
import React from "react";

interface ProvidersProps {
  children: React.ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  console.log("[Providers] Rendering. Env:", {
    domain: process.env.NEXT_PUBLIC_AUTH0_DOMAIN,
    clientId: process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID,
    audience: process.env.NEXT_PUBLIC_AUTH0_AUDIENCE,
  });
  const domain = process.env.NEXT_PUBLIC_AUTH0_DOMAIN;
  const clientId = process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID;
  const audience = process.env.NEXT_PUBLIC_AUTH0_AUDIENCE; // Get audience

  if (!domain || !clientId) {
    // Optionally render a message or throw an error if config is missing
    return <>{children}</>;
  }

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        // Use the audience from environment variables for API access
        audience: audience,
        // Specify the redirect URI, ensuring it matches Auth0 config
        redirect_uri:
          typeof window !== "undefined" ? window.location.origin : undefined,
      }}
    >
      {children}
    </Auth0Provider>
  );
}
