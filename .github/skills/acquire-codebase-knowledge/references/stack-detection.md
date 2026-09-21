# Stack detection reference

Load this file when the stack is ambiguous, for example, when there are multiple manifest files, unfamiliar file extensions, or no obvious `package.json` or `go.mod`.

---

## Manifest file to ecosystem

| File | Ecosystem | Key fields to read |
|------|-----------|--------------------|
| `package.json` | Node.js / JavaScript / TypeScript | `dependencies`, `devDependencies`, `scripts`, `main`, `type`, `engines` |
| `go.mod` | Go | Module path, Go version, and `require` block |
| `requirements.txt` | Python (pip) | List of packages with pinned versions |
| `Pipfile` | Python (pipenv) | `[packages]`, `[dev-packages]`, and Python version in `[requires]` |
| `pyproject.toml` | Python (poetry / uv / hatch) | `[tool.poetry.dependencies]`, `[project]`, `[build-system]` |
| `setup.py` / `setup.cfg` | Python (setuptools, legacy) | `install_requires`, `python_requires` |
| `Cargo.toml` | Rust | `[dependencies]`, `[[bin]]`, `[lib]` |
| `pom.xml` | Java / Kotlin (Maven) | `<dependencies>`, `<artifactId>`, `<groupId>`, `<java.version>` |
| `build.gradle` / `build.gradle.kts` | Java / Kotlin (Gradle) | `dependencies {}`, `sourceCompatibility` |
| `composer.json` | PHP | `require`, `require-dev` |
| `Gemfile` | Ruby | `gem` declarations and `ruby` version constraint |
| `mix.exs` | Elixir | `deps/0`, `elixir: "~> X.Y"` |
| `pubspec.yaml` | Dart / Flutter | `dependencies`, `dev_dependencies`, `environment.sdk` |
| `*.csproj` | .NET / C# | `<PackageReference>`, `<TargetFramework>` |
| `*.sln` | .NET solution | References multiple `.csproj` projects |
| `deno.json` / `deno.jsonc` | Deno (TypeScript runtime) | `imports`, `tasks` |
| `bun.lockb` | Bun (JavaScript runtime) | Binary lockfile; check dependencies in `package.json` |

---

## Language runtime version detection

| Language | Where to find the version |
|----------|--------------------------|
| Node.js | `.nvmrc`, `.node-version`, `engines.node` in `package.json`, and Docker `FROM node:X` |
| Python | `.python-version`, `pyproject.toml [requires-python]`, Docker `FROM python:X` |
| Go | First line of `go.mod` (`go 1.21`) |
| Java | `<java.version>` in `pom.xml`, `sourceCompatibility` in `build.gradle`, and Docker `FROM eclipse-temurin:X` |
| Ruby | `.ruby-version`, `Gemfile` `ruby 'X.Y.Z'` |
| Rust | `rust-toolchain.toml` or `rust-toolchain` file |
| .NET | `<TargetFramework>` in `.csproj` (for example, `net8.0`) |

---

## Framework detection (Node.js/TypeScript)

| Dependency in `package.json` | Framework |
|-----------------------------|-----------|
| `express` | Express.js (minimal HTTP server) |
| `fastify` | Fastify (high-performance HTTP server) |
| `next` | Next.js (React SSR/SSG; check the `pages/` or `app/` directories) |
| `nuxt` | Nuxt.js (SSR/SSG Vue) |
| `@nestjs/core` | NestJS (opinionated Node.js framework with DI) |
| `koa` | Koa (middleware-focused, no built-in router) |
| `@hapi/hapi` | Hapi |
| `@trpc/server` | tRPC (type-safe API without REST/GraphQL schemas) |
| `routing-controllers` | routing-controllers (decorator-based Express wrapper) |
| `typeorm` | TypeORM (SQL ORM with decorators) |
| `prisma` | Prisma (type-safe ORM; check `prisma/schema.prisma`) |
| `mongoose` | Mongoose (MongoDB ODM) |
| `sequelize` | Sequelize (SQL ORM) |
| `drizzle-orm` | Drizzle (lightweight SQL ORM) |
| `react` without `next` | Plain React SPA (check `react-router-dom`) |
| `vue` without `nuxt` | Plain Vue SPA |

---

## Framework detection (Python)

| Package | Framework |
|---------|-----------|
| `fastapi` | FastAPI (async REST and automatic OpenAPI documentation) |
| `flask` | Flask (minimal WSGI web framework) |
| `django` | Django (batteries included; check `settings.py`) |
| `starlette` | Starlette (ASGI, often used as the basis of FastAPI) |
| `aiohttp` | aiohttp (async HTTP client and server) |
| `sqlalchemy` | SQLAlchemy (SQL ORM; check `alembic` migrations) |
| `alembic` | Alembic (SQLAlchemy migration tool) |
| `pydantic` | Pydantic (data validation; core FastAPI component) |
| `celery` | Celery (distributed task queue) |

---

## Monorepo detection

Check these signals in order. A monorepo combines several projects in one repository:

1. `pnpm-workspace.yaml`: pnpm workspaces
2. `lerna.json`: Lerna monorepo
3. `nx.json`: Nx monorepo (also check `workspace.json`)
4. `turbo.json`: Turborepo
5. `rush.json`: Rush (Microsoft's monorepo manager)
6. `moon.yml`: Moon
7. `package.json` with `"workspaces": [...]`: npm/yarn workspaces
8. Presence of `packages/`, `apps/`, `libs/`, or `services/` directories with their own `package.json` files

If a monorepo is detected, each workspace may have **independent** dependencies and conventions. Map each subpackage separately in `STACK.md` and record the monorepo structure in `STRUCTURE.md`.

---

## TypeScript path alias detection

If `tsconfig.json` has a `paths` key, imports with non-relative prefixes are aliases. Map them before documenting the structure.

```json
// Example tsconfig.json
"paths": {
  "@/*": ["./src/*"],
  "@components/*": ["./src/components/*"],
  "@utils/*": ["./src/utils/*"]
}
```

Imports such as `import { foo } from '@/utils/bar'` resolve to `src/utils/bar`. Document as `src/utils/bar`, not `@/utils/bar`.

---

## Docker base image to runtime

If no manifest file is present but a `Dockerfile` exists, the `FROM` line reveals the runtime:

| FROM line pattern | Runtime |
|------------------|---------|
| `FROM node:X` | Node.js X |
| `FROM python:X` | Python X |
| `FROM golang:X` | Go X |
| `FROM eclipse-temurin:X` | Java X (Eclipse Temurin JDK) |
| `FROM mcr.microsoft.com/dotnet/aspnet:X` | .NET X |
| `FROM ruby:X` | Ruby X |
| `FROM rust:X` | Rust X |
| `FROM alpine` (standalone) | Check what was installed through `RUN apk add` |
