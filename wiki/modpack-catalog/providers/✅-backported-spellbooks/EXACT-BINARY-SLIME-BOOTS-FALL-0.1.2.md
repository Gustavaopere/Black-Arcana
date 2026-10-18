# Backported Spellbooks 0.1.2 — Slime Boots, atributos e proteção de queda

**18/10/2026 · ✅ `EXACT_PUBLISHER_BOUNDED_EQUIPMENT_AND_EVENT_METHODS` · ⚠️ sem jogador real, efeitos resolvidos ou evento disparado · ⛔ adapter de perk não autorizado.**

## Proveniência e gate exato

- **Provider / JAR:** `backportedspellbooks`, `backportedspellbooks-0.1.2.jar`, 209.868 bytes, SHA-1 `747847c1f38c73250ebac05ea06b41a381187850`, valor idêntico ao snapshot físico certificado. Publicação CurseForge projeto `1543731` / file `8158731`. Metadado interno `0.1.0` preservado como discrepância de versão, não corrigido por suposição.
- **Host instalado na modlist:** Iron's Spells 'n Spellbooks `3.16.3` (#342), Vanilla Backport `1.1.7.10` (#560) e NeoForge `21.1.250` (#001); estas são identidades de inventário, **não** um teste conjunto de loader/host.
- **Workflow:** [Java 21 #39153448024](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39153448024) terminou **SUCCESS**. Gate novo **11/11 autotestes**, `PASS_BACKPORTED_012_SLIME_BOOTS_FALL_BOUNDED_BYTECODE`, `deviations=[]`. [Artefato JSON #12145728990](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39153448024/artifacts/12145728990). [Verificador fail-closed](../../../../docs/qa/backported_012_slime_boots_fall_bytecode.py) faz `javap -p -c` no JAR previamente validado por SHA-1, sem incorporar bytecode ou assets de terceiros.
- **Fonte de referência:** [`SlimeBootsArmorItem.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/item/armor/SlimeBootsArmorItem.java#L25-L34), [`ServerEvents.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/events/ServerEvents.java), [`ModItems.java`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/blob/07cb65efca0c264762a21c2d6bce0f83e3947226/src/main/java/net/redreaper/backported_spellbooks/init/ModItems.java). Commit de fonte **do dia da release**, sem identidade de build byte a byte provada.

## Parâmetros compilados do item

Em `net.redreaper.backported_spellbooks.item.armor.SlimeBootsArmorItem.<init>`, as quatro construções `AttributeContainer` e o `ImbuableChestplateArmorItem` final constam em sequência e foram validadas pelo verificador:

| Ordem | Registry de atributo | Constante (`ldc2_w`) | Operação no JAR | Proprietário |
|---|---|---|---|---|
| 1 | `Attributes.JUMP_STRENGTH` | `double 0.1d` | `ADD_MULTIPLIED_BASE` | Slime Boots |
| 2 | `ModAttributes.FRICTION_MODIFIER` | `double 0.3d` | `ADD_MULTIPLIED_BASE` | Slime Boots / Vanilla Backport |
| 3 | `ModAttributes.BOUNCINESS` | `double 2.5d` | `ADD_VALUE` | Slime Boots / Vanilla Backport |
| 4 | `ModAttributes.AIR_DRAG_MODIFIER` | `double -0.5d` | `ADD_MULTIPLIED_BASE` | Slime Boots / Vanilla Backport |

Estes operandos são valores passados ao **construtor**, não medições de velocidade, pulo ou rebote. Os valores de `Slime Aspect` são **outros**: bounciness `0.5d ADD_VALUE`, jump `0.15000000596046448d ADD_MULTIPLIED_TOTAL`, air drag `-0.10000000149011612d ADD_MULTIPLIED_TOTAL`, conforme [prova separada](EXACT-BINARY-SLIME-ASPECT-0.1.2.md). Portanto, juntar os dois sistemas em perks exige validar a ordem de agregação do host, baseline, amplificador e restrições reais; somar percentuais ou forçar `ADD_VALUE` por equivalência nominal é incorreto.

## Rota `LivingFallEvent`

O método compilado `net.redreaper.backported_spellbooks.events.ServerEvents.onFallEvent` contém, em ordem delimitada:

1. `LivingFallEvent.getEntity` e teste de tipo `Player`;
2. referência a `EquipmentSlot.FEET`, chamada `Player.getItemBySlot`;
3. referência a `ModItems.SLIME_BOOTS` e chamada `ItemStack.is`;
4. `iconst_1` e **um callsite** de `setCanceled`.

Dentro **desse método** não existem chamada de consulta de cooldown (`getCooldowns` / `isOnCooldown`) nem referência direta a `ModMobEffects.SLIME_ASPECT`. Isso separa a ação de cancelamento de queda do spell, sem provar que o status mágico jamais possa afetar a física do salto/queda por outros consumidores. O verificador identifica presença, sequência e quantidade desses callsites, **não** valida formalmente o fluxo de controle, injeção/inscrição real no EventBus nem o retorno observado em jogador.

`SlimeBootsArmorItem.appendHoverText` contém chamadas de `Utils.applyCooldownReduction` e chave de tooltip `passive_ability_no_cooldown`. O `COOLDOWN_TICKS=20` é campo **da fonte**, não medição do cooldown da queda, e o handler inspecionado não verifica cooldown antes de chamar `setCanceled`. Portanto a tooltip não certifica cooldown físico e não autoriza construir rate-limiter externo por simetria.

## Fronteira de causalidade e plano de QA

- **Identidade semântica:** Slime Boots é um **item/equipamento**, não uma sétima magia; a queda cancelada tampouco constitui outro cast. `backportedspellbooks:slime_aspect` permanece a mesma das seis magias já contadas. +0 raízes mágicas, +0 adapters.
- **Authority:** Backported Spellbooks registra equipamento/efeito e handler; Minecraft/NeoForge, Iron's e Vanilla Backport controlam eventos/atributos/física conforme seu contrato efetivo; RPG Skill Tree apenas progressão e perks via boundary real; Black Arcana apenas seu runtime mágico.
- **Exigência QA física:** jogador real em servidor, botas equipadas/removidas, apenas buff, apenas botas, ambos e nenhum; comparar atributos resolvidos, queda e dano após hit; persistência/relog/respawn; outros modifiers; desativação de provider; config/compatibilidade no perfil. Testar o evento e a redução real, não inferir resultado pela presença do callback.
- **⛔ Perks:** não gerar cancelamento adicional em `LivingFallEvent`, duplicar `AttributeContainer`, aplicar status `SLIME_ASPECT` à força ou atribuir Mastery por tick/fall/cancel sem contrato público seguro e causal ID. Não há hook seguro de mutação validado neste gate.

**Progresso auditado:** `Backported Spellbooks` **6/6 registros mágicos**, **6/6 fichas** e **6/6 magias com método compilado delimitado**, sem mudança quantitativa nesta auditoria de equipamento. Global **—%**, piso documental anterior **1.857 objetos semânticos / 1.855 no escopo estrito**, denominador final aberto. Stage 06.05 🟡; Stage 09 físico pendente; nenhuma promoção ou merge autorizada por esta prova estática.
