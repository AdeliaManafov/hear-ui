# FastAPI Project - Frontend

The frontend is built
with [Vite](https://vitejs.dev/), [React](https://reactjs.org/), [TypeScript](https://www.typescriptlang.org/), [TanStack Query](https://tanstack.com/query), [TanStack Router](https://tanstack.com/router)
and [Chakra UI](https://chakra-ui.com/).

## Frontend development

Before you begin, ensure that you have either the Node Version Manager (nvm) or Fast Node Manager (fnm) installed on
your system.

* To install fnm follow the [official fnm guide](https://github.com/Schniz/fnm#installation). If you prefer nvm, you can
  install it using the [official nvm guide](https://github.com/nvm-sh/nvm#installing-and-updating).

* After installing either nvm or fnm, proceed to the `frontend` directory:

```bash
cd frontend
```

* If the Node.js version specified in the `.nvmrc` file isn't installed on your system, you can install it using the
  appropriate command:

```bash
# If using fnm
fnm install

# If using nvm
nvm install
```

* Once the installation is complete, switch to the installed version:

```bash
# If using fnm
fnm use

# If using nvm
nvm use
```

* Within the `frontend` directory, install the necessary NPM packages:

```bash
npm install
```

* And start the live server with the following `npm` script:

```bash
npm run dev
```

* Then open your browser at http://localhost:5173/.

Notice that this live server is not running inside Docker, it's for local development, and that is the recommended
workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a
production-like environment. But building the image at every change will not be as productive as running the local
development server with live reload.

Check the file `package.json` to see other available options.

### Removing the frontend

If you are developing an API-only app and want to remove the frontend, you can do it easily:

* Remove the `./frontend` directory.

* In the `docker-compose.yml` file, remove the whole service / section `frontend`.

* In the `docker-compose.override.yml` file, remove the whole service / section `frontend` and `playwright`.

Done, you have a frontend-less (api-only) app. 🤓

---

If you want, you can also remove the `FRONTEND` environment variables from:

* `.env`
* `./scripts/*.sh`

But it would be only to clean them up, leaving them won't really have any effect either way.

## Generate Client (MVP note)

The automatic frontend client generation workflow is archived for the MVP to reduce CI noise. Generated client sources
were moved to `archiviert/frontend_react_src/client/`.

If you need to regenerate the client later, restore or copy the original `generate-client` workflow from
`archiviert/.github_workflows/` or run `./scripts/generate-client.sh` locally following the previous instructions.

## Using a Remote API

If you want to use a remote API, you can set the environment variable `VITE_API_URL` to the URL of the remote API. For
example, you can set it in the `frontend/.env` file:

```env
VITE_API_URL=https://api.my-domain.example.com
```

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
