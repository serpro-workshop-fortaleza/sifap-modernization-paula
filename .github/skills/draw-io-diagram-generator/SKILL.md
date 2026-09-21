---
name: "draw-io-diagram-generator"
description: "Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png). Covers mxGraph XML creation, shape libraries, style strings, flowcharts, system architecture, sequence diagrams, ER diagrams, UML class diagrams, network topology, layout strategy, the hediet.vscode-drawio VS Code extension, and the complete agent workflow from request to ready-to-open file."
---
# draw.io diagram generator

This skill lets you generate, edit, and validate draw.io diagram files (`.drawio`) with the correct mxGraph XML structure. All generated files open immediately in the [draw.io extension for VS Code](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) (`hediet.vscode-drawio`), without requiring manual fixes. You can also open the files in the draw.io web or desktop app.

| Section | Purpose |
|---|---|
| When to Invoke | Trigger phrases and supported diagram types |
| Prerequisites | Extension and optional Python tools |
| Step-by-step agent workflow | From request to layout, XML, and validated file |
| Recipes by diagram type | Flowchart, architecture, sequence, ER, and UML snippets |
| Multiple pages and editing | Multipage files and safe edits to existing diagrams |
| Output Template | Exact `.drawio` artifact to deliver |
| Quality Gate | Structural checks before delivery |
| References | Bundled templates, references, and scripts |

---

## When to Invoke

- "Create a system architecture diagram for these services."
- "Draw a flowchart of this approval process."
- "Generate an ER diagram from these tables."
- "Turn this sequence of API calls into a sequence diagram."

Any request to produce or modify a `.drawio`, `.drawio.svg`, or `.drawio.png` file loads this skill. Related trigger phrases include "design a sequence diagram", "make a UML class diagram", "create an ER diagram", "document the architecture", "show the data model", and "visualize the flow".

> [!NOTE]
> Generated files render in the **draw.io extension for VS Code** (`hediet.vscode-drawio`), the editor used for diagrams in the immersion. If it is not installed, the `.drawio` file remains valid. In that case, open it in the draw.io web or desktop app. The Python helpers stored in `scripts/` are optional and require Python 3.8+.

**Supported diagram types**

| Diagram type | Available template | Description |
|---|---|---|
| Flowchart | `assets/templates/flowchart.drawio` | Process flows with decisions and branches |
| System architecture | `assets/templates/architecture.drawio` | Multitier service architecture |
| Sequence diagram | `assets/templates/sequence.drawio` | Actor lifelines and timed message flows |
| ER diagram | `assets/templates/er-diagram.drawio` | Database tables with relationships |
| UML class diagram | `assets/templates/uml-class.drawio` | Classes, interfaces, enums, and relationships |
| Network topology | (use shape library) | Routers, servers, firewalls, and subnets |
| BPMN workflow | (use shape library) | Business process events, tasks, and decision elements (`gateways`) |
| Mind map | (manual) | Central topic with radial branches |

---

## Prerequisites

- If using VS Code integration, install the **draw.io extension for VS Code**, whose ID is `hediet.vscode-drawio`. Install it with:

  ```text
  ext install hediet.vscode-drawio
  ```

- **Supported file extensions**: `.drawio`, `.drawio.svg`, `.drawio.png`
- **Python 3.8+** (optional): for the validation and shape insertion programs in `scripts/`

---

## Step-by-step agent workflow

Follow these steps in order for every diagram generation task.

### Step 1: understand the request

Ask or infer:

1. **Diagram type**: what kind of diagram? (flowchart, architecture, UML, ER, sequence, network...)
2. **Entities / actors**: what are the main components, actors, classes, or tables?
3. **Relationships**: how do they connect? In which direction? With what cardinality?
4. **Output path**: where should the `.drawio` file be saved?
5. **Existing file**: are we creating a file or editing an existing one?

If the request is ambiguous, infer the most appropriate diagram type from context (for example, "show the tables" → ER diagram; "show the API call flow" → sequence diagram).

### Step 2: select a template or start from scratch

- **Use a template** when the diagram type matches a template in `assets/templates/`. Copy the structure and replace the placeholder values.
- **Start from scratch** for new layouts. Begin with the minimum valid structure:

```xml
<!-- Set modified="" to the current ISO 8601 timestamp when generating a new file -->
<mxfile host="Electron" modified="" version="26.0.0">
  <diagram id="page-1" name="Page-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Your cells go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

> **Rule**: IDs `0` and `1` are ALWAYS required and must be the first two cells. Never reuse them.

### Step 3: plan the layout

Before generating XML, sketch the logical placement:

- Arrange in **rows** or **tiers** (use lanes, called `swimlane` in draw.io, to represent tiers)
- **Horizontal spacing**: 40–60 px between shapes on the same row
- **Vertical spacing**: 80–120 px between tier rows
- Default shape size: `120x60` px for process boxes, `160x80` px for swimlanes
- Default canvas: landscape A4 = `1169 x 827` px

### Step 4: generate mxGraph XML

**Vertex cell** (all shapes):

```xml
<mxCell id="unique-id" value="Label"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

