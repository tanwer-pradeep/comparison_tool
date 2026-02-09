/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    images: {
        domains: ["localhost"],
    },
    eslint: {
        // Warning: This allows production builds to successfully complete even if
        // your project has ESLint errors.
        ignoreDuringBuilds: true,
    },
    typescript: {
        // !! WARN !!
        // Dangerously allow production builds to successfully complete even if
        // your project has type errors.
        ignoreBuildErrors: true,
    },
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8000/api/v1/:path*', // Proxy to Backend
            },
        ]
    },
};

export default nextConfig;
