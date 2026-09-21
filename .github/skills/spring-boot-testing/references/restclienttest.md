# @RestClientTest

Isolated REST client testing with MockRestServiceServer.

## Overview

`@RestClientTest` automatically configures:

- RestTemplate/RestClient with mock server support
- Jackson ObjectMapper
- MockRestServiceServer

## Basic setup

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {

  @Autowired
  private WeatherService weatherService;

  @Autowired
  private MockRestServiceServer server;
}
```

## Testing RestTemplate

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {

  @Autowired
  private WeatherService weatherService;

  @Autowired
  private MockRestServiceServer server;

  @Test
  void shouldFetchWeather() {
    // Given
    server.expect(requestTo("https://api.weather.com/v1/current"))
      .andExpect(method(HttpMethod.GET))
      .andExpect(queryParam("city", "Berlin"))
      .andRespond(withSuccess()
        .contentType(MediaType.APPLICATION_JSON)
        .body("{\"temperature\": 22, \"condition\": \"Sunny\"}"));

    // When
    Weather weather = weatherService.getCurrentWeather("Berlin");

    // Then
    assertThat(weather.getTemperature()).isEqualTo(22);
    assertThat(weather.getCondition()).isEqualTo("Sunny");
  }
}
```

## Testing RestClient (Spring 6.1+)

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {

  @Autowired
  private WeatherService weatherService;

  @Autowired
  private MockRestServiceServer server;

  @Test
  void shouldFetchWeatherWithRestClient() {
    server.expect(requestTo("https://api.weather.com/v1/current"))
      .andRespond(withSuccess()
        .body("{\"temperature\": 22}"));

    Weather weather = weatherService.getCurrentWeather("Berlin");

    assertThat(weather.getTemperature()).isEqualTo(22);
  }
}
```

## Request matching

### Exact URL

```java
server.expect(requestTo("https://api.example.com/users/1"))
  .andRespond(withSuccess());
```

### URL pattern

```java
server.expect(requestTo(matchesPattern("https://api.example.com/users/\\d+")))
  .andRespond(withSuccess());
```

### HTTP method

```java
server.expect(ExpectedCount.once(),
  requestTo("https://api.example.com/users"))
  .andExpect(method(HttpMethod.POST))
  .andRespond(withCreatedEntity(URI.create("/users/1")));
```

### Request body

```java
server.expect(requestTo("https://api.example.com/users"))
  .andExpect(content().contentType(MediaType.APPLICATION_JSON))
  .andExpect(content().json("{\"name\": \"John\"}"))
  .andRespond(withSuccess());
```

### Headers

```java
server.expect(requestTo("https://api.example.com/users"))
  .andExpect(header("Authorization", "Bearer token123"))
  .andExpect(header("X-Api-Key", "secret"))
  .andRespond(withSuccess());
```

## Response types

### Success with a body

```java
server.expect(requestTo("/users/1"))
  .andRespond(withSuccess()
    .contentType(MediaType.APPLICATION_JSON)
    .body("{\"id\": 1, \"name\": \"John\"}"));
```

### Success with a resource

```java
server.expect(requestTo("/users/1"))
  .andRespond(withSuccess()
    .body(new ClassPathResource("user-response.json")));
```

### Created

```java
server.expect(requestTo("/users"))
  .andExpect(method(HttpMethod.POST))
  .andRespond(withCreatedEntity(URI.create("/users/1")));
```

### Error response

```java
server.expect(requestTo("/users/999"))
  .andRespond(withResourceNotFound());

server.expect(requestTo("/users"))
  .andRespond(withServerError()
    .body("Internal server error"));

server.expect(requestTo("/users"))
  .andRespond(withStatus(HttpStatus.BAD_REQUEST)
    .body("{\"error\": \"Invalid input\"}"));
```

## Verifying requests

```java
@Test
void shouldCallApi() {
  server.expect(ExpectedCount.once(),
    requestTo("https://api.example.com/data"))
    .andRespond(withSuccess());

  service.fetchData();

  server.verify(); // Verifies that all expectations were met
}
```

## How to ignore additional requests

```java
@Test
void shouldHandleMultipleCalls() {
  server.expect(ExpectedCount.manyTimes(),
    requestTo(matchesPattern("/api/.*")))
    .andRespond(withSuccess());

  // Multiple calls allowed
  service.callApi();
  service.callApi();
  service.callApi();
}
```

## Resetting between tests

```java
@BeforeEach
void setUp() {
  server.reset();
}
```

## Testing timeouts

```java
server.expect(requestTo("/slow-endpoint"))
  .andRespond(withSuccess()
    .body("{\"data\": \"test\"}")
    .delay(100, TimeUnit.MILLISECONDS));

// Tests timeout handling
```

## Best practices

1. Always call `server.verify()` at the end of the test
2. Use resource files for large JSON responses
3. Match the minimum set of request attributes
4. Reset the server in @BeforeEach
5. Test error responses, not just success
6. Verify the request body in POST/PUT calls
