import js from '@eslint/js';
import tanstackQueryPlugin from '@tanstack/eslint-plugin-query';
import { defineConfig, globalIgnores } from 'eslint/config';
import eslintConfigPrettier from 'eslint-config-prettier';
import importPlugin from 'eslint-plugin-import';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import react from 'eslint-plugin-react-x';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import globals from 'globals';
import tseslint from 'typescript-eslint';
import turboPlugin from 'eslint-plugin-turbo';
import eslintReact from '@eslint-react/eslint-plugin';

export default defineConfig([
  globalIgnores(['dist']),
  eslintConfigPrettier,
  eslintPluginPrettierRecommended,
  ...tanstackQueryPlugin.configs['flat/recommended'],
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommendedTypeChecked,
      eslintReact.configs['recommended-typescript'],
      reactHooks.configs['recommended-latest'],
      reactRefresh.configs.vite,
      react.configs.recommended,
      jsxA11y.flatConfigs.strict,
      importPlugin.flatConfigs.recommended,
      importPlugin.flatConfigs.typescript,
    ],
    plugins: {
      'simple-import-sort': simpleImportSort,
      turbo: turboPlugin,
    },
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parser: tseslint.parser,
      parserOptions: {
        projectService: true,
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
    ignores: ['vite.config.ts'],
    settings: {
      'import/resolver': {
        alias: {
          map: [['', './public']],
          extensions: ['.js', '.jsx', '.ts', '.tsx'],
        },
        typescript: {
          alwaysTryTypes: true,
          bun: true,
          project: ['./tsconfig.node.json', './tsconfig.app.json', './tsconfig.json'],
        },
      },
    },
    rules: {
      'react-x/no-class-component': 'error',
      '@eslint-react/dom/no-unsafe-target-blank': 'error',
      '@eslint-react/dom/no-missing-button-type': 'error',
      'simple-import-sort/imports': [
        'error',
        {
          groups: [
            // Packages `react` related packages come first.
            ['^react', '^@?\\w'],
            // Peer packages.
            ['^@tars(/.*|$)'],
            // Internal packages.
            ['^(@|components)(/.*|$)'],
            // Side effect imports.
            ['^\\u0000'],
            // Parent imports. Put `..` last.
            ['^\\.\\.(?!/?$)', '^\\.\\./?$'],
            // Other relative imports. Put same-folder imports and `.` last.
            ['^\\./(?=.*/)(?!/?$)', '^\\.(?!/?$)', '^\\./?$'],
            // Style imports.
            ['^.+\\.?(css)$'],
          ],
        },
      ],
      'simple-import-sort/exports': 'error',
      'import/newline-after-import': 'error',
      'import/no-duplicates': 'error',
      'import/first': 'error',
    },
  },
]);
