# draw.io style reference

Complete reference for the `style` attribute on `<mxCell>` elements. Styles are semicolon-delimited `key=value` pairs.

---

## Style format

```text
style="key1=value1;key2=value2;key3=value3;"
```

- Keys and values are case-sensitive
- The trailing semicolon is optional but recommended
- Unknown keys are silently ignored
- Missing keys use draw.io defaults

---

## Universal style keys

Apply to all shapes and edges.

| Key | Values | Default | Description |
| ----- | -------- | --------- | ------------- |
| `fillColor` | `#hex` / `none` | `#FFFFFF` | Shape fill color (draw.io default; use the semantic palette in project diagrams) |
| `strokeColor` | `#hex` / `none` | `#000000` | Border/line color (draw.io default; use the semantic palette in project diagrams) |
| `fontColor` | `#hex` | `#000000` | Text color |
| `fontSize` | integer | `11` | Font size in pt |
| `fontStyle` | bitmask (see below) | `0` | Bold/italic/underline |
| `fontFamily` | string | `Helvetica` | Font family name |
| `align` | `left`/`center`/`right` | `center` | Horizontal text alignment |
| `verticalAlign` | `top`/`middle`/`bottom` | `middle` | Vertical text alignment |
| `opacity` | 0–100 | `100` | Shape opacity (%) |
| `shadow` | `0`/`1` | `0` | Drop shadow |
| `dashed` | `0`/`1` | `0` | Dashed border |
| `dashPattern` | for example, `8 8` | — | Custom dash/gap pattern (px) |
| `strokeWidth` | float | `2` | Border/line width in px |
| `spacing` | integer | `2` | Padding around text (px) |
| `spacingTop` | integer | `0` | Top text padding |
| `spacingBottom` | integer | `0` | Bottom text padding |
| `spacingLeft` | integer | `4` | Left text padding |
| `spacingRight` | integer | `4` | Right text padding |
| `html` | `0`/`1` | `0` | Allow HTML in the label |
| `whiteSpace` | `wrap`/`nowrap` | `nowrap` | Text wrapping |
| `overflow` | `visible`/`hidden`/`fill` | `visible` | Text overflow behavior |
| `rotatable` | `0`/`1` | `1` | Allow rotation in the editor |
| `movable` | `0`/`1` | `1` | Allow movement in the editor |
| `resizable` | `0`/`1` | `1` | Allow resizing in the editor |
| `deletable` | `0`/`1` | `1` | Allow deletion in the editor |
| `editable` | `0`/`1` | `1` | Allow label editing in the editor |
| `locked` | `0`/`1` | `0` | Lock all editing |
| `nolabel` | `0`/`1` | `0` | Hide the label entirely |
| `noLabel` | `0`/`1` | `0` | Alias for `nolabel` |
| `labelPosition` | `left`/`center`/`right` | `center` | Horizontal label anchor |
| `verticalLabelPosition` | `top`/`middle`/`bottom` | `middle` | Vertical label anchor |
| `imageAlign` | `left`/`center`/`right` | `center` | Image alignment |

### `fontStyle` bitmask values

| Value | Effect |
| ------- | -------- |
| `0` | Normal |
| `1` | Bold |
| `2` | Italic |
| `4` | Underline |
| `8` | Strikethrough |

Combine by addition: `3` = bold + italic, `5` = bold + underline, `7` = bold + italic + underline.

---

## Shape keys (vertices only)

| Key | Values | Description |
| ----- | -------- | ------------- |
| `shape` | see Shape catalog | Override the default rectangle shape |
| `rounded` | `0`/`1` | Rounded rectangle corners |
| `arcSize` | 0–50 | Corner radius percentage (when `rounded=1`) |
| `perimeter` | function name | Connection perimeter type |
| `aspect` | `fixed` | Lock aspect ratio when resizing |
| `rotation` | float | Rotation in degrees |
| `fixedSize` | `0`/`1` | Prevent automatic sizing when editing the label |
| `container` | `0`/`1` | Treat the shape as a container for children |
| `collapsible` | `0`/`1` | Allow collapse/expand toggle |
| `startSize` | integer | Lane (`swimlane`) or container header size (px) |
| `swimlaneHead` | `0`/`1` | Show lane (`swimlane`) header |
| `swimlaneBody` | `0`/`1` | Show lane (`swimlane`) body |
| `fillOpacity` | 0–100 | Fill-only opacity (independent of `opacity`) |
| `strokeOpacity` | 0–100 | Stroke-only opacity |
| `gradientColor` | `#hex` / `none` | Gradient end color |
| `gradientDirection` | `north`/`south`/`east`/`west` | Gradient direction |
| `sketch` | `0`/`1` | Freehand drawing style |
| `comic` | `0`/`1` | Comic/cartoon line style |
| `glass` | `0`/`1` | Glass reflection effect |

