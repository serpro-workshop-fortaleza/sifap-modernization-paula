---
description: "Use when creating, editing, or reviewing draw.io diagrams and mxGraph XML in .drawio, .drawio.svg, or .drawio.png files."
applyTo: "**/*.drawio,**/*.drawio.svg,**/*.drawio.png"
---

# draw.io diagrams - Conventions and constraints

This file activates when you open or edit a `.drawio`, `.drawio.svg`, or `.drawio.png` file. It defines the structure, style, and naming constraints every diagram in this repository must meet to render on the first attempt in VS Code with the `hediet.vscode-drawio` extension and remain consistent throughout the kit. It teaches the invariants a diagram file must maintain, but does not provide step-by-step construction instructions. The authoring procedure, XML recipes by type, templates, and validation script live in the [`draw-io-diagram-generator` skill](../skills/draw-io-diagram-generator/SKILL.md). Read it before generating or restructuring a diagram and do not duplicate its steps here.

## Structural invariants

These invariants are non-negotiable; a diagram violating any of them renders blank or corrupted.

- `id="0"` and `id="1"` are the **first two cells** of every `<diagram>`, in that order, and are never reused for content.
- Every cell `id` is **unique within the diagram page** (IDs may repeat across different pages).
- Every vertex (`vertex="1"`) has a child `<mxGeometry ... as="geometry">` with `x`, `y`, `width`, and `height`.
- Every edge (`edge="1"`) points `source`/`target` to existing vertex IDs **or**, for floating edges such as sequence diagram lifelines, contains `<mxPoint as="sourcePoint">` and `<mxPoint as="targetPoint">` inside `<mxGeometry>`.
- Every cell except `id="0"` has a `parent` that resolves to an existing ID.
- Children of a container (swimlane, table) use coordinates **relative to the parent**, not the canvas.

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <!-- every other cell sets parent to an existing ID -->
</root>
```

> [!WARNING]
> A file that opens blank in VS Code is almost always missing the `id="0"`/`id="1"` root cells or contains an edge whose `source`/`target` ID does not resolve. Check these two invariants first.

## Semantic color palette

Use a single palette throughout the repository so a shape's color always has the same meaning. Pair `fillColor` with its corresponding `strokeColor`.

| Role | fillColor | strokeColor |
|---|---|---|
| Primary / information (default) | `#dae8fc` | `#6c8ebf` |
| Success / start / positive | `#d5e8d4` | `#82b366` |
| Warning / decision | `#fff2cc` | `#d6b656` |
| Error / end / danger | `#f8cecc` | `#b85450` |
| Neutral / interface | `#f5f5f5` | `#666666` |
| External / partner | `#e1d5e7` | `#9673a6` |

## File, naming, and layout conventions

| Aspect | Convention |
|---|---|
| Extension | `.drawio` for versioned diagrams; `.drawio.svg` when embedded in Markdown |
| File name | `kebab-case`, for example, `payment-flow.drawio`, `database-schema.drawio` |
| Location | Beside the code documented by the diagram, in `docs/` or `architecture/` |
| Grid | Align all coordinates to the 10 px grid (values divisible by 10) |
| Spacing | 40–60 px between shapes on the same row; 80–120 px between layer rows |
| Page size | Default landscape A4, `1169 × 827` px |
| Density | At most 40 cells per page; split larger systems into multiple `<diagram>` pages |
| Title | Add a title text cell at the start of each page |

## Validation

Before committing, run the `validate-drawio.py` checker documented in the [`draw-io-diagram-generator` skill](../skills/draw-io-diagram-generator/SKILL.md). Then open the file in VS Code to confirm rendering. The skill owns the exact invocation and troubleshooting table; this file owns the invariants enforced by the checker.

## Conventions

| Rule | Rationale |
|---|---|
| `id="0"` and `id="1"` are the first two cells of each page | draw.io treats them as the reserved root; without them, the file does not render |
| Every vertex style includes `whiteSpace=wrap;html=1` | Labels wrap and render HTML consistently, without overflowing |
| Connectors use `edgeStyle=orthogonalEdgeStyle` | Clean right-angle routing keeps diagrams readable |
| The semantic color palette is used consistently | A color has the same meaning in every diagram |
| Diagram file names use `kebab-case` and live beside the code | Diagrams are easy to find and diff in version control |
| Authoring steps and recipes live in the skill, not here | A single procedure source prevents drift between two copies |

## Do / Don't

| Do | Don't |
|---|---|
| Put `id="0"` and `id="1"` first, followed by content cells | Reuse `0` or `1` for a shape or omit them |
| Point every edge to existing vertex IDs or use floating points | Leave an edge's `source`/`target` dangling |
| Reuse the semantic color palette | Invent ad hoc colors for each diagram |
| Point to the skill for the authoring workflow | Copy the skill's step-by-step recipes into this file |
| Keep child coordinates relative to the container | Use canvas coordinates for cells inside a swimlane |
| Split a dense diagram across pages | Squeeze more than 40 cells into one page |

## PR Checklist

- [ ] `<mxCell id="0" />` and `<mxCell id="1" parent="0" />` are the first two cells of every page
- [ ] All cell IDs are unique within the diagram, and every `parent` resolves
- [ ] Every edge `source`/`target` resolves, or the edge uses `sourcePoint`/`targetPoint`
- [ ] Every vertex has `<mxGeometry as="geometry">`, and container children use relative coordinates
- [ ] The semantic color palette and `whiteSpace=wrap;html=1` vertex style are applied consistently
- [ ] The file uses `kebab-case`, lives in `docs/` or `architecture/`, and has one title cell per page
- [ ] The skill's `validate-drawio.py` checker passes, and the file renders in VS Code