**Edge cell** (all connectors):

```xml
<mxCell id="edge-id" value="Label (optional)"
        style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="source-id" target="target-id" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**Critical rules**:

- Every cell ID must be **globally unique** in the file
- Every vertex must have an `mxGeometry` child with `x`, `y`, `width`, `height`, `as="geometry"`
- Every edge must have `source` and `target` matching existing vertex IDs. **Exception**: floating edges (for example, sequence diagram lifelines) use `sourcePoint`/`targetPoint` inside `<mxGeometry>`; see the sequence diagram recipe
- Each cell's `parent` must reference an existing cell ID
- Use `html=1` in the style when the label contains HTML (`<b>`, `<i>`, `<br>`)
- Escape special XML characters in labels: `&` => `&amp;`, `<` => `&lt;`, `>` => `&gt;`

### Step 5: apply the correct styles

Use the standard semantic color palette for consistency:

| Purpose | fillColor | strokeColor |
|---|---|---|
| Primary / Information | `#dae8fc` | `#6c8ebf` |
| Success / Start | `#d5e8d4` | `#82b366` |
| Warning / Decision | `#fff2cc` | `#d6b656` |
| Error / End | `#f8cecc` | `#b85450` |
| Neutral | `#f5f5f5` | `#666666` |
| External / Partner | `#e1d5e7` | `#9673a6` |

Common style strings by diagram type:

| Purpose | Style string |
|---|---|
| Rounded process box (flowchart) | `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;` |
| Decision diamond | `rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` |
| Start/end terminal | `ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;` |
| Database cylinder | `shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;` |
| Swimlane container (tier) | `swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;` |
| UML class box | `swimlane;fontStyle=1;align=center;startSize=40;fillColor=#dae8fc;strokeColor=#6c8ebf;` |
| Interface / stereotype box | `swimlane;fontStyle=3;align=center;startSize=40;fillColor=#f5f5f5;strokeColor=#666666;` |
| ER table container | `shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;` |
| Orthogonal connector | `edgeStyle=orthogonalEdgeStyle;html=1;` |
| ER relationship (crow's foot) | `edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;startArrow=ERone;` |

> See `references/style-reference.md` for the complete style key catalog and `references/shape-libraries.md` for all shape library names.

### Step 6: save and validate

1. **Write the file** to the requested path with the `.drawio` extension
2. **Run the validator** (optional but recommended):

   ```bash
   python .github/skills/draw-io-diagram-generator/scripts/validate-drawio.py <path-to-file.drawio>
   ```

3. **Tell the user** how to open the file:

  > "Open `<filename>` in VS Code. The draw.io extension will render it automatically. Alternatively, you can use the draw.io web or desktop app."

4. **Provide a brief description** of the diagram's contents so the user knows what to expect.

---

## Recipes by diagram type

### Flowchart

Key elements: Start (ellipse) => Process (rounded rectangle) => Decision (diamond) => End (ellipse)

```xml
<!-- Start node -->
<mxCell id="start" value="Start"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="80" width="120" height="60" as="geometry" />
</mxCell>

<!-- Process -->
<mxCell id="p1" value="Process step"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="200" width="120" height="60" as="geometry" />
</mxCell>

<!-- Decision -->
<mxCell id="d1" value="Condition?"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="460" y="320" width="200" height="100" as="geometry" />
</mxCell>

<!-- Arrow: start to p1 -->
<mxCell id="e1" value=""
        style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="start" target="p1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Architecture diagram (three tiers)

Use **lane containers (`swimlane`)** for each tier. All service boxes are children of their respective lane.

```xml
<!-- Tier swimlane -->
<mxCell id="tier1" value="Client tier"
        style="swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="60" y="100" width="1050" height="130" as="geometry" />
</mxCell>

<!-- Service within the tier (parent="tier1", coordinates relative to the tier) -->
<mxCell id="webapp" value="Web app"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="tier1">
  <mxGeometry x="80" y="40" width="120" height="60" as="geometry" />
</mxCell>
```

> Cross-tier connectors use absolute coordinates with `parent="1"`.

### Sequence diagram

Key elements: actors (top), lifelines (vertical dashed lines), activation boxes, and message arrows.

- Lifelines: `edge="1"` with `endArrow=none` and `dashed=1`, without source/target. Use `sourcePoint`/`targetPoint` in the geometry
- Synchronous message: `endArrow=block;endFill=1`
- Return message: `endArrow=open;endFill=0;dashed=1`
- Self-call: loop the edge through two Array points to the right and back

**Minimal XML snippet:**

```xml
<!-- Actor (human figure) -->
<mxCell id="actorA" value="Client"
        style="shape=mxgraph.uml.actor;pointerEvents=1;dashed=0;whiteSpace=wrap;html=1;aspect=fixed;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="80" width="60" height="80" as="geometry" />
</mxCell>

<!-- Service box -->
<mxCell id="actorB" value="API server"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="480" y="100" width="160" height="60" as="geometry" />
</mxCell>

<!-- Lifeline, floating edge: uses sourcePoint/targetPoint, NOT source/target attributes -->
<mxCell id="lifA" value=""
        style="edgeStyle=none;dashed=1;endArrow=none;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="140" y="160" as="sourcePoint" />
    <mxPoint x="140" y="700" as="targetPoint" />
  </mxGeometry>
</mxCell>

<!-- Activation box (narrow rectangle on the lifeline) -->
<mxCell id="actA1" value=""
        style="fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="130" y="220" width="20" height="180" as="geometry" />
</mxCell>

<!-- Synchronous message -->
<mxCell id="msg1" value="POST /orders"
        style="edgeStyle=elbowEdgeStyle;elbow=vertical;html=1;endArrow=block;endFill=1;"
        edge="1" source="actA1" target="actorB" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Return message (dashed) -->
<mxCell id="msg2" value="201 Created"
        style="edgeStyle=elbowEdgeStyle;elbow=vertical;dashed=1;html=1;endArrow=open;endFill=0;"
        edge="1" source="actorB" target="actA1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

> **Note:** lifelines are floating edges that use `sourcePoint`/`targetPoint` in `<mxGeometry>` instead of `source`/`target` attributes. This is the draw.io pattern for sequence diagrams.

### ER diagram

Use `shape=table` containers with `childLayout=tableLayout`. Rows are `shape=tableRow` cells with `portConstraint=eastwest`. Columns within each row are `shape=partialRectangle`.

Relationship arrows use `edgeStyle=entityRelationEdgeStyle`:

- One-to-one: `startArrow=ERone;endArrow=ERone`
- One-to-many: `startArrow=ERone;endArrow=ERmany`
- Many-to-many: `startArrow=ERmany;endArrow=ERmany`
- Required: `ERmandOne`; optional: `ERzeroToOne`

### UML class diagram

Class boxes are swimlane containers. Attributes and methods are plain text cells. Dividers are swimlane children with zero height.

Arrow styles by relationship type:

| Relationship | Style string |
|---|---|
| Inheritance (extends) | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=0;` |
| Realization (implements) | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=block;endFill=0;` |
| Composition | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=1;endArrow=none;` |
| Aggregation | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=0;endArrow=none;` |
| Dependency | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=open;endFill=0;` |
| Association | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=open;endFill=0;` |

---

## Multipage diagrams

Add multiple `<diagram>` elements for complex systems:

```xml
<mxfile host="Electron" version="26.0.0">
  <diagram id="overview" name="Overview">
    <!-- Overview mxGraphModel -->
  </diagram>
  <diagram id="detail" name="Detailed view">
    <!-- Detailed view mxGraphModel -->
  </diagram>
</mxfile>
```

Each page has its own independent namespace for cell IDs. The same ID value can appear on different pages without conflict.

---

## Editing existing diagrams

When modifying an existing `.drawio` file:

1. **Read** the file first to understand existing cell IDs, positions, and parent hierarchy
2. **Identify the target diagram page** by index or `name` attribute
3. **Assign new unique IDs** that do not collide with existing IDs
4. **Respect the container hierarchy**: children of a lane (`swimlane`) use coordinates relative to the parent
5. **Check edges**: after repositioning nodes, confirm that edge source/target IDs remain valid

Use `scripts/add-shape.py` to safely add a single shape without editing raw XML:

```bash
python .github/skills/draw-io-diagram-generator/scripts/add-shape.py docs/arch.drawio "New service" 700 380
```

---

## Best practices

**Layout**

- Align shapes to the 10 px grid (all coordinates divisible by 10)
- Group related shapes within lane containers (`swimlane`)
- Use one diagram topic per page; use multipage files for complex systems
- Keep 40 cells or fewer per page for readability

**Labels**

- Add a title text cell (`text;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1`) at the top of each page
- Always set `whiteSpace=wrap;html=1` on vertex shapes
- Keep labels concise, with three words or fewer per shape where possible

**Style consistency**

- Consistently use the semantic color palette from Apply the correct styles (Step 5) throughout the project
- Prefer `edgeStyle=orthogonalEdgeStyle` for clean right-angle connectors
- Do not insert arbitrary HTML into labels unless necessary

**File naming**

- Use kebab-case: `order-service-flow.drawio`, `database-schema.drawio`
- Place diagrams beside the code they document: `docs/` or `architecture/`

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| File opens blank in VS Code | Missing id=0 or id=1 cell | Add both root cells before the others |
| Shape is in the wrong position | Child inside a container; coordinates are relative | Check `parent`; adjust x/y relative to the container |
| Edge is not visible | Source or target ID does not match any vertex | Verify that both IDs exist exactly as written |
| Diagram shows "Compressed" | mxGraphModel is base64-encoded | Open in the draw.io web app and use File > Export > XML (uncompressed) |
| Shape style does not render | Typo in the shape= name | Look up the exact style string in `references/shape-libraries.md` |
| Label shows escaped HTML | html=0 on a cell with an HTML label | Add `html=1;` to the cell style |
| Container children overlap the border | Container height is too small | Increase the container height in mxGeometry |

---

## Output Template

Deliver a complete, valid `.drawio` file. The minimal well-formed artifact produced by this skill looks like this:

```xml
<mxfile host="Electron" modified="2026-01-01T00:00:00.000Z" version="26.0.0">
  <diagram id="page-1" name="Overview">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="System overview"
                style="text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;"
                vertex="1" parent="1">
          <mxGeometry x="60" y="30" width="300" height="30" as="geometry" />
        </mxCell>
        <mxCell id="webapp" value="Web app"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="100" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="api" value="API server"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
                vertex="1" parent="1">
          <mxGeometry x="320" y="100" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;html=1;"
                edge="1" source="webapp" target="api" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Along with the file, always provide:

1. **A one-sentence summary** of what the diagram shows.
2. **How to open it**:

  > "Open `<filename>` in VS Code. The draw.io extension will render it automatically. Alternatively, open it in the draw.io web or desktop app."

3. **How to edit it** (if customization is likely):

  > "Click a shape to select it. Double-click to edit the label. Drag to reposition."

4. **Validation status**: state whether the validator program was run and passed.

---

## Quality Gate

Before delivering any generated `.drawio` file, verify:

- [ ] The file starts with the `<mxfile>` root element
- [ ] Every `<diagram>` has a nonempty `id` attribute
- [ ] `<mxCell id="0" />` is the first cell in each diagram
- [ ] `<mxCell id="1" parent="0" />` is the second cell in each diagram
- [ ] All cell `id` values are unique within each diagram
- [ ] Every vertex cell has `vertex="1"` and an `<mxGeometry as="geometry">` child
- [ ] Every edge cell has `edge="1"` and one of: (a) `source`/`target` pointing to existing vertex IDs; or (b) `<mxPoint as="sourcePoint">` and `<mxPoint as="targetPoint">` in its `<mxGeometry>` (floating edge, used for sequence diagram lifelines)
- [ ] Every cell (except id=0) has a `parent` pointing to an existing ID
- [ ] The style contains `html=1` for any label with HTML tags
- [ ] XML is well formed (no unclosed tags or unescaped `&`, `<`, `>` in attribute values)
- [ ] A title label cell exists at the top of each page

Run the automated validator:

```bash
python .github/skills/draw-io-diagram-generator/scripts/validate-drawio.py <file.drawio>
```

---

## References

All supporting files are in `.github/skills/draw-io-diagram-generator/`:

| File | Contents |
|---|---|
| `references/drawio-xml-schema.md` | Complete mxfile / mxGraphModel / mxCell attribute reference, coordinate system, reserved cells, and validation rules |
| `references/style-reference.md` | All style keys with allowed values, vertex and edge style keys, shape catalog, and semantic color palette |
| `references/shape-libraries.md` | All shape library categories (General, Flowchart, UML, ER, Network, BPMN, Mockup, K8s) with style strings |
| `assets/templates/flowchart.drawio` | Ready-to-use flowchart template |
| `assets/templates/architecture.drawio` | Four-tier system architecture template |
| `assets/templates/sequence.drawio` | Sequence diagram template with three actors |
| `assets/templates/er-diagram.drawio` | ER diagram with three tables and crow's foot relationships |
| `assets/templates/uml-class.drawio` | Interface + two classes + enum with relationship arrows |
| `scripts/validate-drawio.py` | Python program to validate the XML structure of any .drawio file |
| `scripts/add-shape.py` | Python command-line interface (CLI) to add a new shape to an existing diagram |
| `scripts/README.md` | How to use the helper programs, with examples |