---

## Shape catalog

### Basic shapes

| Shape | Style string | Visual |
| ------- | ------------- | -------- |
| Rectangle (default) | *(no shape key needed)* | □ |
| Rounded rectangle | `rounded=1;` | ▢ |
| Ellipse / Circle | `ellipse;` | ○ |
| Diamond | `rhombus;` | ◇ |
| Triangle | `triangle;` | △ |
| Hexagon | `shape=hexagon;` | ⬡ |
| Pentagon | `shape=mxgraph.basic.pentagon;` | ⬠ |
| Star | `shape=mxgraph.basic.star;` | ★ |
| Cross | `shape=mxgraph.basic.x;` | ✕ |
| Cloud | `shape=cloud;` | ☁ |
| Note / Callout | `shape=note;folded=1;` | 📝 |
| Document | `shape=document;` | 📄 |
| Cylinder (database) | `shape=cylinder3;` | 🗄 |
| Tape | `shape=tape;` | — |
| Parallelogram | `shape=parallelogram;perimeter=parallelogramPerimeter;` | ▱ |

### Flowchart shapes (`mxgraph.flowchart.*`)

| Shape | Style string | Usage |
| ------- | ------------- | ---------- |
| Process | `shape=mxgraph.flowchart.process;` | Standard process |
| Start/End (terminal) | `ellipse;` or `shape=mxgraph.flowchart.terminate;` | Flow start/end |
| Data (I/O) | `shape=mxgraph.flowchart.io;` | Input/Output |
| Decision | `rhombus;` | Yes/No branch |
| Predefined process | `shape=mxgraph.flowchart.predefined_process;` | Subroutine |
| Manual input | `shape=mxgraph.flowchart.manual_input;` | Manual input |
| Manual operation | `shape=mxgraph.flowchart.manual_operation;` | Manual step |
| Database | `shape=mxgraph.flowchart.database;` | Data storage |
| Internal storage | `shape=mxgraph.flowchart.internal_storage;` | Internal data |
| Direct data | `shape=mxgraph.flowchart.direct_data;` | Drum storage |
| Document | `shape=mxgraph.flowchart.document;` | Document |
| Multiple documents | `shape=mxgraph.flowchart.multi-document;` | Multiple documents |
| On-page connector | `ellipse;` (small) | Page connector |
| Off-page connector | `shape=mxgraph.flowchart.off_page_connector;` | Off-page reference |
| Preparation | `shape=mxgraph.flowchart.preparation;` | Initialization |
| Delay | `shape=mxgraph.flowchart.delay;` | Waiting state |
| Display | `shape=mxgraph.flowchart.display;` | Output display |
| Sort | `shape=mxgraph.flowchart.sort;` | Sorting operation |
| Extract | `shape=mxgraph.flowchart.extract;` | Extraction operation |
| Merge | `shape=mxgraph.flowchart.merge;` | Merge paths |
| Or | `shape=mxgraph.flowchart.or;` | OR gate |
| And | `shape=mxgraph.flowchart.and;` | AND gate |
| Annotation | `shape=mxgraph.flowchart.annotation;` | Comment/note |

### UML shapes (`mxgraph.uml.*`)

| Shape | Style string | Usage |
| ------- | ------------- | ---------- |
| Actor | `shape=mxgraph.uml.actor;` | Use case actor |
| Boundary | `shape=mxgraph.uml.boundary;` | System boundary |
| Control | `shape=mxgraph.uml.control;` | Controller object |
| Entity | `shape=mxgraph.uml.entity;` | Entity object |
| Component | `shape=component;` | Component box |
| Package | `shape=mxgraph.uml.package;` | Package |
| Note | `shape=note;` | UML note |
| Lifeline | `shape=umlLifeline;startSize=40;` | Sequence lifeline |
| Activation | `shape=umlActivation;` | Activation box |
| Destroy | `shape=mxgraph.uml.destroy;` | Destruction marker |
| State | `ellipse;` | State node |
| Initial state | `ellipse;fillColor=#000000;` | UML initial state |
| Final state | `shape=doubleEllipse;fillColor=#000000;` | UML final state |
| Fork/Join | `shape=mxgraph.uml.fork_or_join;` | Fork/join bar |

