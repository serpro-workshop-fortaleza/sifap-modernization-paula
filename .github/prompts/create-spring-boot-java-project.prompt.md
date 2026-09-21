---
name: "create-spring-boot-java-project"
description: "Scaffold the SIFAP 2.0 Spring Boot backend (Java 21 + PostgreSQL 16), delegating the mechanics to the create-spring-boot-java-project skill."
argument-hint: "projectName=<artifactId>"
agent: "implementer"
tools: ["read", "edit", "search", "execute"]
---
# /create-spring-boot-java-project

## Objective

Create a new Spring Boot backend scaffold for SIFAP 2.0 and configure its foundation, pinned to the kit's stack: Java 21 + Spring Boot 3.3 + PostgreSQL 16. The detailed mechanics are in the [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) skill. This prompt applies them without repetition and overrides the skill's generic defaults.

> [!IMPORTANT]
> `backend/` does not exist yet. This command creates it from scratch in Stage 3. Do not assume an inherited prototype.

## When to Invoke

At the start of Stage 3, when the team creates the `backend/` module for the first time.

## Preconditions

- Java 21, Docker, and Docker Compose are installed
- The team has agreed on the artifact name and base package
- No `backend/` module exists yet

## Inputs the Team Must Provide

- `projectName`: the Maven `artifactId` of the new module
- The base package, for example, `com.sifap.<context>`
- Ask the user for any missing information.

## What I Will Do

- Follow the creation steps in the [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) skill
- Override the defaults for this kit: Spring Boot 3.3.x, PostgreSQL 16, no Redis, and no MongoDB
- Generate the project in `backend/` with the `web, data-jpa, postgresql, validation, testcontainers` starters and `springdoc-openapi-starter-webmvc-ui`
- Run `./mvnw clean test` to confirm that the scaffold compiles

## What I Will NOT Do

- Add `data-redis`, `data-mongodb`, or their configuration blocks
- Create the scaffold at the repository root or use Spring Boot 3.4.x
- Create Docker Compose services other than PostgreSQL 16
- Commit secrets; credentials belong in environment variables or Azure Key Vault

## Output Format

```markdown
### Created
- Spring Boot 3.3 scaffold in `backend/` (Java 21, PostgreSQL 16)
- Dependencies: web, data-jpa, postgresql, validation, testcontainers, springdoc
- `docker-compose.yaml` (PostgreSQL 16 only) — optional

### Build
`./mvnw clean test` → BUILD SUCCESS
```

## Definition of Done

- [ ] `backend/` contains a Spring Boot 3.3 scaffold on Java 21
- [ ] Dependencies match those defined by the kit; Redis and MongoDB are absent
- [ ] Any Docker Compose configuration contains PostgreSQL 16 only
- [ ] `./mvnw clean test` passes and no secrets have been committed

## Prompt Body

The [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) skill defines the start.spring.io download and configuration steps. Read it and apply it with the kit overrides below.

**Step 1 — Confirm inputs.**
Define the `artifactId` and base package with the team. Check that Java 21 is available.

**Step 2 — Apply the skill.**
Generate the project according to the skill, restrict dependencies to the kit's stack, and remove Redis and MongoDB.

**Step 3 — Follow the kit's rules.**
Use Spring Boot 3.3.x and PostgreSQL 16, create the scaffold in `backend/`, and limit Docker Compose, if any, to PostgreSQL 16.

**Step 4 — Verify.**
Run `./mvnw clean test` and confirm a successful build before handoff.

## Example Invocation

```text
/create-spring-boot-java-project projectName=sifap-backend
```
