# HEAR Frontend

> Vue.js 3 frontend for Cochlear Implant success prediction (in development)

For general project information, see the main [README](../README.md).

---

## Overview

The frontend provides a web interface for:
- **Patient management:** View, create, and edit patient records
- **Predictions:** Request ML predictions with visual feedback
- **Explanations:** Display SHAP feature importance charts
- **Feedback:** Submit and view clinical feedback

**Current Status:** ⏳ In Progress (MVP focuses on backend API)

---

## Architecture

```
Frontend (Vue.js 3 + TypeScript)
├── src/
│   ├── components/          # Reusable UI components
│   ├── routes/              # Page components (views)
│   ├── client/              # Auto-generated API client (OpenAPI)
│   ├── hooks/               # Composition API hooks
│   └── App.vue              # Root component
└── public/                  # Static assets
```

---

## Tech Stack

- **Framework:** Vue.js 3 + TypeScript
- **Build Tool:** Vite
- **UI Library:** Vuetify (Vue Material Design Components)
- **State Management:** Pinia (optional, TanStack Query for API state)
- **Testing:** Vitest (unit tests) + Playwright (E2E tests)
- **Code Quality:** ESLint + Biome (linter/formatter)

---

## Setup

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or pnpm
- Node Version Manager (nvm or fnm) recommended

### Quick Start

```bash
cd frontend

# Install Node.js version from .nvmrc (if using nvm/fnm)
fnm install  # or: nvm install
fnm use      # or: nvm use

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser
# http://localhost:5173
```

### Environment Configuration

```bash
# Create .env file
cp .env.example .env
```

**Required variables:**

```env
# API URL (backend endpoint)
VITE_API_URL=http://localhost:8000
```

### Using Remote API

If you want to use a remote backend instead of local:

```env
# In frontend/.env
VITE_API_URL=https://api.your-domain.com
```

---

## Development

### Available Scripts

```bash
# Start dev server with hot-reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e

# Type checking
npm run type-check
```

### Docker Development

```bash
# From project root
cd hear-ui

# Start all services (includes frontend)
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.override.yml \
  --env-file "$PWD/.env" up -d

# View frontend logs
docker compose -f docker/docker-compose.yml logs -f frontend

# Frontend available at: http://localhost:5173
```

### VS Code Integration

Recommended extensions:
- **Vue - Official** (Vue Language Features)
- **ESLint**
- **Prettier**
- **TypeScript Vue Plugin**

---

## Testing

### Unit Tests (Vitest)

```bash
# Run all unit tests
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

### E2E Tests (Playwright)

```bash
# Run E2E tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui

# Run specific test file
npx playwright test tests/example.spec.ts
```

### CI/CD

GitHub Actions workflows:
- `ci.yml` - Combined pipeline (lint → test → e2e)
- `playwright.yml` - E2E API tests (18 tests)

---

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Output: frontend/dist/

# Preview production build locally
npm run preview
# Open: http://localhost:4173
```

### Docker Production Build

```bash
# From project root
docker compose -f docker/docker-compose.yml build frontend

# Frontend served via nginx (production mode)
```

---

## API Client Generation

The frontend uses an auto-generated TypeScript client based on the backend's OpenAPI spec.

**Note:** Client generation is currently archived for MVP. Pre-generated client is in `src/client/`.

To regenerate the client:

```bash
# From project root
./scripts/generate-client.sh

# Or manually
cd frontend
npm run generate-client
```

**Configuration:** See `openapi-ts.config.ts`

---

## Contributing

### Code Standards

- **Style:** Use ESLint + Biome for linting/formatting
- **TypeScript:** Strict mode enabled
- **Components:** Single-file components (.vue), use `<script setup>` syntax
- **Tests:** Write unit tests for components, E2E tests for user flows

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and add tests
3. Run linter: `npm run lint`
4. Run tests: `npm run test`
5. Commit: `git commit -m "feat: add feature"`
6. Push and open PR

### Component Guidelines

```vue
<script setup lang="ts">
// Use Composition API with <script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>

<template>
  <div>{{ count }} × 2 = {{ doubled }}</div>
</template>

<style scoped>
/* Scoped styles preferred */
</style>
```

---

## Removing the Frontend

If you're building an API-only app, you can remove the frontend:

1. Delete `./frontend` directory
2. Remove `frontend` service from `docker/docker-compose.yml`
3. Remove `frontend` and `playwright` services from `docker/docker-compose.override.yml`
4. Remove `FRONTEND` environment variables from `.env` and scripts

---

## License

MIT License - see [LICENSE](../LICENSE)

---

## Further Documentation

- [Main README](../README.md) - Complete project documentation
- [i18n Guide](frontend-i18n.md) - Internationalization setup
- [Project Documentation](../docs/Projektdokumentation.md) - Full technical docs (German)
- [Vite Documentation](https://vitejs.dev/) - Build tool
- [Vue.js Documentation](https://vuejs.org/) - Framework
- [Vuetify Documentation](https://vuetifyjs.com/) - UI library


Then, when you run the frontend, it will use that URL as the base URL for the API.

## Code Structure

The frontend code is structured as follows:

* `frontend/src` - The main frontend code.
* `frontend/src/assets` - Static assets.
* `frontend/src/client` - The generated OpenAPI client.
* `frontend/src/components` - The different components of the frontend.
* `frontend/src/hooks` - Custom hooks.
* `frontend/src/routes` - The different routes of the frontend which include the pages.
* `theme.tsx` - The Chakra UI custom theme.

## End-to-End Testing with Playwright (MVP note)

Playwright E2E tests and the CI job that ran them have been archived for the MVP and moved to `archiviert/`. The active
CI workflow was replaced with a noop to reduce CI runtime. If you want to re-enable E2E testing, restore the Playwright
workflow from `archiviert/.github_workflows/playwright.yml` and the tests in `archiviert/frontend_tests_react/`.

Local Playwright runs and instructions are unchanged and remain available in this document history if you need to run
them again.