### Network shapes (`mxgraph.network.*`)

| Shape | Style string |
| ------- | ------------- |
| Server | `shape=server;` |
| Database server | `shape=mxgraph.network.database;` |
| Firewall | `shape=mxgraph.cisco.firewalls.firewall;` |
| Router | `shape=mxgraph.cisco.routers.router;` |
| Switch | `shape=mxgraph.cisco.switches.workgroup_switch;` |
| Cloud | `shape=cloud;` |
| Internet | `shape=mxgraph.network.internet;` |
| Laptop | `shape=mxgraph.network.laptop;` |
| Desktop | `shape=mxgraph.network.desktop;` |
| Mobile device | `shape=mxgraph.network.mobile;` |

### AWS shapes (`mxgraph.aws4.*`)

Use the AWS4 library. Common shapes:

| Shape | Style string |
| ------- | ------------- |
| EC2 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;` |
| Lambda | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;` |
| S3 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;` |
| RDS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;` |
| API Gateway | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;` |
| CloudFront | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;` |
| Load Balancer | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elb;` |
| SQS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;` |
| SNS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;` |
| DynamoDB | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;` |
| ECS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;` |
| EKS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;` |
| VPC | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;` |
| Region | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;` |

### Azure shapes (`mxgraph.azure.*`)

| Shape | Style string |
| ------- | ------------- |
| App Service | `shape=mxgraph.azure.app_service;` |
| Function App | `shape=mxgraph.azure.function_apps;` |
| SQL Database | `shape=mxgraph.azure.sql_database;` |
| Blob Storage | `shape=mxgraph.azure.blob_storage;` |
| API Management | `shape=mxgraph.azure.api_management;` |
| Service Bus | `shape=mxgraph.azure.service_bus;` |
| AKS | `shape=mxgraph.azure.aks;` |
| Container Registry | `shape=mxgraph.azure.container_registry_registries;` |

### GCP shapes (`mxgraph.gcp2.*`)

| Shape | Style string |
| ------- | ------------- |
| Cloud Run | `shape=mxgraph.gcp2.cloud_run;` |
| Cloud Functions | `shape=mxgraph.gcp2.cloud_functions;` |
| Cloud SQL | `shape=mxgraph.gcp2.cloud_sql;` |
| Cloud Storage | `shape=mxgraph.gcp2.cloud_storage;` |
| GKE | `shape=mxgraph.gcp2.container_engine;` |
| Pub/Sub | `shape=mxgraph.gcp2.cloud_pubsub;` |
| BigQuery | `shape=mxgraph.gcp2.bigquery;` |

---

## Edge style keys

| Key | Values | Description |
| ----- | -------- | ------------- |
| `edgeStyle` | see below | Connection routing algorithm |
| `rounded` | `0`/`1` | Rounded corners on orthogonal edges |
| `curved` | `0`/`1` | Curved line segments |
| `orthogonal` | `0`/`1` | Force orthogonal routing |
| `jettySize` | `auto`/integer | Source/target projection size |
| `exitX` | 0.0–1.0 | Source exit X point (0=left, 0.5=center, 1=right) |
| `exitY` | 0.0–1.0 | Source exit Y point (0=top, 0.5=center, 1=bottom) |
| `exitDx` | float | Source exit X offset (px) |
| `exitDy` | float | Source exit Y offset (px) |
| `entryX` | 0.0–1.0 | Target entry X point |
| `entryY` | 0.0–1.0 | Target entry Y point |
| `entryDx` | float | Target entry X offset (px) |
| `entryDy` | float | Target entry Y offset (px) |
| `endArrow` | see Arrow types | Arrowhead at the target |
| `startArrow` | see Arrow types | Arrow tail at the source |
| `endFill` | `0`/`1` | Filled end arrowhead |
| `startFill` | `0`/`1` | Filled start arrowhead |
| `endSize` | integer | End arrowhead size (px) |
| `startSize` | integer | Start arrowhead size (px) |
| `labelBackgroundColor` | `#hex`/`none` | Label background fill |
| `labelBorderColor` | `#hex`/`none` | Label border color |

