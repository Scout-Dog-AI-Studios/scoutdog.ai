const nextJest = require("next/jest");

// Provide the path to your Next.js app to load next.config.js and .env files
const createJestConfig = nextJest({ dir: "./" });

// Add any custom config to be passed to Jest
/** @type {import('jest').Config} */
const customJestConfig = {
  testPathIgnorePatterns: ["<rootDir>/e2e/", "/node_modules/"],
  // Add more setup options before each test is run
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],

  // Use jsdom as the test environment
  testEnvironment: "jest-environment-jsdom",

  // Module name mapper for handling module aliases (e.g., @/*)
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },

  // Ignore node_modules, except for specific ones if needed (usually not required with Next.js preset)
  // transformIgnorePatterns: [
  //   '/node_modules/',
  //   '^.+\\.module\\.(css|sass|scss)$',
  // ],

  // Preset for TypeScript Jest execution
  preset: "ts-jest",
};

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(customJestConfig);
