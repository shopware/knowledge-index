import js from '@eslint/js'
import { FlatCompat } from '@eslint/eslintrc'

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
})

export default [
  {
    ignores: [
      'coverage/**',
      'dist/**',
      'dist-ssr/**',
      'logs/**',
      'node_modules/**',
      'playwright-report/**',
      'test-results/**',
      'cypress/screenshots/**',
      'cypress/videos/**',
      '*.local',
      '*.log',
      '*.tsbuildinfo',
    ],
  },
  ...compat.extends(
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting',
  ),
  {
    languageOptions: {
      ecmaVersion: 'latest',
    },
  },
]
