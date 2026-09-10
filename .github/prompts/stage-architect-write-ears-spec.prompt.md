---
name: "write-ears-spec"
description: "Registra requisitos EARS confirmados em spec.md usando as instruções de artefatos SDD e a skill sdd-requirements-engineer, com rastreabilidade obrigatória."
argument-hint: "feature=NNN-feature-name rules=01-archaeology/business-rules-catalog.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /write-ears-spec

## Objetivo

Transformar somente regras confirmadas da Etapa 1 em requisitos EARS formais em `specs/<NNN>-<feature>/spec.md`. Questões em aberto permanecem como perguntas; não preencha requisitos, critérios ou arquitetura por suposição.

## Quando usar

No início da Etapa 2, após a Dupla 2 selecionar a funcionalidade restrita e concluir a transição H1, na branch `spec/<NNN>-<feature>` criada de `develop`.

> [!NOTE]
> Não use para explorar o legado, catalogar questões (`/catalog-mysteries`) ou projetar módulos (`/design-modular-monolith`). Registre somente requisitos com evidências confirmadas.

## Pré-condições

- `01-archaeology/business-rules-catalog.md` contém as evidências
- A equipe identificou `specs/<NNN>-<feature>/`
- A equipe leu cada origem legada citada

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature-name>`
- `rules=01-archaeology/business-rules-catalog.md`
- O subconjunto de regras **Confirmed** pertencente à funcionalidade
- Justificativa `[GREENFIELD]` confirmada para capacidades sem equivalente legado

## O que farei

- Lerei as [instruções de artefatos SDD](../instructions/sdd-artifacts.instructions.md) e carregarei a skill [sdd-requirements-engineer](../skills/sdd-requirements-engineer/SKILL.md) antes da autoria, no modo `Requirements`
- Confirmarei o escopo e registrarei adiamentos em `02-modern-spec/scope-decisions.md`
- Validarei a origem `.NSP`, `.NSN`, `.NSC`, `.NSA`, `.NSL`, `.jcl` ou `.ddm`
- Preservarei REQ-IDs existentes e atribuirei IDs exclusivos aos requisitos novos, com `source_legacy:` e caminho e linhas; usarei `[GREENFIELD]` somente com justificativa fornecida
- Registrarei padrão EARS, fonte `SRC-###`, prioridade justificada, justificativa do comportamento, status e método de verificação planejado conforme o contrato da skill
- Registrarei Dado/Quando/Então somente quando apoiado por evidência ou decisão de escopo
- Preservarei questões não validadas de `mysteries-found.md`, com todos os campos
- Manterei uma matriz de rastreabilidade e aplicarei o modo `Validation` antes da entrega

## O que não farei

- Criar requisito sem `source_legacy:` ou `[GREENFIELD]` justificado
- Promover, responder ou alterar o status de hipóteses e questões
- Exigir quantidade fixa de requisitos, diagramas C4, ADRs ou endpoints
- Migrar implicitamente `specs/` para `.specs/`, trocar o esquema `REQ-NNN` ou gerar um pacote `Full SDD` para esta solicitação de requisitos
- Colocar artefatos Spec-Kit em `02-modern-spec/`
- Inventar fatos de negócio do SIFAP

## Formato da saída

```markdown
### REQ-007 — Título imperativo curto do comportamento

IF <confirmed unwanted condition>, THEN the system SHALL <one observable response>.

- Padrão EARS: Indesejado
- Prioridade: <P0 | P1 | P2 | P3, com justificativa baseada no escopo confirmado>
- Status: Proposed
- Fonte: SRC-001
- Justificativa: <razão apoiada pela regra confirmada>
- source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAMA>.NSN:L<início>-L<fim>
- Verificação planejada: <teste, inspeção, análise, demonstração ou medição; evidência esperada>
- AC-REQ-007-01 — Aceitação (Dado/Quando/Então):
  - Dado <pré-condição apoiada pela evidência>
  - Quando <gatilho>
  - Então <resultado observável e testável>
```

Mantenha no mesmo `spec.md` o registro das fontes e a matriz de rastreabilidade:

| SRC-ID | Tipo de fonte | Evidência primária | Regra confirmada |
|---|---|---|---|
| SRC-001 | Legado | `<caminho completo do programa>:L<início>-L<fim>` | Regra 4 |

| REQ-ID | Padrão EARS | source_legacy | Regra de origem | Arquivo de origem | SRC-ID | AC-ID |
|---|---|---|---|---|---|---|
| REQ-007 | Indesejado | `<PROGRAMA>.NSN:L<início>-L<fim>` | Regra 4 | `business-rules-catalog.md` | SRC-001 | AC-REQ-007-01 |

## Regras de SDD e compatibilidade com o Spec-Kit

