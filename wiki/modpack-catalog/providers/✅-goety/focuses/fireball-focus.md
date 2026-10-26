# Goety 3.1.4 — `fireball_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `fireball_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 36/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
- **Aquisição documental:** o JAR exato contém receita base de aquisição homônima para este Focus e sem condition de mod carregado; o conjunto tem 80 recipes de tipo `goety:ritual` e 43 shaped. **O tipo específico desta receita não é deduzido apenas pela lista agregada.** A execução real com recursos/progressão do modpack não foi comprovada nesta etapa.
- **Conta semântica:** `COUNTED_EXACT`, já incluída nos 123 Focuses Goety do ledger; materializar a ficha **não acrescenta uma nova identidade**. Receitas alternativas de obtenção não criam outros spells.
- **Escola/categoria exata, classe e método runtime, cast-time, Soul Energy, cooldown, alcance, dano, efeitos, targeting, PVP/proteção, progressão/research e numeric balance:** **NÃO VERIFICADO nesta ficha** para o JAR 3.1.4. A referência source-adjacent 3.1.1 abaixo é evidência de outra versão e não estabelece automaticamente contrato de API/efeito do JAR instalado.

## Authority e deduplicação

Goety é a autoridade de Soul Energy, Focus/Staff casting, custos, recipe execution, servants, cleanup e estado persistente. Black Arcana não cria outro Soul ledger, uma segunda conjuração, um débito adicional, novo summon ou uma segunda world mutation; quaisquer bridges futuras exigem boundary server-safe comprovada e comportamento fail-closed.

## Evidência

- [Inventário semântico exato 3.1.4](../EXACT-3.1.4-SEMANTIC-INVENTORY.md): lista de **123** nomes `_focus` ativos, com `empty_focus` excluído e aquisição agregada 80/43.
- [Auditoria do artefato](../EXACT-3.1.4-ARTIFACT-AUDIT.md): hash físico verificado e exclusões.
- [Fronteira de integração](../INTEGRATION-RULES.md) e [catálogo anterior](../FOCUS-CATALOG.md).

**Clean-room:** a ficha contém dados factuais de identidade e proveniência, não código, assets, tradução de tooltip ou implementação upstream.

## Auditoria técnica para perks — referência source 3.1.1 (26/10/2026)

**Grau de evidência: SOURCE-ADJACENT ONLY.** O ID e a presença do Focus são confirmados no JAR 3.1.4 com SHA-1 acima; **nenhum valor, método, dano ou contrato de modificação abaixo foi confrontado com o bytecode do JAR 3.1.4**. A referência reprodutível é o commit público imutável [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef), linha de código **3.1.1**, e não release 3.1.4. Comparação de comportamento é hipótese até nova prova exata. QA em Survival/modpack **NÃO EXECUTADO**.

**Descrição funcional da fonte adjacente:** dispara uma bola de fogo ou, com conjunto Unholy, um Hell Bolt, podendo produzir projéteis adicionais com staff compatível. O projetil e efeitos posteriores são controlados pelo Goety, não por uma segunda magia Black Arcana.

### Localizadores e execução (somente 3.1.1)

