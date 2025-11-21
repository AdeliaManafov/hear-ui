module.exports = {
    root: true,
    env: {
        browser: true,
        node: true,
        es2021: true,
    },
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
    plugins: ['vue', '@typescript-eslint'],
    extends: ['plugin:vue/vue3-recommended', 'plugin:@typescript-eslint/recommended', 'prettier'],
    rules: {
        // project-specific rules can be added here
        'vue/html-indent': ['error', 2],
        '@typescript-eslint/explicit-module-boundary-types': 'off',
    },
}
