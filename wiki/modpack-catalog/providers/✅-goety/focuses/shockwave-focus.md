# Goety 3.1.4 — `shockwave_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `shockwave_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 86/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
- **Aquisição documental:** o JAR exato contém receita base de aquisição homônima para este Focus e sem condition de mod carregado; o conjunto tem 80 recipes de tipo `goety:ritual` e 43 shaped. **O tipo específico desta receita não é deduzido apenas pela lista agregada.** A execução real com recursos/progressão do modpack não foi comprovada nesta etapa.
- **Conta semântica:** `COUNTED_EXACT`, já incluída nos 123 Focuses Goety do ledger; materializar a ficha **não acrescenta uma nova identidade**. Receitas alternativas de obtenção não criam outros spells.
- **Escola/categoria exata, classe e método runtime, cast-time, Soul Energy, cooldown, alcance, dano, efeitos, targeting, PVP/proteção, progressão/research e numeric balance:** **NÃO VERIFICADO nesta ficha**. A identificação factual do item não estabelece automaticamente contrato de API/efeito.

## Authority e deduplicação

Goety é a autoridade de Soul Energy, Focus/Staff casting, custos, recipe execution, servants, cleanup e estado persistente. Black Arcana não cria outro Soul ledger, uma segunda conjuração, um débito adicional, novo summon ou uma segunda world mutation; quaisquer bridges futuras exigem boundary server-safe comprovada e comportamento fail-closed.

## Evidência

- [Inventário semântico exato 3.1.4](../EXACT-3.1.4-SEMANTIC-INVENTORY.md): lista de **123** nomes `_focus` ativos, com `empty_focus` excluído e aquisição agregada 80/43.
- [Auditoria do artefato](../EXACT-3.1.4-ARTIFACT-AUDIT.md): hash físico verificado e exclusões.
- [Fronteira de integração](../INTEGRATION-RULES.md) e [catálogo anterior](../FOCUS-CATALOG.md).

**Clean-room:** a ficha contém dados factuais de identidade e proveniência, não código, assets, tradução de tooltip ou implementação upstream.

## Auditoria de área, dano e orçamento para perks — fonte adjacente Goety 3.1.1 (26/10/2026)

