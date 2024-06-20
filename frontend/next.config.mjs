/** @type {import('next').NextConfig} */
const nextConfig = {
    generateBuildId: async () => {
      // You can, for example, get the latest git commit hash here
      return 'my-build-id';
    },
    images: {
        domains: [
            'thumbnail10.coupangcdn.com',
            'thumbnail8.coupangcdn.com',
            'thumbnail9.coupangcdn.com',
            'thumbnail7.coupangcdn.com',
            'thumbnail6.coupangcdn.com',
            'thumbnail5.coupangcdn.com',
            'thumbnail4.coupangcdn.com',
            'thumbnail3.coupangcdn.com',
            'thumbnail2.coupangcdn.com',
            'thumbnail1.coupangcdn.com',
            'images.coupangcdn.com'
        ], 
      },
  };

export default nextConfig;
