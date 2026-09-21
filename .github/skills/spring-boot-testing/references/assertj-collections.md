# AssertJ collections

AssertJ assertions for collections: `List`, `Set`, `Map`, arrays, and streams.

## When to use this reference

- The tested value is a `List`, `Set`, `Map`, array, or `Stream`
- You need to check multiple elements, their order, or specific fields
- You use `extracting()`, `filteredOn()`, `containsExactly()`, or similar collection methods
- To check a single scalar or object, use [assertj-basics.md](assertj-basics.md)

## Basic collection checks

```java
List<Order> orders = orderService.findAll();

assertThat(orders).isNotEmpty();
assertThat(orders).isEmpty();
assertThat(orders).hasSize(3);
assertThat(orders).hasSizeGreaterThan(0);
assertThat(orders).hasSizeLessThanOrEqualTo(10);
```

## Containment assertions

```java
// Contains (any order, allows additional items)
assertThat(orders).contains(order1, order2);

// Contains exactly these elements in this order (no additional items)
assertThat(statuses).containsExactly("NEW", "PENDING", "COMPLETED");

// Contains exactly these elements in any order (no additional items)
assertThat(statuses).containsExactlyInAnyOrder("COMPLETED", "NEW", "PENDING");

// Contains any of these elements (at least one match)
assertThat(statuses).containsAnyOf("NEW", "CANCELLED");

// Does not contain
assertThat(statuses).doesNotContain("DELETED");
```

## Field extraction

Extract a field from each element before asserting:

```java
assertThat(orders)
  .extracting(Order::getStatus)
  .containsExactly("NEW", "PENDING", "COMPLETED");
```

Extract multiple fields as tuples:

```java
assertThat(orders)
  .extracting(Order::getId, Order::getStatus)
  .containsExactly(
    tuple(1L, "NEW"),
    tuple(2L, "PENDING"),
    tuple(3L, "COMPLETED")
  );
```

## Filtering before assertion

```java
assertThat(orders)
  .filteredOn(order -> order.getStatus().equals("PENDING"))
  .hasSize(2)
  .extracting(Order::getId)
  .containsExactlyInAnyOrder(1L, 3L);

// Filters by field value
assertThat(orders)
  .filteredOn("status", "PENDING")
  .hasSize(2);
```

## Predicate checks

```java
assertThat(orders).allMatch(o -> o.getTotal().compareTo(BigDecimal.ZERO) > 0);
assertThat(orders).anyMatch(o -> o.getStatus().equals("COMPLETED"));
assertThat(orders).noneMatch(o -> o.getStatus().equals("DELETED"));

// With a description for failure messages
assertThat(orders)
  .allSatisfy(o -> assertThat(o.getId()).isPositive());
```

## Ordered per-element assertions

Check each element in order with individual conditions:

```java
assertThat(orders).satisfiesExactly(
  first  -> assertThat(first.getStatus()).isEqualTo("NEW"),
  second -> assertThat(second.getStatus()).isEqualTo("PENDING"),
  third  -> {
    assertThat(third.getStatus()).isEqualTo("COMPLETED");
    assertThat(third.getTotal()).isGreaterThan(BigDecimal.ZERO);
  }
);
```

## Nested and flat collections

```java
// flatExtracting: flattens one level of nested collections
assertThat(orders)
  .flatExtracting(Order::getItems)
  .extracting(OrderItem::getProduct)
  .contains("Laptop", "Mouse");
```

## Recursive field comparison

Compare elements by fields, not object identity:

```java
assertThat(orders)
  .usingRecursiveFieldByFieldElementComparator()
  .containsExactlyInAnyOrder(expectedOrder1, expectedOrder2);

// Ignores specific fields (for example, generated IDs or timestamps)
assertThat(orders)
  .usingRecursiveFieldByFieldElementComparatorIgnoringFields("id", "createdAt")
  .containsExactly(expectedOrder1, expectedOrder2);
```

## Map assertions

```java
Map<String, Integer> stockByProduct = inventoryService.getStock();

assertThat(stockByProduct)
  .isNotEmpty()
  .hasSize(3)
  .containsKey("Laptop")
  .doesNotContainKey("Fax Machine")
  .containsEntry("Laptop", 10)
  .containsEntries(entry("Laptop", 10), entry("Mouse", 50));

assertThat(stockByProduct)
  .hasEntrySatisfying("Laptop", qty -> assertThat(qty).isGreaterThan(0));
```

## Array assertions

```java
String[] roles = user.getRoles();

assertThat(roles).hasSize(2);
assertThat(roles).contains("ADMIN");
assertThat(roles).containsExactlyInAnyOrder("USER", "ADMIN");
```

## Set assertions

```java
Set<String> tags = product.getTags();

assertThat(tags).contains("electronics", "sale");
assertThat(tags).doesNotContain("expired");
assertThat(tags).hasSizeGreaterThanOrEqualTo(1);
```

## Static import

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.tuple;
import static org.assertj.core.api.Assertions.entry;
```

## Key points

1. **`containsExactly` versus `containsExactlyInAnyOrder`**: use the former when order matters
2. **`extracting()` before containment checks**: avoids implementing `equals()` on domain objects
3. **`filteredOn()` + `extracting()`**: combine them to precisely check a collection subset
4. **`satisfiesExactly()`**: use when each element requires different assertions
5. **`usingRecursiveFieldByFieldElementComparator()`**: prefer it to `equals()` for DTOs and records
