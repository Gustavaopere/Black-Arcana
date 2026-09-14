# Wind's Spellbooks 1.0.5 — catálogo observável de spells

Última auditoria: 2026-09-14

## Escopo e autoridade

Este catálogo fecha a superfície **spell-level observável** de `wind_spellbooks` `1.0.5` para NeoForge 1.21.1. A release não possui source público identificado nesta auditoria; por isso este documento não inventaria implementação interna, fórmulas, custos, cooldowns, raridades ou níveis máximos.

Presença/versão no inventário versionado do modpack:

- RPG Skill Tree sibling `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`: `wind_spellbooks` `1.0.5`.
- A modlist física/runtime atual continua sendo autoridade superior quando estiver disponível/versionada; este arquivo não afirma presença física posterior ao snapshot.

Release pública oficial:

- projeto CurseForge: `Wind's Spellbooks : Iron's Spells 'n Spellbooks Addon`, project ID `1519158`;
- arquivo: `wind_spellbooks-1.0.5.jar`;
- loader: NeoForge;
- game version: Minecraft 1.21.1/1.21;
- upload: 2026-07-22;
- file ID observado no metadata público: `8485822`;
- descrição oficial: adiciona uma escola Wind e **7 new upgradable spells**.

## Resultado

Estado: ✅ **Catalogado no escopo observável de registry da versão 1.0.5**.

Resumo fechado:

- **7/7 spell IDs observados** para o namespace `wind_spellbooks`;
- **1 escola própria observada**: `wind_spellbooks:wind`;
- a contagem de sete IDs coincide exatamente com a contagem de sete spells declarada pelo autor da release;
- a evidência de registry está vinculada ao mesmo arquivo público `wind_spellbooks-1.0.5.jar`, e não a uma versão genérica do addon;
- sem source/decompilação do JAR, semântica interna e tuning permanecem fora do escopo.

## 1. Proveniência do artefato observado

Um snapshot runtime público versionado em `Eldodoron/PEAK-dev@b7fb55221e8472f3878a0aa7b4b9d1e05e812961` registra o arquivo:

- `wind_spellbooks-1.0.5.jar`;
- CurseForge project ID `1519158`;
- CurseForge file ID `8485822`;
- release NeoForge para Minecraft 1.21/1.21.1;
- SHA-1 do arquivo no snapshot: `8744886899bc245ae147a44baa2b183689cec7da`.

Isso alinha o dump de registry utilizado abaixo à release pública exata 1.0.5. O SHA-1 é evidência do artefato desse snapshot externo; **não é declarado como hash do JAR físico atual do modpack do usuário**, que não foi fornecido/versionado nesta tranche.

## 2. Como o inventário de spells foi fechado

O mesmo snapshot contém um dump de attributes. Para interpretar as entradas corretamente, foi verificada a documentação pública do mod `Additional Attributes` (`SiverDX/additional_attributes`), que define:

- `additional_attributes:innate_school/<namespace>/<path>` para cada school type de Iron's;
- `additional_attributes:innate_spell/<namespace>/<path>` para cada spell type de Iron's.

Portanto as entradas `additional_attributes:innate_spell/wind_spellbooks/...` são usadas aqui como enumeração derivada dos spell types efetivamente presentes no registry daquele runtime.

## 3. Inventário fechado — 7 spell IDs

O dump alinhado ao JAR 1.0.5 contém exatamente:

| # | Spell ID observado | Estado |
| ---: | --- | --- |
| 1 | `wind_spellbooks:aeropic` | ✅ observado no registry-derived dump |
| 2 | `wind_spellbooks:almighty_push` | ✅ observado no registry-derived dump |
| 3 | `wind_spellbooks:iron_slash` | ✅ observado no registry-derived dump |
| 4 | `wind_spellbooks:tailwind` | ✅ observado no registry-derived dump |
| 5 | `wind_spellbooks:tornado` | ✅ observado no registry-derived dump |
| 6 | `wind_spellbooks:wind_blade` | ✅ observado no registry-derived dump |
| 7 | `wind_spellbooks:wind_jump` | ✅ observado no registry-derived dump |

Nenhum oitavo `innate_spell/wind_spellbooks/...` aparece no dump auditado. A cardinalidade **7** coincide com a descrição oficial da release, que declara sete spells atualizáveis.

## 4. Escola observada

O mesmo dump contém:

- `additional_attributes:innate_school/wind_spellbooks/wind`;
- `wind_spellbooks:wind_spell_power`;
- `wind_spellbooks:wind_magic_resist`.

A escola `wind_spellbooks:wind` também é coerente com a descrição oficial do addon. Este catálogo registra apenas existência/identidade; não infere damage type, focus item, cor, som ou fórmulas sem fonte técnica correspondente.

## 5. Registries auxiliares observados

### Mob effects

O dump de efeitos do mesmo runtime expõe:

- `wind_spellbooks:aeropic`;
- `wind_spellbooks:tailwind`.

Eles não são contados como spells adicionais.

### Entity types

O dump de entity types expõe:

- `wind_spellbooks:aeromancer`;
- `wind_spellbooks:almighty_push`;
- `wind_spellbooks:dash_stop`;
- `wind_spellbooks:iron_slash`;
- `wind_spellbooks:slash_effect`;
- `wind_spellbooks:tornado`;
- `wind_spellbooks:wind_blade`.

A repetição de nomes entre spell IDs e entity IDs é registrada apenas como superfície observável. Sem implementação ou tracing runtime específico, este catálogo **não afirma** que cada entidade seja criada diretamente pelo spell homônimo, nem descreve comportamento interno.

## 6. O que este catálogo não afirma

Para os sete spells, este documento não atribui sem evidência:

- raridade;
- nível mínimo/máximo;
- custo de mana;
- cooldown;
- cast time ou cast type;
- dano, alcance, duração ou scaling;
- efeitos detalhados;
- recipes/loot/progressão;
- compatibilidade provider específica com Black Arcana.

O status ✅ significa que o **inventário definido — IDs spell-level da release 1.0.5 — está fechado**. Ele não transforma ausência de source em conhecimento de implementação.

## 7. Evidência técnica usada

- CurseForge oficial do addon: project ID `1519158`, release `wind_spellbooks-1.0.5.jar`, NeoForge 1.21.1, 2026-07-22; descrição declara escola Wind + sete spells atualizáveis.
- `Eldodoron/PEAK-dev@b7fb55221e8472f3878a0aa7b4b9d1e05e812961`:
  - `minecraft/mods/.index/winds-spellbooks-irons-spells-n-spellbooks-addon.pw.toml` — arquivo exato, project/file IDs e SHA-1;
  - `minecraft/ct_dumps/attribute.txt` — escola e sete spell IDs;
  - `minecraft/ct_dumps/effect.txt` — efeitos auxiliares;
  - `minecraft/ct_dumps/entitytype.txt` — entity types auxiliares.
- `SiverDX/additional_attributes` README — contrato público que explica `innate_school` e `innate_spell` como attributes gerados por school/spell type de Iron's.

## 8. Limite clean-room

Nenhum código, asset ou implementação de Wind's Spellbooks foi copiado ou incorporado ao Black Arcana. O catálogo usa metadata oficial e registries observáveis de um runtime público versionado.

Qualquer integração futura deve confirmar o JAR físico do modpack, hooks reais e semântica de execução antes de criar provider. Na ausência desses contratos, o Black Arcana deve permanecer fail-closed.