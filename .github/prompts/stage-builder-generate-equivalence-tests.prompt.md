---
name: "generate-equivalence-tests"
description: "Generates JUnit tests that verify whether the modern Java implementation produces the same outputs as the original Natural program for the same inputs."
argument-hint: "class=<java.package>.<Service> method=<method>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /generate-equivalence-tests

## Objective

Generate JUnit 5 parameterized tests that prove a translated Java method produces business results equivalent to the Natural program for the same inputs.

## When to Invoke

After `/translate-natural-to-java`, to verify equivalence.

## Preconditions

- The Java translation exists and compiles
- The Natural source is in `01-archaeology/legacy-sifap/`
- The Javadoc references the Natural file and lines

## Inputs the Team Must Provide

- Java class and method
- Natural file path
- Data and boundary cases known from Stage 1

## What I Will Do

- Identify inputs, outputs, and all `IF/ELSE`, `DECIDE`, and `AT BREAK` branches
- Generate tests for the happy path, branches, boundaries, nulls, and empty values
- Run the tests, report results, and list uncovered branches

## What I Will NOT Do

- Declare equivalence without a test for each branch
- Omit numeric boundaries or error paths
- Invent expected values; all will be derived from Natural logic

## Output Format

`src/test/java/.../[ClassName]EquivalenceTest.java`

## Definition of Done

- [ ] There is a test for each branch
- [ ] Parameterized tests cover the happy path, branches, boundaries, nulls, and empty values
- [ ] Tests compile and run
- [ ] Results and branch coverage are reported
- [ ] Failures identify the divergent branch

## Prompt Body

You are `@builder`. Generate equivalence tests for a Natural-to-Java translation.

**Step 1 - Locate the source.** Read the Natural file and line references in the Javadoc and open them.

**Step 2 - Identify branches.** List the condition, expected action or output, and inputs that trigger each path. Each `IF...THEN...ELSE` creates two or more paths; `DECIDE ON`, N paths; `AT BREAK`, a control-break path.

**Step 3 - Derive cases.** Create at least one case per branch:

```java
@ParameterizedTest
@CsvSource({
    "input1, input2, expectedOutput",  // Branch 1: [description]
    "input3, input4, expectedOutput",  // Branch 2: [description]
})
void should_produce_equivalent_output(Type param1, Type param2, Type expected) {
    var service = new ServiceUnderTest(/* dependencies */);
    var result = service.methodUnderTest(param1, param2);
    assertThat(result).isEqualTo(expected);
}
```

Include minimums and maximums, empty or single-character strings, nulls, and `BigDecimal` precision equivalent to Natural packed decimals.

**Step 4 - Handle data state.** For record-dependent branches, mock responses for existing and missing records.

**Step 5 - Run.** Report the total, passes, detailed failures, and covered branches out of the total.

**Step 6 - Document unclear branches.**

```java
@Test
@Disabled("MYSTERY: Branch at [nat-file:L73] — unclear condition; cannot derive expected output")
void should_handle_mystery_branch() {
    fail("Needs team investigation — see MYS-NNN");
}
```

## Example Invocation

```text
/generate-equivalence-tests class=<java.package>.<Service> method=<method>
```
