# Black Arcana — padrão universal de dossiê técnico para perks, magias e rituais

**Status:** NORMA EDITORIAL DE CATALOGAÇÃO / NÃO É API IMPLEMENTADA.
**Aplicação:** toda ficha `.md` que representa identidade mágica catalogada: spell, glyph (form/effect/augment), ritual, Focus, summon/poder, relíquia ativa ou ação sobrenatural. Índices, inventários, README, auditorias, licenças e relatórios de CI não são *fichas por magia* e continuam sendo fontes/índices, não réplicas de dossiês.

## Objetivo

Permitir ao Codex reconhecer o que cada provider realmente faz e *onde* uma perk pode ler/alterar dados, criar outra magia original ou preservar compatibilidade. A documentação não cria direitos de escrita na API do provider: **um parâmetro identificado no código não é automaticamente interceptável ou mutável**. Usar evidência do JAR/modlist atual, source pin da versão exata e contratos verificados.

## Campos obrigatórios de CADA ficha de objeto mágico

1. **Identidade e versão:** `provider`, `mod_id`, JAR exato, `namespace:id` real ou ID de Focus/glyph, classificação de escola/tipo e `source_sha`/hash quando disponíveis; nome de exibição separado do ID.
2. **Localizadores para o Codex:** URL do arquivo Java no *commit* exato ou classe/member do JAR, pacote/classe, métodos concretos responsáveis pela admissão, seleção de alvo, instância de efeito, dano/cura, conclusão e persistência. Quando não verificados, escrever `NÃO VERIFICADO`.
3. **Casting/execução:** modo de ativação, quem verifica intenção, condição, custo/recurso, cooldown, tempo e lifecycle; diferenciar **default**, configuração efetiva e ações em runtime.
4. **Targeting/geometry:** self/entidade/bloco/posição/área/world, alcance de seleção e de efeito separados, LOS, filtros de alvos/claims/friendly fire, raio, ângulo, profundidade, altura, velocidade, trajetória, quantidade de instâncias/alvos e limites reais.
5. **Resultado:** família funcional, damage source ou estado de cura específico, elemento/escola, DoT, knockback, buff/debuff, status e duração, invocações, efeitos destrutivos, transformação, movimento, loot/ritual, responsabilidade de entity/helper/effect pós-cast.
6. **Scaling e caps:** fórmula literal só quando comprovada, unidade, tick vs segundo, nível, spell power/atributos/config, rounding, hard ceilings, work budgets e risco de multiplicação do número de entidades/targets.
7. **Possibilidades de perks:** **A** atributo nativo comprovado; **B** evento/callback/API oficialmente verificado; **C** wrapper/adapter condicionado a auditoria; **D** sem hook e portanto ⛔ *fail-closed*. Registrar exatamente o que o hook permite, e não aquilo que o designer gostaria de controlar.
8. **Causalidade:** cast → projectile/area/effect → damage/heal/death/summon/ritual completion; token/owner/recast/tick e condições de deduplicação de mastery, procs, cooldown e custos.
9. **Concepção de nova magia:** assinaturas semânticas já ocupadas e possíveis lacunas, sem duplicar magia só por nome/escola/VFX; proposta de magia original não equivale a implementação.
10. **Verificação e pendências:** estado da evidência (wiki/source/JAR exato/integração/GameTest/cliente real), proveniência, blockers e próximos testes.

## Representação mínima por ficha

