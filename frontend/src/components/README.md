# frontend/src/components

Reusable UI components for the frontend application (Chakra UI-based).

Conventions
- Organize each component in its own folder and export it from an `index.tsx` (or `index.ts`) file.
- Use `styles.ts` or `styles.tsx` (optional) for component-specific styling and `types.ts` for explicit prop/type definitions.
- Keep components small, focused, and easy to test. Prefer composition over large monolithic components.

File layout example
- `src/components/MyButton/`
	- `index.tsx` — component entry and named/default exports
	- `styles.ts` — styled-system / Chakra style helpers (optional)
	- `types.ts` — props and small local types (optional)
	- `__tests__/` — unit tests for the component (optional)

Testing and Storybook
- Place unit tests next to components or in `frontend/tests/` depending on the team preference. Use `vitest`/`jest` as configured in the project.
- If Storybook is available in the repository, add stories alongside components (`MyButton.stories.tsx`) to document visual states and help manual QA.

Guidelines
- Export components with clear, typed props and default values where appropriate.
- Avoid coupling components to application-specific hooks or global state; use props and context instead.
- Document public components with short JSDoc comments and, where useful, Storybook stories.

Commands (run from project `frontend` directory)
- Install dependencies: `npm install` (or `pnpm install` / `pnpm i` depending on project setup).
- Start dev server: `npm run dev`.
- Run tests: `npm run test`.
- Run Storybook (if configured): `npm run storybook`.

