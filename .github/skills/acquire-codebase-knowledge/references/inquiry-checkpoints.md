# Investigation checkpoints

Investigation questions per template for Phase 2 of the codebase knowledge acquisition workflow. In each template area, look for answers in the scan output first. Then read source files to fill the gaps.

---

## 1. STACK.md: technology stack

- What is the primary language and its exact version? (check `.nvmrc`, `go.mod`, `pyproject.toml`, and the Docker `FROM` line)
- Which package manager is used? (`npm`, `yarn`, `pnpm`, `go mod`, `pip`, `uv`)
- What are the main runtime frameworks? (web server, ORM, and DI container)
- What do `dependencies` (production) and `devDependencies` (development tools) contain?
- Is there a Docker image? Which base image does it use?
- What are the main scripts in `package.json`, `Makefile`, or `pyproject.toml`?

## 2. STRUCTURE.md: directory structure

- Where is the source code? (usually in `src/`, `lib/`, or the project root for Go)
- What are the entry points? (check `main` in `package.json`, `scripts.start`, `cmd/main.go`, and `app.py`)
- What is the stated purpose of each top-level directory?
- Are there less obvious directories (for example, `eng/`, `platform/`, or `infra/`)?
- Are there hidden configuration directories (`.github/`, `.vscode/`, `.husky/`)?
- What naming conventions do directories follow? (camelCase, kebab-case, domain-based versus layer-based organization)

## 3. ARCHITECTURE.md: patterns

- Is code organized by layer (controllers -> services -> repositories) or by feature?
- What is the main data flow? Trace a request or command from entry to data storage.
- Are there singletons, dependency injection patterns, or explicit startup order requirements?
- Are there background workers, queues, or event-driven components?
- Which design patterns appear repeatedly? (Factory, Repository, Decorator, and Strategy)

## 4. CONVENTIONS.md: code patterns

- What is the file naming convention? (check ten or more files: camelCase, kebab-case, or PascalCase)
- What is the function and variable naming convention?
- Are private methods and fields prefixed (for example, `_methodName` or `#field`)?
- Which linters and formatters are configured? (check `.eslintrc`, `.prettierrc`, and `golangci.yml`)
- What are the TypeScript strictness settings? (`strict`, `noImplicitAny`, etc.)
- How are errors handled in each layer? (throwing an exception versus returning a structured error)
- Which logging library is used and what is the message format?
- How are imports organized? (barrel exports, path aliases, and grouping rules)

## 5. INTEGRATIONS.md: external services

- Which external APIs are called? (look for `axios.`, `fetch(`, `http.Get(`, and base URLs in constants)
- How are credentials stored and accessed? (`.env`, secret manager, and environment variables)
- Which databases are connected? (check the manifest for `pg`, `mongoose`, `prisma`, `typeorm`, and `sqlalchemy`)
- Is there an API gateway, service mesh, or proxy between the application and external services?
- Which monitoring or observability tools are used? (APM, Prometheus, and log pipeline)
- Are there message queues or event buses? (Kafka, RabbitMQ, SQS, and Pub/Sub)

## 6. TESTING.md: test setup

- Which test runner is configured? (check `scripts.test` in `package.json`, `pytest.ini`, and `go test`)
- Where are test files? (colocated with source, in `tests/`, or in `__tests__/`)
- Which assertion library is used? (Jest expect, Chai, or pytest assert)
- How are external dependencies mocked? (`jest.mock`, dependency injection, or setup data known as `fixtures`)
- Are there integration tests accessing real services and unit tests with mocks?
- Is there a required coverage threshold? (check `jest.config.js`, `.nycrc`, and `pyproject.toml`)

## 7. CONCERNS.md: known issues

- How many TODOs, FIXMEs, and HACKs exist in production code? (see scan output)
- Which files had the most git changes in the last 90 days? (see scan output)
- Are there files over 500 lines that mix several responsibilities?
- Does any service make sequential calls that could be parallelized?
- Are there hardcoded values (URLs, IDs, or magic numbers) that should be configuration?
- What security risks exist? (missing input validation, raw error messages exposed to clients, or missing authentication checks)
- Are there performance patterns that do not scale? (N+1 queries or in-memory caches in multi-instance setups)
