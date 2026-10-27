# Goety 3.1.4 — `electrocute_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `electrocute_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 28/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê técnico — Electro Orb, impacto e ramificações elétricas (27/10/2026)

**Proveniência obrigatória:** `COUNTED_EXACT` e identidade do item pertencem ao **JAR Goety 3.1.4 SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`**; somente os **símbolos e call-sites** listados na [auditoria exata](../EXACT-3.1.4-FIRE-BREATH-FROST-NOVA-ELECTRO-ORB-ABI-20261027.md) são afirmações binárias desta versão (run [`40498956210`](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40498956210), artifact `12731937460`). Todas as fórmulas, estatísticas, defaults, casos condicionais e etapas de execução abaixo são **da fonte adjacente 3.1.1** em [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef), **não verificados como iguais no 3.1.4**. `SOURCE_ADJACENT_311` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

### Cuidado com a identidade do Focus

No [`ModItems.java` público 3.1.1](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L386), o item registrado é **`electrocute_focus`**, mas sua classe de magia é **`ElectroOrbSpell`**; o efeito via entidade é **`ElectroOrb`**. O JAR físico 3.1.4 comprova a identidade `electrocute_focus` e a nova auditoria confirma a existência das classes e referências de métodos `ElectroOrbSpell/ElectroOrb`, **não** a construção item→spell no `ModItems` exato. Não usar o nome de classe como prova automática da associação runtime instalada.

Fontes 3.1.1: [`ElectroOrbSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/storm/ElectroOrbSpell.java), [`ElectroOrb.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/ElectroOrb.java), [`WandUtil.chainLightning`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/WandUtil.java#L179-L230), [`SpellExplosion.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/SpellExplosion.java), [`SpellConfig.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1564-L1572).

### Parâmetros e lifecycle segundo fonte 3.1.1

| Eixo | O que a fonte demonstra | Requisito de integração |
|---|---|---|
| Estatísticas | Escola `STORM`; base `SpellStat.range=32`; aceita `POTENCY`/`RANGE`. Config default `cost=8`, `cast duration=0`, `cooldown=40`, `projectile base damage=4.0`. | Config efetiva e escala em 3.1.4 não foram medidas. Números **não são recomendações de balance**. |
| Aquisição/alvo | `getTarget(caster,range)` tenta selecionar `LivingEntity`; no ramo com target, o vetor inicial deriva do movimento do alvo; sem target, usa `caster.getViewVector`. `new ElectroOrb(world,caster,target)` grava owner e mantém target apenas quando não aliado. | Target, owner, trajetória e previsão não se reduzem a raycast único; requer QA de sem-target, player/PVP, mob e aliado. |
| Disparo | `setExtraDamage(potency)`, `setStaff(rightStaff)`, `shoot(...,0.66F,3.0F)` e `world.addFreshEntity`. | Perk `projectile size` ou multi-shot exige hook no **projétil provider-native** com limites; não duplique uma nova conjuração ou energia. |
| Homing e gravidade | `ElectroOrb.tick` atualiza movimento com `getTargetingVec` se existe target; `getDefaultGravity` muda por presença do target; descarta após `10 segundos` na fonte. | Follow-target/hitbox e lifetime diferentes do range nominal; confirmar alvo removido/morto, reload, dimensão e chunk unload. |
| Impacto | `ElectroOrb.onHit` causa `Entity.hurt` no impacto em entidade e aciona `finalizeExplosion`; fonte de dano `SHOCK`/`indirectShock` quando há owner, adiciona `extraDamage`. | Dano direto != splash/chain; não dar Mastery tripla por um único projétil. |
| Staff: splash e chain | Se `isStaff`, a fonte 3.1.1 cria `SpellExplosion` de raio `2` com callback a `WandUtil.chainLightning`; pode aplicar `SPASMS` após probabilidade base `5%`, acrescida `25 pontos percentuais` quando trovoada com chuva sobre o alvo. | **Não foi auditado o bytecode da inner class anônima**; os números são apenas source-adjacent, não efeitos comprovados na instalação 3.1.4. |
| Cadeia | `WandUtil.chainLightning` na fonte usa até `4 hops`, `8 em trovoada`; filtra alvos com `MobUtil.canAttack` e linha de visão, seleciona candidatos em área, reduz `damage` após cada salto. | Precisam de cap global de alvos, orçamento e autorização de ataque no server; não inferir chain de dano base do nome “Electrocute”. |

### ABI exata 3.1.4: superfícies separadas

- `ElectroOrbSpell.SpellResult` referencia `SpellStat.getRange`, `getTarget`, `ElectroOrb.setPos`, `setExtraDamage`, `setStaff`, `shoot` e `ServerLevel.addFreshEntity`.
- `ElectroOrb.onHit` referencia `Entity.hurt` e `ElectroOrb.finalizeExplosion`; `finalizeExplosion` referencia `isStaff`.
- `ElectroOrb.tick` referencia `getTargetingVec`; `getDefaultGravity` referencia `getTarget`.

**Não comprovado pela ABI:** valores de velocity, homing ativo, bounce/pierce, damage source específico, número de chains, chuva/trovoada, quantidade de efeitos, permissões ou frequência de spawn. O dispatch de `SpellExplosion` anônimo pode impor condições extras; não inventar comportamento efetivo.

**QA pendente:** owner, alvos hostis/amigos, staff e wand comuns, target movendo ou desconectando, partículas versus hits, clima, ordem de choque/splash/chain, raio e budgets, `SHOCK`/`SPASMS`, cooldown/custo, persistência e descarte. **⛔ Perks de tamanho, chain, dano, multi-shot e transformação de status sem contrato mutador exato seguem bloqueadas.** Não alterar certificação.
