# Apprentice's Codex 1.0.1.1 — Fire

Artefato físico: `apprentice_codex-1.0.1.1-mc1.21.1.jar` (SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`). Versão declarada: `1.0.1.1`.

Registry Fire observado no `SpellRegistry.java` do artefato: **6/6** no recorte examinado. A contagem é documental e não encerra o universo integral do provider.

| Registry ID | Nome | Nível máx. declarado | Raridade mín. declarada | Cooldown declarado | Cast | Poder declarado | Mana declarada |
|---|---|---:|---|---:|---|---|---|
| `apprenticecodex:thermal_process` | Thermal Process | 3 | Rare | 20.0 s | Continuous | `100 + 150*(n-1)` | `10 + 5*(n-1)` |
| `apprenticecodex:magic_spear` | Magic Spear | 5 | Epic | 0.5 s | Instant | `600 + 300*(n-1)` | `30 + 30*(n-1)` |
| `apprenticecodex:artisan_smash` | Artisan Smash | 3 | Rare | 8.0 s | Long | `900 + 400*(n-1)` | `40 + 20*(n-1)` |
| `apprenticecodex:combustion_jet` | Combustion Jet | 5 | Uncommon | 8.0 s | Instant | `400 + 200*(n-1)` | `30 + 10*(n-1)` |
| `apprenticecodex:catch_flame` | Catch Flame | 8 | Uncommon | 0.5 s | Long | `800 + 75*(n-1)` | `10 + 3*(n-1)` |
| `apprenticecodex:thermal_slice` | Thermal Slice | 5 | Rare | 6.0 s | Long | `500 + 200*(n-1)` | `40 + 10*(n-1)` |

Todos os valores acima são coeficientes/defaults lidos no JAR 1.0.1.1. Mana, cooldown, spell power, nível, raridade e escola efetivos são produzidos por `AbstractSpell`/`SpellConfigManager`, atributos, Curios e eventos do host; permanecem **NÃO VERIFICADOS**.

## Resumo das raízes

- **Thermal Process** — feixe contínuo que combina dano, debuff acumulativo e processamento de itens/receitas com ponte Create provider-owned.
- **Magic Spear** — míssil de mira assistida com disparo alternado, homing limitado e explosão curta no impacto.
- **Artisan Smash** — launcher conjurado que dispara uma shell explosiva com raio escalado por poder e política de aliados própria.
- **Combustion Jet** — onda orientada em movimento com dano único por vítima, queima e recuo manual separado do dano.
- **Catch Flame** — chama de curto alcance que alterna tipo de dano contra alvos em chamas e pode acender blocos sob gates de configuração/permissão.
- **Thermal Slice** — corte com katana conjurada, dash curto e `ThermalSundered` compartilhado com Catch Flame e Thermal Process.

Componentes como entidades, eventos, tipos de dano, efeitos e callbacks pertencem à raiz semântica correspondente; não são contados como magias adicionais. `ThermalSundered` é um efeito compartilhado, não uma sétima raiz.

## Limites

Cada ficha é `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, com `mutating_hook=NOT_VERIFIED`, `mutation=NO_MUTATION`, `physical_qa=NOT_TESTED` e `perk_certification=NOT_CERTIFIED`. Nenhuma homologação de perk, configuração instalada, QA físico, universo integral do provider ou implementação na `main` é afirmada.
