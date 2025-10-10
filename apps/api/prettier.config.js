import baseConfig from '@tars/prettier';

/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
const config = {
  ...baseConfig,
  plugins: ['prettier-plugin-packagejson']
};

export default config;