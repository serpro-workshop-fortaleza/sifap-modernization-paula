# draw.io shape libraries

Reference guide to all built-in shape libraries. Enable them under `View > Shapes` in the draw.io editor or in the VS Code extension's shapes panel.

---

## Library catalog

### General

**Enable**: always active by default

Common shapes for any diagram type.

| Shape | Style key | Usage |
| ------- | ----------- | --------- |
| Rectangle | *(default)* | Boxes, steps, components |
| Rounded rectangle | `rounded=1;` | Softer process boxes |
| Ellipse | `ellipse;` | States, start/end |
| Triangle | `triangle;` | Arrows, gates |
| Diamond | `rhombus;` | Decisions |
| Hexagon | `shape=hexagon;` | Labels, technical icons |
| Cloud | `shape=cloud;` | Cloud services |
| Cylinder | `shape=cylinder3;` | Databases |
| Note | `shape=note;` | Annotations |
| Document | `shape=document;` | Files |
| Arrow shapes | Various `mxgraph.arrows2.*` | Flow directions |
| Callouts | `shape=callout;` | Speech bubbles |

---

### Flowchart

**Enable**: `View > Shapes > Flowchart`
**Shape prefix**: `mxgraph.flowchart.`

Standard ANSI/ISO flowchart symbols.

| Symbol | Style string | ANSI name |
| -------- | ------------- | ----------- |
| Start / End | `ellipse;` | Terminal |
| Process (rectangle) | `rounded=1;` | Process |
| Decision | `rhombus;` | Decision |
| I/O (parallelogram) | `shape=mxgraph.flowchart.io;` | Data |
| Predefined process | `shape=mxgraph.flowchart.predefined_process;` | Predefined process |
| Manual operation | `shape=mxgraph.flowchart.manual_operation;` | Manual operation |
| Manual input | `shape=mxgraph.flowchart.manual_input;` | Manual input |
| Database | `shape=mxgraph.flowchart.database;` | Direct access storage |
| Document | `shape=mxgraph.flowchart.document;` | Document |
| Multiple documents | `shape=mxgraph.flowchart.multi-document;` | Multiple documents |
| On-page connector | `ellipse;` (small, 30×30) | Connector |
| Off-page connector | `shape=mxgraph.flowchart.off_page_connector;` | Off-page connector |
| Preparation | `shape=mxgraph.flowchart.preparation;` | Preparation |
| Delay | `shape=mxgraph.flowchart.delay;` | Delay |
| Display | `shape=mxgraph.flowchart.display;` | Display |
| Internal storage | `shape=mxgraph.flowchart.internal_storage;` | Internal storage |
| Sort | `shape=mxgraph.flowchart.sort;` | Sort |
| Extract | `shape=mxgraph.flowchart.extract;` | Extract |
| Merge | `shape=mxgraph.flowchart.merge;` | Merge |
| Or | `shape=mxgraph.flowchart.or;` | Or |
| Annotation | `shape=mxgraph.flowchart.annotation;` | Annotation |
| Card | `shape=mxgraph.flowchart.card;` | Punched card |

**Example complete style strings for flowcharts:**

```text
Process:          rounded=1;whiteSpace=wrap;html=1;
Decision:         rhombus;whiteSpace=wrap;html=1;
Start/End:        ellipse;whiteSpace=wrap;html=1;
Database:         shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;
Document:         shape=mxgraph.flowchart.document;whiteSpace=wrap;html=1;
I/O (Data):       shape=mxgraph.flowchart.io;whiteSpace=wrap;html=1;
```

---

### UML

**Enable**: `View > Shapes > UML`

#### Use case diagrams

| Shape | Style string |
| ------- | ------------- |
| Actor | `shape=mxgraph.uml.actor;whiteSpace=wrap;html=1;` |
| Use case (ellipse) | `ellipse;whiteSpace=wrap;html=1;` |
| System boundary | `swimlane;startSize=30;whiteSpace=wrap;html=1;` |

#### Class diagrams

Use lane containers (`swimlane`) for class boxes:

```xml
<!-- Class container -->
<mxCell value="«interface»&#xa;IOrderService"
        style="swimlane;fontStyle=1;align=center;startSize=30;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="200" height="160" as="geometry" />
</mxCell>

<!-- Attributes (children of the class) -->
<mxCell value="+ id: string&#xa;+ status: string"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;overflow=hidden;html=1;"
        vertex="1" parent="classId">
  <mxGeometry y="30" width="200" height="60" as="geometry" />
</mxCell>

<!-- Method separator line -->
<mxCell value="" style="line;strokeWidth=1;fillColor=none;" vertex="1" parent="classId">
  <mxGeometry y="90" width="200" height="10" as="geometry" />
</mxCell>

<!-- Methods (children of the class) -->
<mxCell value="+ create(): Order&#xa;+ cancel(): void"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;overflow=hidden;html=1;"
        vertex="1" parent="classId">
  <mxGeometry y="100" width="200" height="60" as="geometry" />
</mxCell>
```

