import path from 'node:path'
import {defineConfig} from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    test: {
        environment: 'jsdom',
        globals: true,
        setupFiles: ['./src/test/setup.ts'],
        include: [
            'src/**/*.spec.ts',
            'src/**/*.test.ts',
            'src/**/__tests__/**/*.spec.ts',
            'src/**/__tests__/**/*.test.ts',
        ],
        coverage: {
            provider: 'v8',
            reporter: ['text', 'html', 'lcov'],
            include: ['src/**/*.{ts,vue}'],
            exclude: [
                'src/client/**',
                'src/test/**',
                'src/vite-env.d.ts',
                'src/shims-vue.d.ts',
            ],
        },
        server: {
            deps: {
                inline: ['vuetify'],
            },
        },
    },
})