- As instruções SDD só são carregadas automaticamente para `.specs/**`; leia-as explicitamente neste prompt e aplique as regras de evidência, atomicidade EARS, rastreabilidade e status.
- Preserve `specs/<NNN>-<feature>/spec.md` e o esquema `REQ-NNN` do [fluxo Spec-Kit do kit](../../09-cheat-sheets/spec-kit-workflow.md). O contrato de dez artefatos em maiúsculas é específico de `.specs/`, não uma autorização para substituir as convenções existentes.
- Use `SHALL` nas cláusulas normativas conforme a skill. Preserve significado e IDs ao normalizar requisitos existentes. `SRC-###` complementa, mas nunca substitui, `source_legacy:`.
- Não invente prioridade, métrica, aprovação ou resultado de teste para completar o modelo. Campos sem evidência ficam `PENDING` ou `BLOCKED`, com impacto e responsável registrados; requisitos bloqueados não são apresentados como prontos.
- Carregue somente os recursos necessários ao modo selecionado. Não presuma que geradores e validadores citados pela skill existem neste repositório ou se aplicam ao Spec-Kit; registre portões não executados e o motivo.

## Definição de pronto

- [ ] As instruções SDD e a skill foram lidas e aplicadas nos modos `Requirements` e `Validation`
- [ ] `spec.md` contém somente requisitos da funcionalidade
- [ ] Cada requisito tem uma resposta EARS observável com `SHALL`, os metadados da skill, critério com ID estável e `source_legacy:` válido ou `[GREENFIELD]` justificado
- [ ] Questões em aberto permanecem fora dos requisitos e sem mudança de status
- [ ] A matriz relaciona cada REQ-ID às evidências revisadas
- [ ] Portões aplicáveis e bloqueios estão registrados; a especificação permanece `Draft` ou `Ready for review` até aprovação humana explícita

## Corpo do prompt

Você é `@architect`. Promova regras confirmadas da Etapa 1 a requisitos EARS formais sem inventar evidências.

**Etapa 0 — Carregar o fluxo SDD.**
Leia as [instruções de artefatos SDD](../instructions/sdd-artifacts.instructions.md) e carregue a skill [sdd-requirements-engineer](../skills/sdd-requirements-engineer/SKILL.md). Se a ferramenta de skills estiver indisponível, leia o `SKILL.md` diretamente. Selecione `Requirements` para este prompt e consulte a [referência EARS](../skills/sdd-requirements-engineer/references/ears-notation.md) e os [portões de qualidade](../skills/sdd-requirements-engineer/references/quality-gates.md). Aplique a compatibilidade com o Spec-Kit definida acima, sem criar artefatos fora do escopo solicitado.

**Etapa 1 — Confirmar o escopo.**
Liste somente linhas **Confirmed** atribuídas pela equipe à funcionalidade. Registre adiamentos em `scope-decisions.md`. Não inclua **Inferred** ou **Mystery**.

**Etapa 2 — Validar cada origem.**
Abra cada membro citado e confirme as linhas. Se a referência falhar, devolva a regra como questão em aberto. Nunca cite `.NSD`; não há esse arquivo no corpus.
Associe cada evidência primária a um `SRC-###` estável e à regra confirmada, mantendo o caminho completo em `source_legacy:`.

**Etapa 3 — Escrever o requisito EARS.**
Preserve IDs existentes e atribua `REQ-NNN` exclusivo aos requisitos novos. Classifique cada requisito em exatamente um dos seis padrões da skill e escreva uma única resposta observável:

- Ubíquo: `The system SHALL <response>.`
- Orientado a evento: `WHEN <event>, the system SHALL <response>.`
- Orientado a estado: `WHILE <state>, the system SHALL <response>.`
- Opcional: `WHERE <feature is present>, the system SHALL <response>.`
- Indesejado: `IF <unwanted condition>, THEN the system SHALL <response>.`
- Complexo: `WHILE <state>, WHEN <event>, the system SHALL <response>.`

Anexe `source_legacy:`. Para capacidade nova, use `[GREENFIELD]` seguido somente da justificativa fornecida pela equipe.
Preencha os demais campos do modelo com evidência; mantenha lacunas explícitas. Um alvo não funcional só pode ser normativo quando sua métrica, carga, janela de observação, ambiente e responsável estiverem definidos.

**Etapa 4 — Registrar critérios.**
Adicione Dado/Quando/Então somente para comportamento apoiado por evidências. Preserve IDs de aceitação existentes; para novos critérios, use `AC-REQ-NNN-NN` e registre método de verificação planejado, sem apresentá-lo como teste executado.

**Etapa 5 — Preservar questões em aberto.**
Copie itens não validados para “Questões em aberto”, preservando evidência `path:line`, impacto, hipótese não confirmada, pessoa responsável e status. Não responda nem altere.

**Etapa 6 — Construir a matriz.**
Mantenha a tabela `REQ-ID | EARS Pattern | source_legacy | Source Rule | Source File | SRC-ID | AC-ID` e o registro de fontes. Verifique a ligação nos dois sentidos entre regra, fonte, requisito e aceitação.

**Etapa 7 — Validar e escrever.**
Aplique o modo `Validation` da skill aos requisitos e os portões pertinentes ao escopo. Registre resultados, lacunas e verificações não executadas. Grave em `specs/<NNN>-<feature>/spec.md` como `Draft` ou `Ready for review`, sem presumir aprovação humana. Não infle o escopo quando faltar tempo.

## Exemplo de chamada

```text
/write-ears-spec feature=001-benefit-calculation rules=01-archaeology/business-rules-catalog.md
```

Espere um `spec.md` com requisitos EARS apoiados por evidências, `source_legacy:`, matriz de rastreabilidade e questões em aberto preservadas.
