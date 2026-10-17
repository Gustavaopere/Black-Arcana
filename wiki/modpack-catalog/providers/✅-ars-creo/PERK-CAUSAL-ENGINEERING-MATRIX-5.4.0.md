# Ars Creo 5.4.0 — matriz de engenharia causal para perks

**Checkpoint 17/10/2026 · PR #825.** Matrizes source-pinned dos sete mecanismos do provider. **Não são sete magias, nem novas identidades semânticas.** O Black Arcana controla seu runtime mágico; Ars Nouveau e Create mantêm seus próprios executores, recursos, destinos, rituais, máquinas, redes cinéticas e inventários. RPG Skill Tree gerencia atributos/perks/Mastery somente quando existir contrato de resultado autêntico.

## Proveniência, barras e estado

- Instalado no sibling: `ars_creo-1.21.1-5.4.0.jar`, mod ID `ars_creo`, SHA-1 documentado `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Source oficial de versão 5.4.0 [baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2](https://github.com/baileyholl/Ars-Creo/tree/6a99d36fab441653478fc49de8f28164f0894eb2); source pin não certifica paridade de métodos do JAR instalado.
- Host da modlist: Ars Nouveau `5.13.1`, Create `6.0.10` (ambos posteriores aos builds usados no projeto); integração efetiva/ABI/servidor e cliente permanece **⚠️ NÃO VERIFICADA**.
- **Barra global — —%:** piso do catálogo semântico mais recente **1.857 objetos semânticos / 1.855 estritos**, denominador aberto; **+0 magia**.
- **Barra Ars Creo — ✅ 7/7 (100%) famílias documentadas** com fichas causais de Source/target/custos/range/tempo/side/owners quando aplicáveis; **0/0 spells provider-own registrados**, 1 block+BE+item e 2 Display Sources conforme source registry; **⚠️ QA runtime pendente**; **⛔ 0 adapters RPG homologados**.

## Sete sistemas — escopo causal de integração

| Família | Ficha individual | Comportamento real encontrado no source | Gate/risco | Perk |
|---|---|---|---|---|
| `moving-spell-turrets` | [Moving Spell Turrets](systems/moving-spell-turrets.md) | Basic interação server, Timer `gameTime % time`, Enhanced nova posição; Source manual antes de `MethodProjectile/MethodTouch`; caster `OTHER`, FakePlayers | ⚠️ Source debit e cast não suportado; autoria de Mastery ⛔ | ⛔ mutações do cast / caster / cooldown sem seam |
| `source-on-contraptions` | [Source on Contraptions](systems/source-on-contraptions.md) | Provider 1× por contraption, Source Jar 10.000/transfer10.000, agregação sobre Create blocks, creative infinito/refund | ⚠️ add/remove/relog e inflação de recursos | ⛔ segundo Source ledger / descontos externos |
| `moving-portals` | [Moving Portals](systems/moving-portals.md) | AABB 1 bloco por tick/new-position, PortalTile teleport provider, `fallDistance=0` também em tentativa sem sucesso | ⚠️ repetição/cancelamento/destino inválido | ⛔ novos destinos/retarget sem contrato |
| `moving-rituals` | [Moving Rituals](systems/moving-rituals.md) | RitualBrazierTile fake, item scan inflate1 a cada 5 ticks, SourceUtil range6; onEnd/tryTick sem guard geral client-only no método | ⚠️ compat de ritual a ritual, item consume/side/state | ⛔ duplicação de execução/Source/ritual BA |
| `potion-jar-fluid-bridge` | [Potion Jar ↔ Create Fluid](systems/potion-jar-fluid-bridge.md) | 2.5 mB por unidade Ars; ceil(mB×0.4); `fill` pode informar volume distinto da unidade enviada à jar, sujeito a host checks | ⚠️ conservação, simulate/execute, overflow | ⛔ perks de geração/refund de fluido |
| `starbuncle-wheel` | [Starbuncle Wheel](systems/starbuncle-wheel.md) | Create generator speed default 16/24, stress capacity 16, tag gold na direita do facing horizontal | ⚠️ config runtime/kinetics/load | ⛔ conversão em mana/Source ou proc XP |
| `display-sources` | [Display Sources](systems/display-sources.md) | `ars_creo:turret` e `ars_creo:source_jar`; apresentam nome da magia/Source, sem inferência de sucesso | ⚠️ dados UI/staleness | ⛔ XP/cast/progression baseada em texto |

## Contratos transversais e protocolo de aceite

**Casting e deduplicação:** `ITurretBehavior.castSpell` decodifica `spell_caster` NBT; antes de resolver um MethodProjectile/MethodTouch, cobra Source de jars presentes e, se insuficiente, de Source externo no raio 6. `ContraptionCaster.expendMana` é propositalmente vazio. O contexto usa `ANFakePlayer` e o projétil usa `FakePlayerFactory.getMinecraft`, sem contrato de identidade de ServerPlayer real e `CasterType.OTHER`. Um movimento, actor callback, packet UI, custo ou spawn não autoriza nova raiz de Mastery/Arcane Danger/Corruption/Strain. **Teste de custo sem castType suportado é prioritário**.

**Estado e limites:** `ContraptionSource` soma saldos sobre os blocos da contraption, `getTransferRate` escolhe o máximo, e `SourceUtilMixin` lida com provider creative/infinito, inclusive refund de providers previamente debitados. Não replicar essas mutações, não usar creative como saldo Black Arcana, não fazer polling global per-tick.

**Mundo e mobilidade:** `PortalBehavior` delega a `PortalTile.teleportEntityTo`, consulta AABBs locais por tick/posição, e zera fallDistance inclusive sem teleport verificado; `RitualBehavior` mantém ritual na tile mockada com consumo potencial de item/Source. Contraption/Create não libera a própria magia do Black Arcana das regras de `WorldEffectPolicy`. Ritual interaction custom é comentado no source; não inferir tablet/hand interaction em movimento.

**Conservação de poções:** `PotionTank.fill` e `drain` empregam 2.5/0.4 e `ceil` em ambos os sentidos de requisição mB → Ars unit. A simulação calcula fluid amount diferente do parâmetro usado em `jar.add` em parte dos ramos. **Hipótese de divergência de conservação**, condicionada a checks de `jar.canAccept` e `jar.add` do Ars host — não declarar duplicação confirmada.

**Semantical count:** sete sistemas são famílias de compatibilidade/infraestrutura já catalogadas. O total de spell roots do Ars Creo é zero, e seus eventos não geram castIDs próprios no Black Arcana. Cada ficha contém QA de servidor dedicado, client, Survival, persistência, claims e interplay de providers.

## Próximos gates

1. Validar bytecode/JAR exato de Ars Creo 5.4.0 e ABI com Ars Nouveau 5.13.1/Create 6.0.10; anotar divergência de source.
2. Testar ações de moving turret com e sem Source e tipos não suportados, atribuição real de FakePlayer e pós-dano; não creditar Mastery sem identity/settlement.
3. Testar Potion Jar mB 1,2,3,5, cap e quase cheio em SIMULATE/EXECUTE e drain/fill; registrar invariantes de conservação.
4. Testar ritual por ID com tile mockada, loaded/unloaded/chunks e no-double-completion; portais com no destination e fallDistance sem teleport.
5. Validar fluid/Source/world/perk sem violar `plans/DECISIONS.md` e D035: Stage 06.05 🟡, Stage 09 físico PENDING; PR draft/CI gates impedem merge por esta documentação.

**Status de integração:** `SOURCE_CAUSALITY` para comportamento auditado; `⚠️` para runtime; `⛔` para mudança de geometry/target/custo/dano/temporização sem seam. `+0` novas magias, `+0` adapter implementado.
