---
name: "create-spring-boot-java-project"
description: "Scaffold a Spring Boot (Java 21) project through start.spring.io with Maven, springdoc-openapi, and ArchUnit, ready to run with Docker Compose. Use when someone wants to start a new Spring Boot backend application or generate a starter project. Aligns with the kit's Java 21 + Spring Boot 3.3 stack."
---
# Create a Java project with Spring Boot

Create a new Spring Boot 3.3 backend application scaffold in Java 21, pinned to the kit's stack (PostgreSQL 16, Maven, springdoc-openapi, ArchUnit, and Testcontainers). Run all commands in the integrated terminal in VS Code, the kit's only approved editor. The guided [`/create-spring-boot-java-project`](../../prompts/create-spring-boot-java-project.prompt.md) command applies kit-specific overrides (target module and dependency set).

> [!IMPORTANT]
> The kit uses **PostgreSQL 16 only**, with no Redis or MongoDB. Create the scaffold in a new `backend/` module; it does not exist yet (the team creates it in Stage 3). Never commit credentials to Git history. Supply them through environment variables.

## When to Invoke

- "Start a new Spring Boot backend application for us."
- "Scaffold the `backend/` module."
- "Generate a Spring Boot 3.3 starter project in Java 21 with PostgreSQL."
- "Set up the project structure so we can start Stage 3."

## Prerequisites

Confirm that the required tools are installed:

| Tool | Purpose |
|---|---|
| Java 21 (JDK) | Build and run the application |
| Docker + Docker Compose | Run PostgreSQL 16 locally |
| VS Code | Kit-approved editor |

To customize the artifact name or base package, change `artifactId` and `packageName` in [Download the Spring Boot project template](#download-the-spring-boot-project-template). To change the Spring Boot version, change `bootVersion` in the same step. Keep the version within the kit's 3.3.x line.

## Check the Java version

```shell
java -version
```

Confirm that the output reports Java 21.

## Download the Spring Boot project template

Download a Maven + Java 21 scaffold from start.spring.io with the kit's dependency set (no Redis or MongoDB):

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-java} \
  -d bootVersion=3.3.5 \
  -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,validation,testcontainers \
  -d javaVersion=21 \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

## Extract and clean up

```shell
unzip starter.zip -d ./${input:projectName:demo-java}
rm -f starter.zip
cd ${input:projectName:demo-java}
```

## Add springdoc-openapi and ArchUnit

Insert the `springdoc-openapi-starter-webmvc-ui` and `archunit-junit5` dependencies in `pom.xml`:

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.8.6</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.2.1</version>
  <scope>test</scope>
</dependency>
```

## Configure SpringDoc and JPA

Add the SpringDoc UI settings to `application.properties`:

```properties
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
```

Add the PostgreSQL datasource and JPA settings. Read the password from an environment variable. Never hardcode it:

```properties
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=${POSTGRES_PASSWORD}
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

> [!NOTE]
> Use `ddl-auto=validate` (not `update`) so that versioned Flyway migrations control the schema, per [`database.instructions.md`](../../instructions/database.instructions.md). Set `POSTGRES_PASSWORD` in the shell or a local Git-ignored `.env` file, never in `application.properties`.

## Add Docker Compose (PostgreSQL 16 only)

Create `compose.yaml` at the project root with a single PostgreSQL 16 service:

```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
```

Add the data directory to `.gitignore`:

```gitignore
postgres_data
```

## Verify the build

Testcontainers provides a real PostgreSQL 16 instance for tests. This lets the build run without manually starting a database:

```shell
./mvnw clean test
```

To run the application with a local database, start the Compose service first:

```shell
docker compose up -d
./mvnw spring-boot:run
docker compose down
```

## Output Template

```markdown
### Created
- `backend/`: Spring Boot 3.3 scaffold (Java 21, Maven)
- Dependencies: web, data-jpa, postgresql, validation, testcontainers, lombok, springdoc, archunit
- `compose.yaml`: PostgreSQL 16 service only

### Build
`./mvnw clean test` -> BUILD SUCCESS
```

## Quality Gate

- [ ] The scaffold uses Spring Boot 3.3.x on Java 21 and was generated in a new `backend/` module.
- [ ] The dependency set matches the kit; there is no Redis, MongoDB, or caching starter (`cache`).
- [ ] Every Docker Compose file defines only a PostgreSQL 16 service.
- [ ] No credentials are hardcoded; the datasource password comes from `POSTGRES_PASSWORD`.
- [ ] `./mvnw clean test` passes (BUILD SUCCESS) before handing off the scaffold.
