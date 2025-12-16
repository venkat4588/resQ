import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Disable Strict Mode to avoid double mounting of components in dev,
  // which can cause Leaflet to initialize the map container twice.
  reactStrictMode: false,
};

export default nextConfig;