#### UML relationship arrows

| Relationship | Style string |
| ------------- | ------------- |
| Inheritance (extends) | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=0;` |
| Implementation (implements) | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=block;endFill=0;` |
| Association | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=open;endFill=0;` |
| Dependency | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=open;endFill=0;` |
| Aggregation | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=0;endArrow=none;` |
| Composition | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=1;endArrow=none;` |

#### Component diagram

| Shape | Style string |
| ------- | ------------- |
| Component | `shape=component;align=left;spacingLeft=36;whiteSpace=wrap;html=1;` |
| Interface (lollipop) | `ellipse;whiteSpace=wrap;html=1;aspect=fixed;` (small circle) |
| Port | `shape=mxgraph.uml.port;` |
| Node | `shape=mxgraph.uml.node;whiteSpace=wrap;html=1;` |
| Artifact | `shape=mxgraph.uml.artifact;whiteSpace=wrap;html=1;` |

#### Sequence diagrams

| Shape | Style string |
| ------- | ------------- |
| Actor | `shape=mxgraph.uml.actor;whiteSpace=wrap;html=1;` |
| Lifeline (object) | `shape=umlLifeline;startSize=40;whiteSpace=wrap;html=1;` |
| Activation box | `shape=umlActivation;whiteSpace=wrap;html=1;` |
| Synchronous message | `edgeStyle=elbowEdgeStyle;elbow=vertical;html=1;endArrow=block;endFill=1;` |
| Asynchronous message | `edgeStyle=elbowEdgeStyle;elbow=vertical;html=1;endArrow=open;endFill=0;` |
| Return | `edgeStyle=elbowEdgeStyle;elbow=vertical;dashed=1;html=1;endArrow=open;endFill=0;` |
| Self-call | `edgeStyle=elbowEdgeStyle;elbow=vertical;exitX=1;exitY=0.3;entryX=1;entryY=0.5;html=1;` |

#### State diagrams

| Shape | Style string |
| ------- | ------------- |
| Initial state (solid circle) | `ellipse;html=1;aspect=fixed;fillColor=#000000;strokeColor=#000000;` |
| State | `rounded=1;whiteSpace=wrap;html=1;arcSize=50;` |
| Final state | `shape=doubleEllipse;fillColor=#000000;strokeColor=#000000;` |
| Transition | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=1;` |
| Fork/Join | `shape=mxgraph.uml.fork_or_join;html=1;fillColor=#000000;` |

---

### Entity-relationship (ER diagrams)

**Enable**: `View > Shapes > Entity Relation`

#### Modern ER tables (crow's foot notation)

```xml
<!-- Table container -->
<mxCell id="tbl-orders" value="orders"
        style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="80" width="240" height="210" as="geometry" />
</mxCell>

<!-- Column row -->
<mxCell id="col-id" value=""
        style="shape=tableRow;horizontal=0;startSize=0;swimmilaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
        vertex="1" parent="tbl-orders">
  <mxGeometry y="30" width="240" height="30" as="geometry" />
</mxCell>

<!-- PK marker cell -->
<mxCell value="PK" style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;fontStyle=1;overflow=hidden;"
        vertex="1" parent="col-id">
  <mxGeometry width="40" height="30" as="geometry" />
</mxCell>

<!-- Column name cell -->
<mxCell value="id" style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
        vertex="1" parent="col-id">
  <mxGeometry x="40" width="140" height="30" as="geometry" />
</mxCell>

<!-- Data type cell -->
<mxCell value="UUID" style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontStyle=2;"
        vertex="1" parent="col-id">
  <mxGeometry x="180" width="60" height="30" as="geometry" />
</mxCell>
```

#### ER relationship connectors (crow's foot)

