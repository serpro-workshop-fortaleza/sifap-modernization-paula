# Massa de dados sintética do legado

> **Trilha:** [Kit do Time](../../README.md) › [Estágio 1](../README.md) › **Massa de dados sintética**

**Os registros que o SIFAP legado processa.** Esta pasta contém os mesmos arquivos de largura fixa carregados no Adabas do laboratório compartilhado, para comparar o comportamento legado com o sistema moderno.

| Campo | Valor |
|---|---|
| **Público-alvo** | Dupla 4 (DBA + QA); a Dupla 3 consome na migração |
| **Pré-requisitos** | Ler os DDMs em [`legacy-sifap/adabas-ddms/`](../legacy-sifap/adabas-ddms/) |
| **Tempo estimado** | 15 min |
| **Estágio** | Estágio 1 — Arqueologia; insumo do Estágio 3 |
| **Resultado esperado** | Registros decodificados para validar o sistema moderno |

> [!IMPORTANT]
> **Dados 100% sintéticos.** Não há dado pessoal real, nenhum CPF ou NIS atribuído a pessoa real e nenhum registro de produção. Os dígitos verificadores são válidos apenas para exercitar os validadores do legado.

---

## Arquivos e volumes

| Arquivo | Registros | Bytes por registro (sem a quebra de linha) | Layout de origem |
|---|---:|---:|---|
| `beneficiary.dat` | 500 | 1739 | `layout-beneficiary.txt`, arquivo 150 BENEFICIARY |
| `payment.dat` | 2000 | 855 | `layout-payment.txt`, arquivo 152 PAYMENT |
| `social-program.dat` | 6 | 361 | `layout-social-program.txt`, arquivo 151 SOCIAL-PROGRAM |
| `audit.dat` | 200 | 4995 | `layout-audit.txt`, arquivo 153 AUDIT |

---

## Regeneração

Execute a partir da raiz do repositório:

```bash
python3 01-archaeology/legacy-seed-data/generate_seed.py
```

O gerador usa apenas a biblioteca padrão do Python 3 e uma semente fixa, portanto a saída é reproduzível byte a byte. Este README também é gerado; traduza o texto dentro de `write_readme()`, nunca só o arquivo.

---

## Notas de layout

Há um registro físico por linha. Campos alfanuméricos são ASCII preenchidos com espaços à direita. Campos numéricos desempacotados são dígitos preenchidos com zeros à esquerda.

> [!WARNING]
> Campos decimais compactados são BCD binário, com a escala declarada no DDM/FDT. **Eles não são legíveis como texto e exigem decodificação antes de qualquer carga no PostgreSQL.** Pelo mesmo motivo, converter identificadores para número descarta os zeros à esquerda de CPF e NIS.

Grupos periódicos e campos MU são emitidos na quantidade máxima de ocorrências, para que os scripts ADACMP/ADALOD carreguem registros determinísticos de largura completa. A quebra de linha não faz parte da largura do registro.

---

## Fixtures didáticas

- Os dígitos verificadores de CPF e NIS usam os algoritmos módulo 11 de [`SUBVALCP.NSN`](../legacy-sifap/natural-programs/SUBVALCP.NSN) e [`SUBVALNI.NSN`](../legacy-sifap/natural-programs/SUBVALNI.NSN).
- Alguns beneficiários têm CPF válido começando com `000`, para o caminho de exceção de teste governamental.
- As rendas familiares cruzam as faixas de cálculo 300, 600, 1000 e 1500.
- Beneficiários da região `99` exercitam o desvio de elegibilidade internacional ou diplomático.
- Os dependentes cobrem nenhum, vários, situações inativa e desligada, e um registro no máximo de 10 ocorrências.
- Os pagamentos incluem estornos, conciliação divergente, retornos bancários e linhas com bruto, desconto e líquido propositalmente desequilibrados para os laboratórios de relatório.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Estágio 1 — Arqueologia](../README.md)<br/><sub>Índice do estágio e seus artefatos.</sub> | [DDMs do Adabas](../legacy-sifap/adabas-ddms/README.md)<br/><sub>Definições de campo que descrevem estes registros.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