**Autoridade da evidência:** `shockwave_focus` tem identidade/receita no inventário do JAR **Goety 3.1.4** com SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`. Os comportamentos abaixo se limitam ao source **3.1.1** em [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). **Não é equivalência com bytecode, valores físicos ou API 3.1.4**; testes reais não realizados. `SOURCE_ADJACENT_311 / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED`.

**Descrição funcional da fonte 3.1.1:** conjuração de impacto mágico em torno do caster, com feedback visual em área e entrega de dano por `MobUtil.explosionDamage`/`SpellExplosion`. A seleção dos alvos pertence a esse consumer; partículas não são hits.

### Fontes e cadeia de execução em 3.1.1

- [`ModItems.SHOCKWAVE_FOCUS` — linha 311](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L311) liga o Focus a `new MagicFocus(new ShockwaveSpell())` na revisão pública; a classe binária do JAR instalado continua pendente.
- [`ShockwaveSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/ShockwaveSpell.java): `defaultStats().setRadius(4.0D)`, `acceptedEnchantments` com `POTENCY/RADIUS`, `SpellResult(ServerLevel,LivingEntity,ItemStack,SpellStat)`.
- [`SpellConfig.java` — linhas 1881–1892](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1881-L1892): **defaults 3.1.1** `shockwaveCost=80`, `shockwaveTime=0`, `shockwaveCoolDown=80`, `shockwaveMinDamage=5.0` e `shockwaveMaxDamage=24.0`. Mínimo e máximo são configurações independentes, sem evidência aqui de cross-validation.
- [`MobUtil.explosionDamage`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MobUtil.java#L799-L806) instancia [`SpellExplosion.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/SpellExplosion.java), que seleciona AABB, filtra allies/owner/itens e pode causar dano e knockback; [`RandomUtil.nextInt`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/RandomUtil.java) normaliza argumento não positivo antes de gerar inteiro.

### Matriz de perks, targeting e custo

| Eixo | Fato demonstrado somente em source 3.1.1 | Gate real |
|---|---|---|
| Geometria/dimensão | `SpellStat.radius=4.0` é convertido por `(int)` antes do cast, com acréscimo de `RADIUS` se Focus encantado. `SpellExplosion.explosionRangeEntities` usa **AABB** (não esfera de seleção pura) com extensão baseada no raio. | O consumidor calcula distância/exposição posteriormente; não reportar área circular final só com base na AABB ou nas partículas. |
| Config de raio | `SpellExplosion` admite `SpellExplosionDouble`, que dobra o raio de seleção/normalização; o feedback visual em `ShockwaveSpell` recebe raio anterior. | **Pode haver divergência entre raio visual e dano** na fonte 3.1.1; config do modpack e código 3.1.4 desconhecidos. |
| Targeting/dano | `MobUtil.explosionDamage` usa `DamageSource.indirectMagic(caster,caster)`; `SpellExplosion` percorre entidades, calcula distância/exposição, exclui `ItemEntity`, allies e source conforme condições e tenta `hurt`/push. | Não confundir entidade incluída na AABB com hit efetivo; áreas protegidas, cancelamentos, resistências e tipo final de dano precisam QA. |
| Valor de dano | `damage=ShockwaveDamage × WandUtil.damageMultiply + potency`, `maxDamage=ShockwaveMaxDamage × WandUtil.damageMultiply + potency`; `trueDamage=Mth.clamp(damage+RandomUtil.nextInt(random,(int)(maxDamage-damage)),damage,maxDamage)`. | **MaxDamage não é necessariamente valor amostrado inclusivo**: `nextInt` usa limite exclusivo. Se os fatores/valores forem inválidos ou invertidos, o clamp e fallback exigem caso de teste. Não afirmar dano físico 5–24 em 3.1.4. |
| Projétil/cast | `ShockwaveSpell.SpellResult` não cria um projétil separado no corpo inspecionado; uma chamada a `MobUtil.explosionDamage` executa a rotina de área. | N/A para tamanho/velocidade de projétil nesse corpo 3.1.1; addons podem alterar o pipeline. Um cast ≠ número de entidades atingidas. |
| Work budget | Dois loops inteiros de `-radius` a `radius-1` produzem **4 × radius²** posições verificadas no corpo de partículas (para radius positivo), antes do efeito de explosão. | `radius` maior aumenta custo quadraticamente; cap/limites de 3.1.4 e desempenho real precisam ser medidos. Aumentar AOE por perk sem budget explícito fica bloqueado. |
| Cooldown e custo | `defaultSoulCost`, `defaultCastDuration` e `defaultSpellCooldown` consultam config com defaults 80/0/80 na versão pública. | O `DarkWand/SEHelper` mantém débito/cooldown provider-owned. Desconto, cast instantâneo e mínimo de ticks exigem contrato efetivo e verificação. |
| Destruição do mundo | As classes `ShockwaveSpell`/`SpellExplosion` inspecionadas descrevem dano/knockback e feedback, sem alteração explícita de blocos nesses corpos. | **Não equivale a provar** segurança de todos os listeners, claims ou addon side effects. Não antecipar `WorldEffectPolicy` do Black Arcana. |

### Decisões de integração

Perks potenciais: potência, raio, queda de dano, cap de alvos, cooldown e custo. São **eixos de design**, sem autorização de alterar `SpellStat`, `SpellExplosionDouble` ou produção de partículas da versão instalada. Um adapter que aumente radius deve impor limite de custo em scans, server authority, proteção contra estourar inteiros e equivalência exata de targeting; nenhuma delas está comprovada.

**Causalidade e Mastery:** uma invocação nativa de `shockwave_focus` gera uma rotina de dano possivelmente multi-alvo, não uma conjuração por `hurt` nem por partícula. Proibir double-charge, double-proc, geração de Arcane Danger pelo dano Goety sem contrato causal e contorno de ally filters. **⛔ Mutação fail-closed; ⚠️ documentação source-adjacent somente.**

**Pendência de certificação:** comparar `ShockwaveSpell`/`SpellExplosion`/`RandomUtil`/`SpellConfig` no JAR Goety **3.1.4 SHA-exato**, confirmar configuração física, caps de raio, política de dano/world effects, eventos, entidades com resistência/claims e testes em servidor real/Survival. **Não modificar índices e manifesto; não incrementar o progresso 100%.**

## Adendo de ABI exata do JAR 3.1.4 — 26/10/2026

**Nova evidência, distinta do estudo da fonte 3.1.1 acima:** no JAR `goety-3.1.4.jar` com SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, o [probe de assinaturas e relações de chamadas](../EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md) confirmou os símbolos abaixo (`GitHub Actions run 40344481668`, `success`; artifact `12659699310`).

`ShockwaveSpell.SpellResult` referencia `MobUtil.explosionDamage`, `SpellStat.getRadius` e `WandUtil.damageMultiply`. `ShockwaveSpell.defaultStats` referencia `SpellStat.setRadius`.

**Interpretação estrita:** `EXACT_ABI_CALL_REFERENCES_VERIFIED` cobre apenas classe/método/field e referências estáticas apontadas; **não** confirma ramos executados, fórmulas, balanceamento, configs, eventos efetivos, hooks seguros ou testes físicos. A análise `SOURCE_ADJACENT_311` permanece uma fonte separada; `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED` continuam válidos. Goety mantém autoridade, sem homologação de perks e sem incremento dos contadores globais.
