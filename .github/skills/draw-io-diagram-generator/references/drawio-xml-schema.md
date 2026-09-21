# draw.io XML schema reference

Complete reference for the `.drawio` file format (mxGraph XML). Use it when generating, parsing, or validating diagram files.

---

## Top-level structure

Every `.drawio` file is XML with this root structure:

```xml
<!-- Set modified to the current ISO 8601 timestamp when generating a new file -->
<mxfile host="Electron" modified=""
        agent="draw.io" version="26.0.0" type="device">
  <diagram id="<unique-id>" name="<Page name>">
    <mxGraphModel ...attributes...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- All content cells go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### `<mxfile>` attributes

| Attribute | Required | Default | Description |
| ----------- | ---------- | --------- | ------------- |
| `host` | No | `"app.diagrams.net"` | Originating editor (`"Electron"` for desktop/VS Code) |
| `modified` | No | — | ISO 8601 timestamp |
| `agent` | No | — | User agent string |
| `version` | No | — | draw.io version |
| `type` | No | `"device"` | Storage type |

### `<diagram>` attributes

| Attribute | Required | Description |
| ----------- | ---------- | ------------- |
| `id` | Yes | Unique page identifier (any string) |
| `name` | Yes | Tab label displayed in the editor |

### `<mxGraphModel>` attributes

| Attribute | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `dx` | int | `1422` | X-axis scroll offset |
| `dy` | int | `762` | Y-axis scroll offset |
| `grid` | `0`/`1` | `1` | Show grid |
| `gridSize` | int | `10` | Grid snap size in px |
| `guides` | `0`/`1` | `1` | Show alignment guides |
| `tooltips` | `0`/`1` | `1` | Enable tooltips |
| `connect` | `0`/`1` | `1` | Enable connection arrows on hover |
| `arrows` | `0`/`1` | `1` | Show directional arrows |
| `fold` | `0`/`1` | `1` | Enable group expansion/collapse |
| `page` | `0`/`1` | `1` | Show page boundary |
| `pageScale` | float | `1` | Page zoom scale |
| `pageWidth` | int | `1169` | Page width in px (landscape A4) |
| `pageHeight` | int | `827` | Page height in px (landscape A4) |
| `math` | `0`/`1` | `0` | Enable LaTeX math rendering |
| `shadow` | `0`/`1` | `0` | Global shape shadow |

**Common page sizes (px at 96 dpi):**

| Format | Width | Height |
| -------- | ------- | -------- |
| Landscape A4 | `1169` | `827` |
| Portrait A4 | `827` | `1169` |
| Landscape A3 | `1654` | `1169` |
| Landscape Letter | `1100` | `850` |
| Portrait Letter | `850` | `1100` |
| Screen (16:9) | `1654` | `931` |

---

## Reserved cells (always required)

```xml
<mxCell id="0" />                 <!-- Root cell: never omit or add attributes -->
<mxCell id="1" parent="0" />     <!-- Default layer: all cells are children of this one -->
```

These two cells MUST be the first entries inside `<root>`. IDs `0` and `1` are reserved and cannot be used by any other cell.

---

## Vertex element (shape)

```xml
<mxCell
  id="2"
  value="Label text"
  style="rounded=1;whiteSpace=wrap;html=1;"
  vertex="1"
  parent="1">
  <mxGeometry x="200" y="160" width="120" height="60" as="geometry" />
</mxCell>
```

### `<mxCell>` vertex attributes

| Attribute | Required | Type | Description |
| ----------- | ---------- | ------ | ------------- |
| `id` | Yes | string | Unique identifier in this diagram |
| `value` | Yes | string | Label text (HTML allowed if the style has `html=1`) |
| `style` | Yes | string | Semicolon-delimited key=value style string |
| `vertex` | Yes | `"1"` | Must be `"1"` to declare a shape |
| `parent` | Yes | string | Parent cell ID (`"1"` for the default layer) |

### `<mxGeometry>` vertex attributes

| Attribute | Required | Type | Description |
| ----------- | ---------- | ------ | ------------- |
| `x` | Yes | float | Left edge of the shape (px from the canvas origin) |
| `y` | Yes | float | Top edge of the shape (px from the canvas origin) |
| `width` | Yes | float | Shape width in px |
| `height` | Yes | float | Shape height in px |
| `as` | Yes | `"geometry"` | Always `"geometry"` |

---

## Edge element (connector)

```xml
<mxCell
  id="5"
  value="Label"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;"
  edge="1"
  source="2"
  target="3"
  parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### `<mxCell>` edge attributes

| Attribute | Required | Type | Description |
| ----------- | ---------- | ------ | ------------- |
| `id` | Yes | string | Unique identifier |
| `value` | Yes | string | Connector label (empty string when there is no label) |
| `style` | Yes | string | Style string (see Edge styles) |
| `edge` | Yes | `"1"` | Must be `"1"` to declare a connector |
| `source` | No | string | Source vertex ID |
| `target` | No | string | Target vertex ID |
| `parent` | Yes | string | Parent cell ID (usually `"1"`) |

### `<mxGeometry>` edge attributes

| Attribute | Required | Type | Description |
| ----------- | ---------- | ------ | ------------- |
| `relative` | No | `"1"` | Always `"1"` for edges |
| `as` | Yes | `"geometry"` | Always `"geometry"` |

### Edge with label offset

```xml
<mxGeometry x="-0.1" y="10" relative="1" as="geometry">
  <mxPoint as="offset" />
</mxGeometry>
```

