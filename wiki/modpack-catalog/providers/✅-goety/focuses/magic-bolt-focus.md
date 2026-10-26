# Goety 3.1.4 — `magic_bolt_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `magic_bolt_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 63/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê de engenharia causal — Magic Bolt (26/10/2026)

**Separação de evidência:** o ID `magic_bolt_focus` está no inventário SHA-exato do **JAR Goety 3.1.4**; a descrição de classe e os parâmetros abaixo provêm exclusivamente da fonte pública **Goety 3.1.1** no commit imutável [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). **Equivalência Java/classfile com 3.1.4, config física, hook seguro e QA no modpack: NÃO VERIFICADOS.** `SOURCE_ADJACENT_311`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

**Descrição funcional no source adjacente:** projétil mágico com dano/cursing ao atingir entidade e uma `MagicGround` persistente gerada no impacto válido; o efeito em área pertence à mesma conjuração, com código próprio de ticks e proprietários.

### Evidência localizável — somente Goety 3.1.1

- [`ModItems.MAGIC_BOLT_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L302) associa `magic_bolt_focus` a `new MagicFocus(new MagicBoltSpell())` na versão de referência.
- [`MagicBoltSpell`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/MagicBoltSpell.java) possui `defaultSoulCost`, `defaultCastDuration`, `defaultSpellCooldown`, `acceptedEnchantments` e `SpellResult(ServerLevel, LivingEntity, ItemStack, SpellStat)`.
- [`SpellConfig.java` linhas 1044–1052](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1044-L1052): defaults de referência `magicBoltCost=8`, `magicBoltTime=0`, `magicBoltCoolDown=20`, `magicBoltDamage=4.0`, com ranges de configuração (`time` 0–72000, dano ≥1). **Não** são valores lidos no mundo instalado.
- [`MagicBolt.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/MagicBolt.java) consome potência/duração e trata `onHitEntity`, `onHit`, `magicGround` e `tick`. [`MagicGround.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/util/MagicGround.java) contém `radius`, seleção de entidades e dois caminhos de chamada a `hurt`. [`SpellHurtingProjectile.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellHurtingProjectile.java) contém os filtros de colisão e o estado básico.

### Matriz de parâmetros, alcance e causalidade

| Eixo | Evidência source 3.1.1 | Restrição de engenharia |
|---|---|---|
| Cast/custo/cooldown | Defaults de config são 8 / 0 / 20; `MagicBoltSpell` lê os valores por método; `SpellResult` cria exatamente **um** `MagicBolt` e define `owner` antes do spawn. | Cobrança, duração medida, unidade de cooldown, cancelamento/reembolso e equivalência 3.1.4 **NÃO VERIFICADOS**. |
| Alvo, geometria e LOS | O cast posiciona projétil à frente do caster usando vetor de olhar, sem raycast próprio; `MagicBolt.canHitEntity` protege dono/aliados/owned segundo condições locais; `MagicGround.tick` lê entidades na `getBoundingBox()` da armadilha. | Não inferir raycast de lock-on, alcance, raio de explosão ou limite de alvos. `MagicGround.radius()=1.0f` **não prova uma seleção circular de raio 1**, pois o consumidor lê AABB. |
| Potency / dano | `SpellStat.potency` (mais POTENCY encantada) passa a `setExtraDamage`. `MagicBolt.onHitEntity` calcula `config MagicBoltDamage × WandUtil.damageMultiply`, pode substituir pela base `ATTACK_DAMAGE` do dono `Mob`, acrescenta `extraDamage`, usa `ModDamageSource.magicBolt`, e chama `hurt`. | O `4.0` da config não é HP final; damage source exato e aplicação são somente 3.1.1. A rotina possui caminhos com `owner` nulo que precisam QA. |
| Status ao impacto | Quando `hurt` retorna aceito e target é `LivingEntity`, aplica `GoetyEffects.CURSED` por `100 × (extraDuration + 1)` ticks **se** há dono `LivingEntity`; sem ele, base 100 ticks. | Valor nominal no source, não tempo observado na 3.1.4; um `damage event` não implica por si só debuff aplicado. |
| Efeito posterior | `MagicBolt.onHit` em servidor, se a colisão é aceita, executa `magicGround` e descarta o projétil. A armadilha `MagicGround` recebe owner e duração `100 × (extraDuration + 1)` se owner vivo, ou 100 sem ele. | É uma consequência do **mesmo cast**, não um segundo spell. Não contar armadilha por VFX nem ativação cliente. |
| Dano da área | `MagicGround.tick` busca `LivingEntity` elegíveis dentro da bounding box, exclui owner/aliados quando conhecido e **tenta** `hurt(magic,4.0f)` em cada alvo; se houver owner, há **segunda chamada** `hurt(indirectMagic, damage)` (4.0 nominal ou metade de `ATTACK_DAMAGE` se owner `Mob`). | Duas tentativas de `hurt` **não** provam dois danos efetivos por tick: i-frames, invulnerabilidade, event cancellation e conflitos com addons exigem QA. |
| Duração/lifetime | `MagicBolt.tick` descarta o projétil a partir de `tickCount>=100`; `MagicGround.tick` descarta a entidade quando `tickCount>=getDuration()`. `extraDuration` é estado serializado no projectile. | Não confundir lifetime de projétil com área, cooldown ou cast-time. `extraDuration<-1` e overflow/caps requerem prova de validação em 3.1.4. |
| Mundo / segurança | `MagicGround` é entidade persistente temporária, com múltiplas buscas de entidades em tick; não há alteração direta de blocos nesses métodos observados. | A ausência de `setBlock` nesses corpos não certifica nenhuma política global de claims; Black Arcana `WorldEffectPolicy` só protege efeitos próprios. |

### Implicações para perks e Mastery

Perks candidatas futuras: potência, duração do debuff, duração da `MagicGround`, filtros de alvo, geometry/hitbox, número de hits e dano da área. Esses são **eixos de design, não hooks certificados**. O uso de setters internos (`setExtraDamage`, `setExtraDuration`) não demonstra interceptação segura por RPG Skill Tree nem modifica a entidade antes do cast na versão 3.1.4.

**Não mutar por suposição:** não duplicar pagamento de Soul Energy, prolongar uma área externa sem autorização, converter `MagicGround` em nova magia Black Arcana, creditar Mastery por projectile spawn + hit + área por tick, ou aplicar `WorldEffectPolicy` retroativamente ao Goety. Um observador futuro exige owner/cast correlation e política server-authoritative de deduplicação.

**Gates pendentes:** JAR 3.1.4 hash-exato para `MagicBoltSpell`/`MagicBolt`/`MagicGround`, classe e codec reais, config efetiva, cooldown/débito, side de `onHitEntity`, capacidade e multiplicidade da consulta `getEntitiesOfClass`, controle de owner, duração extrema/overflow e QA dedicada em jogo. Até esse gate: **⚠️ SOURCE_ADJACENT / ⛔ mutation FAIL-CLOSED / sem certificado de sete evidências; índice global não se altera.**
