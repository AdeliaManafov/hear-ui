# frontend/src/routes

Page definitions and routing configuration (TanStack Router).

Overview
- This directory contains the application's route definitions, top-level layout routes, and wrappers for protected (authenticated) routes.

Structure
- Top-level route definitions and nested routes.
- Layout components that wrap sets of pages (for example, `AppLayout`, `AuthLayout`).
- Protected routes: use an authentication wrapper or route guard component (for example, `RequireAuth`) to restrict pages to logged-in users.

Where pages live
- Pages and route modules typically live in `src/routes/` or in a `pages/` subfolder. Each page should export a route entry that can be composed into the route tree.

Notes
- If API paths or shapes change in the backend, regenerate the frontend OpenAPI client and update route-level data loaders or hooks that call the API.
- Follow the project's patterns for route registration: keep routes declarative and small, and centralize any route-tree composition logic.

