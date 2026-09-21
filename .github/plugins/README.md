# Copilot plugins

This directory packages selected Copilot **skills** and **agents**
as named plugins and exposes them through a **local
plugin marketplace**
so they can be declared in
[`.github/copilot/settings.json`](../copilot/settings.json).

## What is here

- Ten plugin directories, each with a `plugin.json` manifest and a `README.md`.
- [`marketplace.json`](marketplace.json) - a local **directory marketplace**
  named `datacorp-mm-team-kit`, listing all ten plugins.

The actual skill and agent content is **not** duplicated here. It is maintained
once at the repository level, in [`.github/skills/`](../skills/) and
[`.github/agents/`](../agents/). Each `plugin.json` references that
shared content with relative paths such as `../../skills/<name>/` and
`../../agents/<name>.agent.md`.

## Two layers, one source of truth

1. **Native discovery (in this repository).** Copilot automatically loads
  all skills in `.github/skills/` and all agents in `.github/agents/`.
  In this repository, these components already work without installing anything.
2. **Plugin packaging (for naming and reuse).** Plugins
  group shared components into thematic collections and publish them
  through the official `marketplace` / `enabledPlugins` mechanism.

## Catalog

| Plugin | Content | Status |
|--------|---------|--------|
| [`arch`](arch/) | - | catalog only (no components in this kit) |
| [`azure-cloud-development`](azure-cloud-development/) | 3 skills | enabled |
| [`chromium-control-canvas`](chromium-control-canvas/) | - | catalog only (no components in this kit) |
| [`context-engineering`](context-engineering/) | 1 skill | enabled |
| [`copilot-sdk`](copilot-sdk/) | 1 skill | enabled |
| [`database-data-management`](database-data-management/) | 2 skills | enabled |
| [`frontend-web-dev`](frontend-web-dev/) | 1 agent, 1 skill | enabled |
| [`java-development`](java-development/) | 4 skills | enabled |
| [`software-engineering-team`](software-engineering-team/) | 1 agent | enabled |
| [`testing-automation`](testing-automation/) | 2 skills | enabled |

These manifests were adapted from the `github/awesome-copilot` marketplace. Of the 48
component references in the original manifests, 16 point to content
present in this kit and were retained; the other 32 point to skills, agents,
or extensions that are not part of this kit and were removed. Each plugin's
README lists exactly what was removed.

## How plugins are enabled

Declarative configuration lives in
[`.github/copilot/settings.json`](../copilot/settings.json):

```json
{
  "extraKnownMarketplaces": {
    "datacorp-mm-team-kit": {
      "source": { "source": "directory", "path": ".github/plugins" }
    }
  },
  "enabledPlugins": {
    "java-development@datacorp-mm-team-kit": true
  }
}
```

- `extraKnownMarketplaces` registers the local directory marketplace. The value
  shape (`{ "source": { "source": "directory", "path": ... } }`) is exactly
  what the CLI writes when you register a directory marketplace.
- `enabledPlugins` keys are plugin **specifications** in the form
  `name@marketplace`, never bare names or filesystem paths.
  Only the eight plugins containing components are enabled; the two
  catalog-only entries are listed in the catalog but are not
  enabled, because enabling them would load nothing.

To register the marketplace on demand from the repository root, use the
CLI-supported command for a directory source (the explicit `./` prefix is
required so the path is not interpreted as a GitHub
`owner/repo` specification):

```bash
copilot plugin marketplace add ./.github/plugins
copilot plugin marketplace browse datacorp-mm-team-kit
```

## Known limitations

- **In this repository, plugins add no new functionality.**
  Everything they reference is already loaded through native discovery of
  `.github/skills/` and `.github/agents/`. The plugin layer serves
  documentation and packaging: it records which shared components
  form each collection and exposes them through the official marketplace mechanism.
- **Installed plugins copy only their own directory.** When a plugin is
  installed from a marketplace, Copilot copies that plugin's directory, not the
  repository root. Because these manifests point to shared content
  **outside** the plugin directory (`../../skills/...`, `../../agents/...`), those
  components are not copied on installation and will not appear in another
  repository or in a global installation. This was verified empirically:
  installing this kind of plugin reports success but includes zero skills.
  To provide a self-contained plugin, the referenced content must be
  bundled in the plugin directory. This kit deliberately does not duplicate that
  content, since it is maintained once at the repository root.
- **Headless `copilot -p` runs did not apply the repository's
  `extraKnownMarketplaces`.** In a non-interactive prompt
  session, only default marketplaces were loaded. Declarative
  settings are documented for interactive and agent sessions; the reliable,
  verified way to register the local marketplace is the
  `copilot plugin marketplace add ./.github/plugins` command above.

## Validation

```bash
# all manifests and configuration files parse as JSON
python3 -c "import json,glob; [json.load(open(f)) for f in \
  glob.glob('.github/plugins/*/plugin.json') + \
  ['.github/copilot/settings.json', '.github/plugins/marketplace.json']]"

# Markdown lint (uses the root .markdownlint-cli2.jsonc file)
npx --yes markdownlint-cli2 ".github/plugins/**/*.md"
```

## References

- Copilot CLI plugins:
  <https://docs.github.com/copilot/concepts/agents/copilot-cli/about-cli-plugins>
- Creating plugins:
  <https://docs.github.com/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating>
- Copilot CLI reference:
  <https://docs.github.com/copilot/how-tos/copilot-cli>
- Original marketplace: <https://github.com/github/awesome-copilot>
