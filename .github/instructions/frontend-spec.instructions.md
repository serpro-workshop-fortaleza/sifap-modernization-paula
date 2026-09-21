---
description: "Use when implementing or reviewing Next.js 15 App Router, TypeScript, Tailwind CSS, shadcn/ui, and server components in frontend/."
applyTo: "frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**,frontend/**/*.ts,frontend/**/*.tsx"
---

# Frontend specification - Next.js 15 + TypeScript

This file activates when working with TypeScript, TSX, App Router routes, or reusable components in `frontend/`. It teaches the platform contract for the modernized SIFAP (Payment Oversight and Administration System): Next.js 15 App Router, Server Components, Server Actions, strict TypeScript, Tailwind CSS, shadcn/ui, accessibility baseline, and Vitest integration. It governs the framework, typing, styling, and server/client boundaries; [`frontend.instructions.md`](frontend.instructions.md) governs component construction, client interaction details, state coordination, accessibility implementation, and user-facing workflows.

## Stack summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | Next.js (App Router) | 15 |
| Language | TypeScript (strict mode) | 5+ |
| Styling | Tailwind CSS | 3.4+ |
| Components | shadcn/ui | Latest |
| State (client) | React `useState` and Context when needed | Native |
| Server data | Server Components and Server Actions | Native |
| Tests | Vitest + Testing Library | Latest |

## App Router patterns

### Server Components (default)

Every component is a Server Component unless explicitly marked otherwise. Server Components:

- Run on the server and never send JS to the client
- Can use `await` directly to fetch data
- Cannot use hooks, event handlers, or browser APIs

```tsx
// app/<resource>/page.tsx - Server Component (default)
export default async function ResourcePage() {
  const response = await fetch('/api/v1/<resource>');
  if (!response.ok) throw new Error('Failed to load the resource');
  const resources = await response.json();
  return <ResourceList resources={resources} />;
}
```

### Client Components

Add `'use client'` only when interactivity is needed:

```tsx
'use client';

import { useState } from 'react';

export function ResourceFilter({ onFilter }: { onFilter: (term: string) => void }) {
  const [term, setTerm] = useState('');
  return (
    <input
      value={term}
      onChange={e => { setTerm(e.target.value); onFilter(e.target.value); }}
      placeholder="Filter resources..."
    />
  );
}
```

Rules:

- **Reduce the `'use client'` surface**: push interactivity into the smallest possible component. A page that fetches data MUST be a Server Component; only the interactive filter/form inside it MUST be a Client Component.
- **NEVER expose secrets in client components**: API keys, tokens, and internal URLs MUST stay on the server.
- **Avoid state dependencies by default**: use local `useState` and Context for shared client state. Add a state or cache library only with an ADR justifying the dependency.

### Server Actions for mutations

Use server actions instead of API route handlers for form submissions:

```tsx
// app/<resource>/actions.ts
'use server';

export async function createResource(formData: FormData) {
  const value = formData.get('value');
  // Validate and call the backend API
  const res = await fetch(`${process.env.API_URL}/api/v1/<resource>`, {
    method: 'POST',
    body: JSON.stringify({ value }),
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) throw new Error('Failed to create the resource');
}
```

## TypeScript conventions

- **`strict: true`** in `tsconfig.json`: no exceptions and no `// @ts-ignore`
- **No `any`**: use `unknown` and narrow it with type guards
- **Named exports only in reusable components**: `export function ResourceCard()`. App Router route files may use the `export default` required by Next.js.
- **Interface over type** for extensible object shapes
- **Utility types**: use `Pick`, `Omit`, and `Partial` instead of duplicating interfaces

```tsx
// Correct: named export and typed props
export function ResourceCard({ resource }: { resource: ResourceDto }) {
  return <div>{resource.label}</div>;
}

// Wrong: default export and any type
export default function ResourceCard({ resource }: { resource: any }) { ... }
```

## Tailwind CSS + shadcn/ui

- Use Tailwind utility classes directly; do not create separate CSS files unless essential
- Use shadcn/ui components for standard UI elements (Button, Card, Table, Dialog, etc.)
- When the team defines design system tokens, use them for colors and spacing
- Responsive by default: mobile-first with `sm:`, `md:`, and `lg:` breakpoints

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function ResourceSummary({ total }: { total: number }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Resource summary</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-2xl font-bold">{total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</p>
      </CardContent>
    </Card>
  );
}
```

## Accessibility baseline

Every page and component MUST meet these minimum requirements:

- All images have `alt` text
- Form inputs have associated `<label>` elements
- Interactive elements are keyboard navigable
- Color is not the only means of conveying information
- The page has a single `<h1>`, and headings follow a logical order

## Testing with Vitest

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ResourceCard } from './ResourceCard';

describe('ResourceCard', () => {
  it('displays the resource label when a resource is provided', () => {
    render(<ResourceCard resource={{ label: 'Example' }} />);
    expect(screen.getByText('Example')).toBeInTheDocument();
  });
});
```

Test name: `should_[expected behavior]_when_[condition]` or `displays [what] when [condition]`.

## Conventions

| Rule | Rationale |
|---|---|
| Next.js 15 App Router with Server Components by default | Reduces client JavaScript and keeps data access on the server |
| `strict: true`, no `any`, and no `// @ts-ignore` | Type errors surface before execution |
| Named exports in reusable components | Consistent imports; route files retain required defaults |
| Server Actions for mutations | Forms mutate through a server boundary |
| Tailwind CSS and shadcn/ui for UI | Avoids ad hoc styling stacks and keeps components consistent |
| Vitest + Testing Library with behavior-focused names | Tests describe visible behavior and expected conditions |

## Do / Don't

| Do | Don't |
|---|---|
| Use named exports in component files | Use `export default` in reusable components |
| Use `unknown` with type guards | Use `any` or suppress strict TypeScript |
| Use `async`/`await` in asynchronous workflows | Chain `.then()` calls |
| Style with Tailwind and shadcn/ui | Add CSS modules or styled-components |
| Fetch directly with `await` in Server Components | Add client-side data fetching to Server Components |
| Keep secrets on the server | Put secrets in `'use client'` files or `NEXT_PUBLIC_` variables |

## PR Checklist

- [ ] `tsconfig.json` remains strict; no `any` or `// @ts-ignore` was added
- [ ] Server Components remain the default, and `'use client'` appears only where interaction requires it
- [ ] Mutations use Server Actions and validate data before calling the backend API
- [ ] Reusable components use named exports; route files use defaults only when Next.js requires them
- [ ] Styling uses Tailwind utilities and shadcn/ui components without a new styling dependency
- [ ] The accessibility baseline is covered: labels, keyboard operation, heading order, and cues beyond color
- [ ] Vitest + Testing Library tests cover changed behavior with the agreed naming pattern