- [`ModItems.FIREBALL_FOCUS` — linha 407](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L407): registro `fireball_focus` → `new MagicFocus(new FireballSpell())` na fonte adjacente. O ID do item no JAR 3.1.4 tem evidência binária separada; a classe concreta da versão instalada **ainda não**.
- [`FireballSpell.java` — linhas 28–137](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/nether/FireballSpell.java#L28-L137): `defaultSoulCost`, `defaultCastDuration`, `defaultSpellCooldown`, `getSpellType`, `acceptedEnchantments` e `SpellResult(ServerLevel, LivingEntity, ItemStack, SpellStat)`.
- [`Spell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/Spell.java): `serverCheckSpellResult` só invoca o resultado em `ServerLevel`; `rightStaff` testa `IWand` e compatibilidade de `SpellType`. Os métodos de admissão e débito final de Soul Energy **não foram rastreados até o consumidor**.
- [`SpellConfig.java` — linhas 950–960](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L950-L960): **defaults declarados na fonte 3.1.1**, não a configuração efetiva do pack: `fireballCost=4` (config inteiro ≥0), `fireballTime=0` (0–72000), `fireballCoolDown=40` (≥0), `fireballDamage=5.0` (≥1) e `fireballGriefing=true`.
- [`ModFireball.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/ModFireball.java) e [`HellBolt.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/HellBolt.java): consumidores pós-cast (colisão, dano, fogo, estado e descarte). Os métodos e os números são **da mesma fonte adjacente**.

### Matriz de parâmetros, geometria e consequências

| Eixo de perk | Cadeia verificada em source 3.1.1 | Limite de conclusão para 3.1.4 |
|---|---|---|
| Ativação/custo | `FireballSpell` lê `SpellConfig.FireballCost`; classe base entrega resultado no servidor. | Default 4 na 3.1.1; **cobrança efetiva, redução, refunds e ordem de eventos 3.1.4 NÃO VERIFICADOS**. |
| Cast/cooldown | Métodos `defaultCastDuration` e `defaultSpellCooldown` retornam valores configurados; defaults 0 e 40. | Valores inteiros de config; não atribuir segundos, ticks efetivos, tempo de animação ou modificabilidade por perk sem consumidor exato. |
| Alvo/alcance/LOS | `SpellResult` usa direção visual do caster, sem `getTarget` ou raycast de aquisição explícito nessa rotina. Colisão delegada às entidades. | **Alcance máximo, LOS, hitbox, friendly fire, raio de explosão e número de vítimas NÃO VERIFICADOS**; não confundir vetor de olhar com alcance. |
| Projéteis | Primeiro `ModFireball`, ou `HellBolt` se `hasUnholySet(caster)`. Se `rightStaff(staff)`, a rotina gera **mais dois** da mesma família (1 ou 3 por execução dessa rotina). Os adicionais deslocam origem em X/Z por valores gaussianos. | É contagem de instâncias da rotina adjacente, não garantia de limite absoluto do cast de 3.1.4 nem propriedade pública mutável. |
| Potency/burning | `SpellStat` fornece `potency` e `burning`; `enchantedFocus` acrescenta níveis `POTENCY`/`BURNING`. `ModFireball` recebe `setExtraDamage(potency)` e `setFiery(burning)`; `HellBolt` recebe `setDamage(configDamage × WandUtil.damageMultiply() + potency)` e `setFiery(burning)`. | A expressão configura entidades, **não prova dano final de HP**, valores máximos ou possibilidade de retarget/scale externa. |
| Colisão/dano | Em `ModFireball.onHitEntity`, o dono jogador usa base de `FireballDamage × damageMultiply`, outros donos podem usar `getDamage`, somando `extraDamage`. DamageSource normalmente `fireball`, com ramo `magicFireball` condicionado por Nether Robe. `HellBolt.onHitEntity` usa `hellfire` e `getDamage`. | Tipos são condicionais da fonte 3.1.1; não rotular automaticamente toda Fireball como dano mágico, nem transferir fonte de dano 3.1.4 por analogia. |
| Ignição/efeitos persistentes | `ModFireball` aplica até `5 × (1 + fiery)` segundos de fogo no alvo na chamada adjacente e `HellBolt` aplica `5 × fiery` se `fiery>0`. `HellBolt.onHit` pode gerar entidade secundária `Hellfire`. | Tempo nominal da chamada, não duração medida; `Hellfire` é **efeito downstream da mesma ação**, não segundo cast. |
| Vida útil | Ambas classes têm descarte local quando `tickCount >= secondsToTicks(10)`. | Limite desse código em 3.1.1; velocidade e dimensões físicas não foram verificadas nem em 3.1.1 nem no JAR 3.1.4. |
| Mundo/claims | `ModFireball.onHitBlock` só tenta criar fogo se `isDangerous` e passar por `EventHooks.canEntityGrief` ou config específica para dono jogador. `isShifting` pode desligar `dangerous` na construção de `ModFireball`. | Não confundir controles nativos de griefing com aprovação do `WorldEffectPolicy` Black Arcana; variante Hell Bolt/Hellfire requer auditoria própria. |

### Mutabilidade, causalidade e gates

**Exame de eixos:** `SpellStat` fornece setters de atributos [na fonte 3.1.1](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/SpellStat.java), mas **isso não é evidência de evento público mutador**, de modificação por jogador nem de segurança na versão 3.1.4. Alterações A (config nativa) são apenas defaults/config verificados **na fonte adjacente**; B (hook/evento) = **NÃO VERIFICADO**; C (adapter futuro) = **CONDICIONADO**; D (retarget/raio/velocidade/tipo de dano/persistência) = **⛔ FAIL-CLOSED** até prova no JAR exato e QA.

**Deduplicação proposta:** um acionamento provider-native → 1 ou 3 projéteis → colisões/status/Hellfire; todos são efeitos de uma só identidade `fireball_focus`. Mastery/proc não deve ser concedido por lançamento e por cada entidade ao mesmo tempo sem regra de autoria e correlação aprovada. Não criar custo/cooldown secundário, duplicar dano ou contornar griefing do provider.

**Próximas provas obrigatórias:** `FireballSpell`/`ModFireball`/`HellBolt` no classfile SHA-exato 3.1.4; config realmente carregada e override por datapack; fluxo de mana/Soul Energy (reserva/debito/cancelamento); colisão no dedicated server com múltiplos projéteis, Nether Robe, shift, addon e world claim; cliente real/Survival. **Status deste dossiê: ⚠️ source-adjacent, sem certificado de sete evidências; não incrementar contadores de 100%.**
