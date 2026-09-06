# Iron's Spells 'n Spellbooks — índice canônico do provider

- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Runtime:** `1.21.1-3.16.3`
- **Regra desta Wiki:** TODO spell existente recebe um arquivo `.md`, mesmo quando não há alteração planejada pelo Black Arcana. Spells deprecated ainda presentes no provider recebem ficha histórica/semântica, mas não inflam a contagem ativa do catálogo oficial.

## Progresso do catálogo individual

| Escola | Total ativo | Fichas ativas | Estado |
|---|---:|---:|---|
| Blood | 10 | 10 | `COMPLETO` |
| Eldritch | 7 | 7 | `COMPLETO` |
| Ender | 16 | 16 | `COMPLETO` |
| Evocation | 17 | 17 | `COMPLETO` |
| Fire | 13 | 13 | `COMPLETO` |
| Holy | 12 | 12 | `COMPLETO` |
| Ice | 12 | 12 | `COMPLETO` |
| Lightning | 10 | 10 | `COMPLETO` |
| Nature | 13 | 0 | `PENDENTE` |

**Cobertura ativa atual:** 97/110 spells do Iron's base possuem ficha individual canônica.

`COMPLETO` significa que todos os spells ativos da escola possuem ficha e que cada campo obrigatório está resolvido por evidência ou marcado explicitamente `NÃO VERIFICADO`. Não significa que QA visual/client-real ou internals de toda entity/effect tenham sido testados.

### Provenance dos passes Ice + Lightning

O catálogo oficial atual de `https://iron.wiki/spells/` é a authority player-facing para o conjunto ativo e valores publicados. Internals são auditados no commit upstream `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`.

O próprio `gradle.properties` desse commit declara `minecraft_version=1.21.1` e `mod_version=1.21.1-3.16.3`, correspondendo ao JAR instalado. Quando documentação pública e source divergem, ambas são preservadas com sua provenance; comportamento fino não auditado permanece `NÃO VERIFICADO`/provider-native.

### Spells legados/deprecated fora da contagem ativa

- `holy/cloud-of-regeneration.md` — implementação ainda presente no source 3.16.3, `Deprecated=true`, ausente do catálogo ativo. Mantida sem alterar o total ativo de 110.

## Escolas nativas do Iron's base

1. Blood — 10
2. Eldritch — 7
3. Ender — 16
4. Evocation — 17
5. Fire — 13
6. Holy — 12
7. Ice — 12
8. Lightning — 10
9. Nature — 13

**Total ativo: 110 spells.**

## Estrutura física obrigatória

`providers/irons-spells/<escola>/<spell>.md`

Spells de addons permanecem no provider que realmente os registra, mesmo quando usam escola do Iron's.

## Escolas adicionais no modpack

O runtime do stack possui escolas extras fornecidas por addons. Entre as já comprovadas estão Astral, Radiance, Shadow, Cosmic, Aqua, Symmetry, Empty e Sound. A lista total só é fechada a partir de runtime/JARs reais; nenhum nome é inventado para completar contagem.

## Campos obrigatórios por magia

Cada ficha resolve ou marca `NÃO VERIFICADO` para: status/provider/versão/ID/escola; descrição; níveis/raridade; cast/channel; recurso/custo/cooldown; dano/cura/tipo; alcance/área/duração; scaling/caps; targets/PvP/bosses/summons; requisitos/obtenção/aprendizado; itens/focus/rituais; VFX/animação/áudio; bridges; deduplicação; bugs/QA/fail-closed; fonte/evidência.