```yaml
technical_perk_dossier: 1             # esquema editorial, NÃO codec/datapack consumido por mod
source_status: SOURCE_PINNED          # ou BINARY_EXACT / DOC_ONLY / UNVERIFIED
source:
  provider: "<nome real>"
  mod_id: "<real>"
  version: "<da modlist atual>"
  installed_jar: "<real ou NÃO VERIFICADO>"
  sha: "<commit/fingerprint quando comprovado>"
  source_code: "<permalink exato ou NÃO VERIFICADO>"
  implementation_class: "<FQCN real ou NÃO VERIFICADO>"
identity:
  registry_id: "<namespace:id verificado ou tipo de recurso>"
  taxonomy: "<spell|glyph|ritual|focus|summon|ability|system>"
  host: "<Iron's|Ars|Goety|outro real>"
parameters:
  mana_or_resource: "<authority e fórmula/NOT VERIFIED>"
  level: "<valor real ou NOT VERIFIED>"
  targeting: "<alcance de aquisição separado do alcance de impacto>"
  damage_or_heal: "<fórmula/proveniência ou NOT VERIFIED>"
  geometry: "<raio/cone/projéteis/etc, com unidade>"
  duration: "<ticks/segundos, com ownership>"
  scaling_and_caps: "<limites e fórmula evidenciados>"
extension:
  native_attributes: "<comprovados>"
  usable_hook: "<signature real, ou NÃO VERIFICADO>"
  mutation_status: "CONDITIONED"      # opções editoriais ONLY: NATIVE / VERIFIED_HOOK / CONDITIONED / BLOCKED
  progress_authority: "RPG Skill Tree, boundary read-only/contratado"
  casting_authority: "<provider>"
  black_arcana_role: "<own runtime / validated observer>"
  causal_deduplication: "<cast and effect identity>"
qa:
  exact_artifact: "<prova ou pendente>"
  source_logic: "<prova ou pendente>"
  provider_cast_runtime: "PENDING"
  survival_modpack: "PENDING"
```

Esquema acima é **exemplo**, não uma instância preenchida nem uma definição aceitada pelo parser atual de Black Arcana. Não injetar essas chaves nos arquivos de datapack existentes, que têm contratos próprios em `plans/DECISIONS.md`.

## Regras especiais por família

| Família | Objetos de modificação relevantes | Cuidado |
|---|---|---|
| Iron's e addons | `AbstractSpell`, spell registry, `DefaultConfig`, entidades/projéteis/efeitos, eventos reais | `getSpellPower` afeta vários parâmetros correlacionados; nem todo evento aceita alterar área/contagem |
| Ars Nouveau e addons | forma + efeitos + amplificadores; composição, augments permitidos, mana e tier | Glyph não equivale a spell independente; verificar multiplicação, ordem e compatibilidades; não duplicar pipeline |
| Goety | Focus, staff/cast/ritual, Soul Energy, servants e estados nativos | Item/Focus identificado não prova fórmula, nome de classe ou hook; sem inspeção exata, BLOCKED |
| Malum/Eidolon/Hexalia e demais | recipe/ritual/efeito, souls/spirits, blocos, requisitos, lifecycle | Preservar fonte de recurso e efeitos provider-owned; não presumir APIs entre mods |
| Black Arcana próprio | Spell/domain/ritual canônico, WorldEffectPolicy, Corruption/Strain/Arcane Danger | Runtime original com transação/cast única; design e código próprio, caps e testes |
| Reliquified/itens sobrenaturais | AbilityTemplate/item/mode/event, recast/proc | Uma habilidade primária não cria uma segunda identidade semântica por subability/tooltip |

## Estados independentes por objeto

- **Catálogo**: ✅ catalogado, ❌ não catalogado, 🟡 em implementação, ⚠️ parcial/condicionado, ⛔ bloqueado.
- **Fidelidade técnica**: `IDENTITY_ONLY`, `SOURCE_PARAMETERS`, `SOURCE_CAUSALITY`, `EXACT_BINARY`, `PHYSICAL_QA`; não tratar estágios como automaticamente cumulativos.
- **Mutabilidade**: `NATIVE_ATTRIBUTE`, `VERIFIED_EVENT_OR_API`, `CONDITIONED_ADAPTER`, `FAIL_CLOSED`.
- **Testes físicos**: `PENDING` até observação em cliente/servidor/modpack. Um CI verde não é um PASS de Survival.

## Workflow para TODAS as fichas

`latest main -> modlist atual -> provider source/JAR versão exata -> registry -> ficha atual -> class/member -> física/efeitos downstream -> alterações documentais + estado -> diff/teste de cobertura -> PR revisão -> merge após gates`.

Proibido preencher faltas com estimativas silenciosas, copiar implementação/asset upstream sem licença compatível, reutilizar hook de outro provider por analogia, alterar branch compartilhada sem revisão e promover Stage 06.05/07/08 apenas por documentação.

**Autoridades:** [arquitetura](../../../plans/DECISIONS.md), [estado](../../../plans/STATUS.md), [proveniência](../../../SOURCES.md), [inventário atual](CATALOGO-GLOBAL-MAGIAS.md), [RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/tree/main). A [campanha do Iron's no PR #795](https://github.com/Gustavaopere/Black-Arcana/pull/795) é independente e ainda draft.
