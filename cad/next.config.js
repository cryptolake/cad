/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/api/:path*"
            : "/api/",
      },
      {
        source: "/static/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/static/:path*"
            : "/static/",
      },
      {
        source: "/token",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/token"
            : "/token",
      },
    ];
  },
};

module.exports = nextConfig;