### `edgeStyle` values

| Value | Routing | When to use |
| ------- | --------- | ---------- |
| `none` | Straight line | Simple direct connections |
| `orthogonalEdgeStyle` | Right-angle bends | Flowcharts, architecture |
| `elbowEdgeStyle` | Single elbow | Clean directional diagrams |
| `entityRelationEdgeStyle` | ER-style routing | ER diagrams |
| `segmentEdgeStyle` | Segmented with handles | Fine-tuned routing |
| `isometricEdgeStyle` | Isometric grid | Isometric diagrams |

### Arrow types (`endArrow` / `startArrow`)

| Value | Shape | Usage |
| ------- | ------- | --------- |
| `block` | Filled triangle | Standard directed arrow |
| `open` | Open V tip → | Open/lightweight arrow |
| `classic` | Classic arrow | draw.io default arrow |
| `classicThin` | Thin classic | Compact diagrams |
| `none` | No arrowhead | Undirected lines |
| `oval` | Circular dot | Aggregation start |
| `diamond` | Hollow diamond | Aggregation |
| `diamondThin` | Thin diamond | Narrow diagrams |
| `ERone` | bar `\|` | ER "one" cardinality |
| `ERmany` | Crow's foot | ER "many" cardinality |
| `ERmandOne` | `\|\|` | Mandatory one in ER |
| `ERzeroToOne` | `o\|` | Zero or one in ER |
| `ERzeroToMany` | `o<` | Zero or many in ER |
| `ERoneToMany` | `\|<` | One or many in ER |

---

## Color palette

### Semantic colors (recommended for consistent diagrams)

| Meaning | Fill | Stroke | Usage |
| --------- | ------ | -------- | ------- |
| User / Client | `#dae8fc` | `#6c8ebf` | Browser, client apps |
| Service / Process | `#d5e8d4` | `#82b366` | Server-side services |
| Database / Storage | `#f5f5f5` | `#666666` | Databases, files |
| Decision / Warning | `#fff2cc` | `#d6b656` | Decision nodes, alerts |
| Error / Critical | `#f8cecc` | `#b85450` | Error paths, critical points |
| External / Partner | `#e1d5e7` | `#9673a6` | Third parties, external systems |
| Queue / Async | `#ffe6cc` | `#d79b00` | Message queues |
| Gateway / Proxy (`proxy`) | `#dae8fc` | `#0050ef` | API gateways and proxies (`proxies`) |

### Shapes with dark backgrounds

For dark-themed diagrams, use:

- Fill: `#1e4d78` (dark blue), `#1a4731` (dark green)
- Stroke: `#4aa3df`, `#67ab9f`
- Font: `#ffffff`

---

## Complete style examples

### Rounded blue box

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

### Green process step

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;
```

### Yellow decision diamond

```text
rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;
```

### Red error box

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;
```

### Database cylinder

```text
shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#f5f5f5;strokeColor=#666666;
```

### Lane container (`swimlane`)

```text
shape=pool;startSize=30;horizontal=1;fillColor=#f5f5f5;strokeColor=#999999;
```

### Lane (`swimlane`)

```text
swimlane;startSize=30;fillColor=#ffffff;strokeColor=#999999;
```

### Orthogonal connector

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;
```

### Directed arrow (thick)

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeWidth=2;
```

### Dashed dependency line

```text
edgeStyle=orthogonalEdgeStyle;dashed=1;endArrow=open;endFill=0;strokeColor=#666666;
```

### ER relationship line (one-to-many)

```text
edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;startArrow=ERmandOne;endFill=1;startFill=1;
```

### UML inheritance arrow (hollow triangle)

```text
edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=0;
```

### UML composition (filled diamond)

```text
edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=1;endArrow=none;
```

### UML aggregation (open diamond)

```text
edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=0;endArrow=none;
```

### UML dependency (dashed arrow)

```text
edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=open;endFill=0;
```

### Invisible connector (for alignment)

```text
edgeStyle=none;strokeColor=none;endArrow=none;
```
