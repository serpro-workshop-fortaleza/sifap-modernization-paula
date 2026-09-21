---
description: "Use when implementing or reviewing authentication, authorization, cryptography, secure configuration, secret handling, and security-sensitive code."
applyTo: "backend/src/main/java/**/auth/**,backend/src/main/java/**/security/**,backend/src/main/java/**/config/**,backend/src/main/resources/**,frontend/**/auth/**,frontend/**/middleware.ts"
---

# Security conventions - Authentication, secrets, and injection

This file activates for security-sensitive code: `auth/`, `security/`, and `config/` packages, everything in `backend/src/main/resources/`, plus `frontend/**/auth/**` and `frontend/middleware.ts`. It teaches authentication, authorization, input validation, CORS, secret handling, and sensitive data protection under the repository's OWASP Top 10 rules. General REST structure lives in [`backend.instructions.md`](backend.instructions.md); Terraform secret storage lives in [`infrastructure.instructions.md`](infrastructure.instructions.md).

## Authentication (OAuth2 / JWT)

The backend is a stateless OAuth2 resource server that validates JWTs through Spring Security. Never hand-roll token parsing or cryptography.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()))
            .cors(Customizer.withDefaults())
            .csrf(csrf -> csrf.disable()); // Stateless token API; no session cookie
        return http.build();
    }
}
```

If passwords are stored, hash with argon2 or bcrypt (never a plain digest), rate-limit login, and require MFA for administrators.

## Authorization

Authorize every request, deny by default, and enforce least privilege. Use method security to check roles and explicitly validate resource ownership.

```java
@PreAuthorize("hasRole('AUDITOR')")
public AuditReport generate(UUID resourceId, Authentication principal) {
    Resource resource = resourceService.getOwned(resourceId, principal.getName());
    // ownership is checked in the service; the role alone is not enough
    return AuditReport.of(resource);
}
```

## Input validation and injection

Validate at every boundary with `@Valid` (see [`backend.instructions.md`](backend.instructions.md)). Build queries only with JPA/JPQL bound parameters, escape HTML on output, and validate uploads by type and size.

> [!WARNING]
> Never concatenate user input into a query, shell command, or markup. String-built SQL is the classic injection vector; parameter binding is mandatory.

## CORS

Explicitly configure allowed origins. The `*` wildcard is forbidden in production.

```java
@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example.gov.br")); // never use "*" in production
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

## Secrets and secure configuration

No secret is hardcoded, committed, or logged. Read secrets from the environment or Key Vault; use Managed Identity for Azure service-to-service authentication. On the frontend, only non-secret values may use the `NEXT_PUBLIC_` prefix; every prefixed value is sent to the browser.

## Sensitive data (CPF, amounts)

> [!IMPORTANT]
> Mask regulated fields (CPF, benefit amounts) in logs, error responses, and URLs. Never put them in query strings or unencrypted storage, and always transmit over TLS.

```java
// keeps the first 3 and last 2 digits of an 11-digit CPF
String masked = cpf.replaceAll("(\\d{3})\\d{6}(\\d{2})", "$1******$2");
```

## Frontend authentication boundary (`middleware.ts`)

Protect routes in middleware; never trust the client to enforce access. Keep tokens and secrets on the server.

```ts
import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session) return NextResponse.redirect(new URL('/login', request.url));
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*'] };
```

## Automation and agent boundaries

An AI agent or automation never grants itself new permissions or accesses a production database without explicit human approval. Changes to authentication, roles, or secret handling require peer review before merge.

## Conventions

| Rule | Rationale |
|---|---|
| OAuth2/JWT through Spring Security | No error-prone custom authentication code |
| Authorize every request and deny by default | Least privilege at every boundary |
| JPA/JPQL bound parameters only | Eliminates SQL injection |
| Explicit CORS origins, no `*` in production | Blocks cross-origin abuse |
| Environment/Key Vault secrets, Managed Identity | No credentials in code or logs |
| Mask CPF and amounts everywhere | Protects regulated data |

## Do / Don't

| Do | Don't |
|---|---|
| Hash passwords with argon2/bcrypt | Store or log plaintext or a plain digest |
| Check the role **and** resource ownership | Treat a role as sufficient authorization |
| Keep secrets on the server | Prefix a secret with `NEXT_PUBLIC_` |
| Mask sensitive fields before logging | Put CPF/amounts in logs or query strings |

## PR Checklist

- [ ] Endpoints authenticate through Spring Security; no custom token parsing
- [ ] Every request is authorized, with deny-by-default and ownership checks where relevant
- [ ] All queries use bound parameters; uploads and inputs are validated
- [ ] CORS lists explicit origins; no `*` in production configuration
- [ ] No secret is hardcoded, committed, or logged; Azure authentication uses Managed Identity
- [ ] CPF, amounts, and tokens are masked in logs, errors, and URLs