| Cardinality | Style string |
| ------------- | ------------- |
| One-to-one | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERmandOne;startFill=1;endFill=1;` |
| One-to-many | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERmany;startFill=1;endFill=1;` |
| Zero-to-many | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERzeroToMany;startFill=1;endFill=0;` |
| Zero-to-one | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERzeroToOne;startFill=1;endFill=0;` |
| Many-to-many | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmany;endArrow=ERmany;startFill=1;endFill=1;` |

---

### Network / Infrastructure

**Enable**: `View > Shapes > Networking`

| Shape | Style string |
| ------- | ------------- |
| Generic server | `shape=server;html=1;whiteSpace=wrap;` |
| Web server | `shape=mxgraph.network.web_server;` |
| Database server | `shape=mxgraph.network.database;` |
| Laptop | `shape=mxgraph.network.laptop;` |
| Desktop | `shape=mxgraph.network.desktop;` |
| Mobile phone | `shape=mxgraph.network.mobile;` |
| Router | `shape=mxgraph.cisco.routers.router;` |
| Switch | `shape=mxgraph.cisco.switches.workgroup_switch;` |
| Firewall (`firewall`) | `shape=mxgraph.cisco.firewalls.firewall;` |
| Cloud (generic) | `shape=cloud;` |
| Internet | `shape=mxgraph.network.internet;` |
| Load balancer | `shape=mxgraph.network.load_balancer;` |

---

### BPMN 2.0

**Enable**: `View > Shapes > BPMN`
**Shape prefix**: `shape=mxgraph.bpmn.*`

| Shape | Style string |
| ------- | ------------- |
| Start event | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.ellipsePerimeter;symbol=general;verticalLabelPosition=bottom;` |
| End event | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.ellipsePerimeter;symbol=terminate;verticalLabelPosition=bottom;` |
| Task | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rectanglePerimeter;symbol=task;` |
| Exclusive gateway | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rhombusPerimeter;symbol=exclusiveGw;` |
| Parallel gateway | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rhombusPerimeter;symbol=parallelGw;` |
| Subprocess | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rectanglePerimeter;symbol=subProcess;` |
| Sequence flow | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=1;` |
| Message flow | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=block;endFill=0;` |
| Participant group (`Pool`) | `shape=pool;startSize=30;horizontal=1;` |
| Lane | `swimlane;startSize=30;` |

---

### Mockup / Wireframe

**Enable**: `View > Shapes > Mockup`

| Shape | Style string |
| ------- | ------------- |
| Button | `shape=mxgraph.mockup.forms.button;` |
| Input field | `shape=mxgraph.mockup.forms.text1;` |
| Checkbox | `shape=mxgraph.mockup.forms.checkbox;` |
| Dropdown | `shape=mxgraph.mockup.forms.comboBox;` |
| Browser window | `shape=mxgraph.mockup.containers.browser;` |
| Mobile device screen | `shape=mxgraph.mockup.containers.smartphone;` |
| List | `shape=mxgraph.mockup.containers.list;` |
| Table | `shape=mxgraph.mockup.containers.table;` |

---

### Kubernetes

**Enable**: `View > Shapes > Kubernetes`

| Resource | Style string |
| ---------- | ------------- |
| Pod | `shape=mxgraph.kubernetes.pod;` |
| Deployment | `shape=mxgraph.kubernetes.deploy;` |
| Service | `shape=mxgraph.kubernetes.svc;` |
| Ingress | `shape=mxgraph.kubernetes.ing;` |
| ConfigMap | `shape=mxgraph.kubernetes.cm;` |
| Secret | `shape=mxgraph.kubernetes.secret;` |
| PersistentVolume | `shape=mxgraph.kubernetes.pv;` |
| Namespace | `shape=mxgraph.kubernetes.ns;` |
| Node | `shape=mxgraph.kubernetes.node;` |

---

## Enabling libraries in VS Code

Libraries are enabled in the draw.io editor (embedded in VS Code):

1. Open any `.drawio` or `.drawio.svg` file in VS Code
2. Click the `+` icon in the shapes panel (left sidebar) → `Search Shapes` or `More Shapes`
3. Select the library you want to enable
4. Shapes appear in the panel for drag and drop

Libraries are stored per user in draw.io settings (not per project).

---

## Creating a custom shape library

A custom library is an XML file with the `.xml` extension, loaded through `File > Open Library`:

```xml
<mxlibrary>
  [
    {
      "xml": "&lt;mxCell value=\"Component\" style=\"rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;\" vertex=\"1\"&gt;&lt;mxGeometry width=\"120\" height=\"60\" as=\"geometry\" /&gt;&lt;/mxCell&gt;",
      "w": 120,
      "h": 60,
      "aspect": "fixed",
      "title": "My component"
    }
  ]
</mxlibrary>
```

Each shape entry contains:

- `xml`: XML-escaped cell definition
- `w` / `h`: default width/height
- `aspect`: `"fixed"` to lock the aspect ratio
- `title`: name displayed in the panel
