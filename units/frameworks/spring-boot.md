---
id: spring-boot
title: Spring Boot
paths: ["**/src/main/resources/application*.{yml,yaml,properties}", "**/*Controller.{kt,java}", "**/*Application.{kt,java}"]
---
Spring Boot. Follow the official reference documentation's conventions (docs.spring.io/spring-boot).

Structure
- Package by feature (`auth/`, `tags/`), each with its controller, service, repository and DTOs.
- Constructor injection only (no field `@Autowired`); in Kotlin, primary constructors with `private val`.
- Controllers stay thin: map HTTP to a service call and back. Business rules live in services; persistence in repositories.
- Never expose JPA entities in the API; map to request/response DTOs, validated with Bean Validation (`@Valid`, `@NotBlank`).

Configuration
- Typed `@ConfigurationProperties` classes over scattered `@Value`.
- Profiles for environments (`application-dev.yml`); secrets from environment variables or a secret store, never committed in `application*.yml`.

Persistence
- Transactions on service methods (`@Transactional`), read-only where possible; never on controllers.
- Watch for N+1 queries: fetch joins or entity graphs; keep `open-in-view` disabled.
- Schema changes only through migrations (Flyway or Liquibase), never `ddl-auto=update` outside throwaway local setups.

Errors and API
- One `@RestControllerAdvice` mapping exceptions to consistent error responses (`ProblemDetail`); no stack traces to clients.
- Correct status codes (201 with `Location` on create, 404, 409, 422), and pagination for lists.

Security
- Spring Security with explicit rules: deny by default, allow public endpoints by name. Stateless JWT for APIs; CSRF stays on for cookie sessions.

Verify
- `@WebMvcTest` / `@DataJpaTest` slices for focused tests, `@SpringBootTest` with Testcontainers for integration; run the touched module's tests through the build tool.
