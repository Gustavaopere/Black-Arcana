# Goety 3.1.4 — `soul_heal_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `soul_heal_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 94/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

**Grau de evidência: SOURCE-ADJACENT ONLY.** A presença de `soul_heal_focus` está confirmada como item de Focus no JAR 3.1.4 hash-matched; o algoritmo abaixo foi lido no commit público imutável [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef), que declara **3.1.1**, **NÃO** a versão instalada 3.1.4. Nenhum método ou coeficiente aqui é certificado para 3.1.4. QA física do cast/Survival **NÃO EXECUTADA**.

**Descrição funcional da fonte adjacente:** cura o próprio caster e, se houver radius positivo, pode curar aliados e entidades cujo dono imediato seja o caster dentro da região de consulta. Não é dano mágico nem um disparo ofensivo.

### Localizadores de classe e parâmetros (somente 3.1.1)

- [`ModItems.SOUL_HEAL_FOCUS` — linha 310](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L310): entrada de registro `soul_heal_focus` associada a `new MagicFocus(new SoulHealSpell())` na versão adjacente.
- [`SoulHealSpell.java` — linhas 25–88](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/SoulHealSpell.java#L25-L88): métodos `defaultStats`, `defaultSoulCost`, `defaultCastDuration`, `defaultSpellCooldown`, `conditionsMet` e `SpellResult(ServerLevel, LivingEntity, ItemStack, SpellStat)`.
- [`SpellConfig.java` — linhas 1915–1923](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1915-L1923): defaults **3.1.1**, não config implantada: `soulHealCost=250` (≥0), `soulHealDuration=0` (0–72000), `soulHealCoolDown=200` (≥0), `soulHealAmount=8` (mínimo configurável 2).
- [`SpellStat.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/SpellStat.java): `potency` (inteiro) e `radius` (double); setters/`increaseRadius` existem nessa classe da versão adjacente, mas **não constituem API externa mutadora segura**.
- [`Spell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/Spell.java): ponte `serverCheckSpellResult` executa `SpellResult` apenas em `ServerLevel`. Fluxo real de admissão, custo/reserva/debito e cancelamento fora desse método **NÃO VERIFICADO**.

### Matriz causal orientada a perks

| Eixo | Observado na implementação pública 3.1.1 | Condição/limite |
|---|---|---|
| Condição de admissão | `SoulHealSpell.conditionsMet`, quando caster é `Mob`, exige `health < maxHealth`; para outros casters retorna decisão base. | Não inferir filtro de HP aplicado a jogadores sem verificar a classe base/consumer 3.1.4. |
| Alvo de cura | `caster.heal(heal)` é executado; **se** radius > 0, `getEntitiesOfClass(LivingEntity.class, caster.getBoundingBox().inflate(8.0 × radius))` consulta entidades. Só aplica cura adicional se `MobUtil.areAllies` ou `MobUtil.getOwner(target)==caster`. | **AABB expandida por eixo**, não círculo/esfera de raio 8 × radius; não confirma line-of-sight, limite máximo de entidades ou proteção PVP. |
| Potency/atributos | `defaultStats().setPotency(1)`. `spellStat.getPotency()` e `getRadius()` são base; `WandUtil.enchantedFocus` adiciona níveis `POTENCY` e `RADIUS`. | Não concluir escalonamento ilimitado nem controle de radius por perks externas; limites de config/nível efetivos não medidos. |
| Fórmula da cura | `baseHeal=SpellConfig.SoulHealAmount.get()`; `heal = baseHeal + RandomUtil.nextInt(worldRandom, baseHeal * max(0, potency - 1) + 1)`, em seguida usa o mesmo `heal` para caster e demais elegíveis. | **Literal da fonte adjacente**, depende da implementação de `RandomUtil.nextInt`; distribuição, arredondamento, limites efetivos e HP restaurado em 3.1.4 NÃO VERIFICADOS. |
| Mana/custo/cooldown | São lidos de `SoulHealCost`, `SoulHealDuration` e `SoulHealCoolDown`, com defaults 250/0/200 na fonte 3.1.1. | Não assumir que valores 3.1.1 estejam ativos no pack, que duration seja segundos, nem que a Soul Energy seja debitada pelo método desta ficha. |
| Dano/status/projétil | Nenhum projétil ofensivo ou `DamageSource` é criado em `SoulHealSpell.SpellResult` observado; há partículas/som de cura. | **N/A apenas no corpo auditado 3.1.1**, não prova ausência de efeitos de addons ou interceptors na versão 3.1.4. |
| Duração/aoe/caps | A operação é cura imediata chamada uma vez por `SpellResult`; a consulta em AABB pode alcançar múltiplas entidades. | Sem prova de budget explícito do método, limite global de alvos, repeats por tick ou sobrevivência de buffs. Não prometer raio circular ou duração de HoT. |
| Lifecycle causal | `SpellResult` realiza cura própria + curas de aliados/owned e partículas; não cria novo Focus nem summon. | Se o próprio caster satisfizer também os filtros da consulta, avaliar em QA risco de múltipla invocação de `heal`; **duplicação não comprovada** sem verificar `MobUtil.areAllies` e retorno da consulta. |

### Possibilidades seguras e pendências

- **Parâmetros candidatos à perk**, caso um contrato real venha a existir: `radius`, `potency`, quantidade efetivamente restaurada e filtros de aliados. Não alterar a lista de alvos no cliente; o servidor e o Goety controlam `heal`/custo.
- **Mutabilidade:** A = configurações provider-native vistas apenas no source 3.1.1; B = hook mutador Goety 3.1.4 **NÃO VERIFICADO**; C = adapter de observação/consulta **CONDICIONADO**; D = cura extra, mudança de ally filter, pagamento externo, reset de cooldown ou readjust de AABB em runtime **⛔ FAIL-CLOSED**.
- **Causalidade/Mastery:** tratar a execução Goety como uma única conjuração mesmo ao curar múltiplos alvos; evitar recompensa duplicada por cast, `heal` e partículas. Não alimentar `Corruption`/`Strain` do Black Arcana sem uma bridge de identidade aprovada.
- **QA exigida:** comparar `SoulHealSpell`, `SpellStat`, `SpellConfig` e consumo no classfile exato 3.1.4; demonstrar o config carregado; testar potência e raio com caster solo, aliado, pet próprio, não aliado e caster já curado; validar limite dos alvos, possível autocura duplicada e refund sob cast cancelado no dedicated server, seguido de Survival/modpack real.

**Estado para certificado:** ⚠️ dossiê de causalidade source-adjacent, **não** promoção ao manifesto de sete evidências, **não** liberação de perk mutadora e **não** incremento do progresso técnico 100%.
