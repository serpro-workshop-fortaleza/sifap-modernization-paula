---
description: "Use when creating frontend UI components, pages, client interactions, component state, accessibility, and user-facing workflows."
applyTo: "frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**"
---

# Frontend conventions - Component construction and interaction

This file activates when you create UI in `frontend/app/**` or `frontend/components/**`. It focuses on component construction, client interaction, component state, accessibility implementation, and user-facing workflows. It governs component behavior; [`frontend-spec.instructions.md`](frontend-spec.instructions.md) governs the platform contract for Next.js 15 App Router, strict TypeScript, Tailwind/shadcn styling, Server Components, and Server Actions. Follow that file for those topics and do not repeat them here.

> [!NOTE]
> `frontend/` does not exist yet; the team scaffolds it in Stage 3. These are the conventions components must follow from their creation.

## Component construction

Create small, single-responsibility components with named exports and typed props. Prefer composition over a growing list of props and keep presentational components free of data fetching.

```tsx
import type { ResourceDto } from '@/types/resource';

export function ResourceCard({ resource }: { resource: ResourceDto }) {
  return (
    <article className="rounded-lg border p-4">
      <h3 className="font-semibold">{resource.label}</h3>
      <p className="text-muted-foreground">{formatBRL(resource.amount)}</p>
    </article>
  );
}
```

Keep the `'use client'` surface as small as possible: a Server Component fetches data and passes it to a small Client Component that handles interaction (see [`frontend-spec.instructions.md`](frontend-spec.instructions.md)).

## Component state

Use local `useState` by default. Lift state to the nearest common ancestor when siblings need to share it. Use Context **only** for genuinely shared client state and add a state management library only with an ADR justifying the dependency.

```tsx
'use client';

import { useState } from 'react';

export function ResourceFilter({ onFilter }: { onFilter: (term: string) => void }) {
  const [term, setTerm] = useState('');
  return (
    <label className="flex flex-col gap-1">
      <span>Filter resources</span>
      <input
        value={term}
        onChange={(event) => { setTerm(event.target.value); onFilter(event.target.value); }}
      />
    </label>
  );
}
```

Inputs are controlled (`value` + `onChange`). Derive values during rendering instead of mirroring props in state.

## Client interaction and asynchronous workflows

Mutations go through server actions, not client-side `fetch` (see [`frontend-spec.instructions.md`](frontend-spec.instructions.md)). Wrap the call in `useTransition` to control disabled/pending state and reflect it with `aria-busy`.

```tsx
'use client';

import { useTransition } from 'react';
import { Button } from '@/components/ui/button';

export function ArchiveButton({ id, onArchive }: { id: string; onArchive: (id: string) => Promise<void> }) {
  const [isPending, startTransition] = useTransition();
  return (
    <Button
      type="button"
      disabled={isPending}
      aria-busy={isPending}
      onClick={() => startTransition(() => onArchive(id))}
    >
      {isPending ? 'Archiving…' : 'Archive'}
    </Button>
  );
}
```

## User-facing workflows

Every asynchronous screen renders three explicit states, **loading**, **empty**, and **error**, never a blank screen. Confirm destructive actions and format amounts and dates with an explicit locale so output is deterministic.

```tsx
if (isLoading) return <Spinner aria-label="Loading resources" />;
if (resources.length === 0) return <EmptyState message="No resources yet" />;
if (error) return <ErrorState onRetry={refetch} />;
```

## Accessibility (WCAG 2.1 AA)

| Requirement | How to meet it |
|---|---|
| Labels | Every input has `<label htmlFor>` or `aria-label` |
| Keyboard | All interactive elements can be reached and operated with Tab/Enter/Space |
| Focus | Move focus into the dialog on opening and return it to the trigger on closing |
| Contrast | Text ≥ 4.5:1, large text ≥ 3:1 |
| Structure | One `<h1>` per page, logical heading order, and landmarks |
| Color | Never the only cue; combine it with text or an icon |

Use semantic elements (`<button>`, `<nav>`, `<table>`) before reaching for ARIA; add ARIA only when native semantics are missing.

## Conventions

| Rule | Rationale |
|---|---|
| Named exports for components | Consistent imports compatible with tree shaking |
| Typed props, no `any` | Failures surface at compile time |
| Local `useState`, Context only when shared | Minimal, predictable state graph |
| Colocate the test with the component | Behavior and coverage stay together |
| Explicit loading/empty/error states | No dead ends in the UI |

## Do / Don't

| Do | Don't |
|---|---|
| Push `'use client'` to the smallest leaf | Mark an entire page with `'use client'` |
| Mutate through a server action | Use `fetch` for a client-side mutation |
| Label every control | Use placeholder text as a label |
| Format amounts/dates with a locale | Render raw numbers or ISO strings for users |

## PR Checklist

- [ ] Components use named exports and fully typed props
- [ ] `'use client'` is restricted to the smallest interactive component
- [ ] Shared state uses Context only when justified; no unapproved state library is present
- [ ] Asynchronous screens render loading, empty, and error states
- [ ] Inputs have labels, work with a keyboard, and meet AA contrast
- [ ] A colocated Testing Library test covers the interaction (see [`tests.instructions.md`](tests.instructions.md))