In relative geometry, `x` moves the label along the edge (-1 to 1). `y` is the perpendicular offset in px.

### Edge with manual waypoints (control points)

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points">
    <mxPoint x="340" y="80" />
    <mxPoint x="340" y="200" />
  </Array>
</mxGeometry>
```

---

## Multipage diagrams

```xml
<mxfile>
  <diagram id="page-1" name="Overview">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
  <diagram id="page-2" name="Details">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
</mxfile>
```

Each `<diagram>` is a separate page/tab. Cell IDs are scoped to their own `<diagram>`. The same ID value can appear on different pages without conflict.

---

## Layer cells

Layers replace the default layer `id="1"`. Cells are assigned to a layer through `parent`:

```xml
<mxCell id="0" />
<mxCell id="1" value="Background" parent="0" />        <!-- layer 1 -->
<mxCell id="layer2" value="Services" parent="0" />         <!-- layer 2 -->
<mxCell id="layer3" value="Connectors" parent="0" />       <!-- layer 3 -->

<!-- Assign the layer through the parent attribute -->
<mxCell id="10" value="API" ... parent="layer2">
  <mxGeometry ... />
</mxCell>
```

Toggle layer visibility:

```xml
<mxCell id="layer2" value="Services" parent="0" visible="0" />
```

---

## Lane container (`swimlane`)

```xml
<!-- Lane container (swimlane) -->
<mxCell id="swim1" value="Process" style="shape=pool;startSize=30;horizontal=1;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="800" height="340" as="geometry" />
</mxCell>

<!-- Lane 1 (child of the swimlane container) -->
<mxCell id="lane1" value="Client" style="swimlane;startSize=30;"
        vertex="1" parent="swim1">
  <mxGeometry x="0" y="30" width="800" height="150" as="geometry" />
</mxCell>

<!-- Shape within the lane (child of the lane) -->
<mxCell id="step1" value="Place order" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="lane1">
  <mxGeometry x="80" y="50" width="120" height="60" as="geometry" />
</mxCell>
```

> **Important**: cells within a lane (`swimlane`) have `parent` set to the **lane ID**, not `"1"`.
> Coordinates within lanes are **relative to the lane origin**.

---

## Group cells

```xml
<!-- Invisible group container -->
<mxCell id="group1" value="" style="group;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry" />
</mxCell>

<!-- Children relative to the group origin -->
<mxCell id="child1" value="A" style="rounded=1;" vertex="1" parent="group1">
  <mxGeometry x="20" y="20" width="100" height="60" as="geometry" />
</mxCell>
```

---

## HTML labels

When the style contains `html=1`, `value` can contain HTML:

```xml
<mxCell value="&lt;b&gt;OrderService&lt;/b&gt;&lt;br&gt;&lt;i&gt;:8080&lt;/i&gt;"
        style="rounded=1;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
</mxCell>
```

HTML must use XML escaping:

- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`

Common supported HTML tags: `<b>`, `<i>`, `<u>`, `<br>`, `<font color="#hex">`, `<span style="...">`, `<hr/>`

---

## Tooltip / Metadata

```xml
<mxCell value="Service name" tooltip="Processes orders" style="..." vertex="1" parent="1">
  <mxGeometry ... />
</mxCell>
```

---

## ID generation rules

| Rule | Detail |
| ------ | -------- |
| IDs `0` and `1` | Reserved, always the root and default layer |
| All other IDs | Must be unique within their `<diagram>` |
| Safe pattern | Sequential integers starting at `2` or UUID strings |
| Across pages | IDs do not need to be unique across different `<diagram>` pages |

**Safe sequential ID example:**

```text
id="2", id="3", id="4", ...
```

**UUID-style example:**

```text
id="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

---

## Coordinate system

- The origin `(0, 0)` is at the **top-left corner** of the canvas
- `x` increases **to the right**
- `y` increases **downward**
- All units are in **pixels**

---

## Recommended spacing

| Context | Value |
| --------- | ------- |
| Minimum space between shapes | `40px` |
| Comfortable spacing | `80px` |
| Lane (`swimlane`) inner padding | `20px` |
| Page edge margin | `40px` |
| Connector routing clearance | `10px` |

---

## Minimal valid `.drawio` file

```xml
<mxfile host="Electron" modified="2026-03-25T00:00:00.000Z" version="26.0.0">
  <diagram id="main" name="Page-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## Validation rules

### Required

- [ ] Cells `id="0"` and `id="1"` are always present as the first two children of `<root>`
- [ ] No other cell uses `id="0"` or `id="1"`
- [ ] All `id` values are unique within each `<diagram>`
- [ ] Every `<mxCell>` has exactly one `<mxGeometry>` child
- [ ] `<mxGeometry>` has the `as="geometry"` attribute
- [ ] Vertex cells have `vertex="1"`; edge cells have `edge="1"`
- [ ] Edge `source`/`target` IDs reference existing vertex IDs in the same diagram
- [ ] Children of a lane (`swimlane`) have `parent` set to the lane ID, not `"1"`
- [ ] HTML in `value` attributes uses XML escaping

### Recommended

- [ ] Shapes do not overlap unless intentional (use spacing ≥40 px)
- [ ] Edge labels are short (≤4 words)
- [ ] Layer cells have descriptive names in `value`
- [ ] All shapes fit within the `pageWidth` × `pageHeight` boundaries
