# Lapsus

**Revisão documental: 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita aos pins abaixo. Catálogo ✅; runtime/perks ⚠️ condicionados. **+0 identidades mágicas.**

| Identidade e evidência | Valor / limite da prova |
|---|---|
| Provider / host / tipo | Ypsilon's Fundamentalism (Fundamental Principles); `mod_id=ypfundamentals`; host Iron's Spells 'n Spellbooks; `spell`, escola default Ender. |
| ID real / classe | `ypfundamentals:lapsus`; `com.ypsi.fundamentalism.spells.ender.LapsusSpell`; registro singleton via `ModSpells#registerSpell(AbstractSpell)` ([Registry]). Nome de exibição separado do ID. |
| Artefato físico histórico | Minecraft 1.21.1 / NeoForge; `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [publicação CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503). [Auditoria histórica](../EXACT-BINARY-SPELLS-1.1.7.1.md) e [Java21 SUCCESS](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443): `COUNTED_EXACT` só identidade/registry/classe/escola, sem prova de métodos ou gameplay. SHA-256: NÃO VERIFICADO. |
| Source consultado | Ypsilon `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, metadados 1.1.7.1 / MIT ([Metadados]); dependência declarada Iron's **3.16.2** ([Versão]). Herança consultada separadamente em Iron's **3.16.3** `e4056af90302d37eb1739f5ff05020b020e6e252`. Não se afirma equivalência binária/source nem compatibilidade operacional 3.16.2→3.16.3. |
| Descrição oficial / resumo original | [Guia e nome no recurso de idioma][Guia]: memoriza uma posição e permite regressar durante uma janela curta. Nenhum asset ou implementação foi copiado. |

Os números seguintes são **defaults/fórmulas do source**, não config implantada. `n` é o nível resolvido pelo host; as listas usam nível nominal e multiplicadores neutros = 1. Gates, categorias ASM/Principles e valores efetivos exigem QA no pack. [Contrato comum de custos, eventos e compatibilidade](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

## Matriz por campo

`NATIVE` identifica config/atributo nativo, sem prometer controle individual por perk; `CONDITIONAL` exige contrato/teste do adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para a mudança descrita.

| Campo | Default / fórmula / unidade | Declarante, fase e boundary real | Mutabilidade / limite / teste |
|---|---|---|---|
| Nível / raridade / escola | 1–3; Rare; Ender; cooldown default 45 s = 900 ticks. | `LapsusSpell#defaultConfig` [Spell]; config resolvida por host. | `NATIVE/CONFIG_NATIVE` global; config efetiva NÃO VERIFICADA; Q1. |
| Mana | `50+10(n−1)` = 50 / 60 / 70 mana antes de multiplicador e truncamento `int` do host. | Construtor [Spell] + `AbstractSpell#getManaCost(int)` [Host valores]; `castSpell` cobra antes de `onCast`, somente se a origem consome mana e ainda não existe recast [Host cast]. | `NATIVE/CONFIG_NATIVE` mana multiplier; evento `setManaCost(int)` é `CONDITIONAL` [Evento cast]. Não cobrar de novo no retorno; Q2. |
| Cast / cooldown | INSTANT; 0 ticks. Cooldown base 900 ticks; redução efetiva, origem sword/creative e evento pertencem ao host. | `getCastType`, construtor [Spell]; `MagicManager#addCooldown/getEffectiveSpellCooldown` [Host cooldown]. `onRecastFinished` chama `super` antes de limpar posição [Recast]. | `NATIVE` para configuração/atributo de cooldown; `CONDITIONAL` para evento. Janela não é cooldown; Q2/Q3. |
| Recast / janela | Total **2 execuções incluindo inicial**, portanto 1 retorno; TTL `60n` ticks = 3 / 6 / 9 s. | `getRecastCount`, `getTicksToLive`, `onCast` [Execução]; `RecastInstance` inicializa `remainingRecasts=total−1` [Host recast]. Cast data fornecido = `null`. | `SEM_HOOK_SEGURO` para alterar count/TTL isoladamente; não há config específica provada. Q3. |
| Alvo / alcance | Self. Salva `entity.blockPosition().below()` e solicita destino **(X, Y+1, Z)** dessa `BlockPos`, sem `+0.5` de centralização. Não soma 1 a X/Z. Não há distância máxima implementada nesta classe. | `onCast` server-side [Execução]. Primeiro cast grava; segundo usa o estado que estiver no campo `location`. | `SEM_HOOK_SEGURO` para extensão de alcance ou retarget. Sem range declarado não significa teleport seguro/ilimitado autorizado; Q4/Q5. |
| LOS / destino / dimensão | Sem raycast, LOS, teste de chão, colisão segura, chunk carregado ou chave de dimensão no estado local. | `location` é apenas `BlockPos` [Spell]. Host `Utils#handleSpellTeleport(AbstractSpell,Entity,Vec3)` posta `SpellTeleportEvent`, usa coordenadas do evento e chama `entity.teleportTo` se não cancelado [Teleport]. | `CONDITIONAL` para cancelamento/coordenadas via evento auditado [Evento teleport]; não prova proteção/claims nem mudança de dimensão; Q4. |
| Retorno cancelado / falha | O boolean do helper significa **canceled**. A spell ignora o retorno, zera fall distance e limpa `location` mesmo se o evento cancelar. Nenhum refund/rollback local. | Sequência em `onCast` [Execução] + helper [Teleport]. | `SEM_HOOK_SEGURO` para prometer retry/refund; preservar causalidade provider-owned; Q4. |
| Custódia / persistência | `private BlockPos location` vive na instância singleton registrada, compartilhada entre jogadores e mundos que usem a instância. Sem owner UUID, dimension key, NBT ou sync próprios; `onRecastFinished` limpa o mesmo campo. | Campo [Spell], registro [Registry], limpeza [Recast]. Recast do host é por jogador, posição não é. | `SEM_HOOK_SEGURO` para declarar multiplayer-safe ou criar posição paralela. Q5/Q6. |
| Dano / tipo / área | Nenhum `applyDamage`, cura, buff, AOE ou projétil no fluxo. `baseSpellPower=15`, incremento 0 são campos de construtor sem uso no resultado de Lapsus; escola Ender não é dano aplicado. | [Spell] [Execução]. | `N/A` para dano/type/hitbox/velocidade/pierce/summon; conversão ou AOE = `SEM_HOOK_SEGURO`; Q1. |

## Pipeline, obtenção e autoria

Ingresso por casting do host: `attemptInitiateCast` valida mana/cooldown/aprendizado, chama `checkPreCastConditions` herdado e `SpellPreCastEvent`; Lapsus só delega `canBeCastedBy` [Host gates] [Recast]. **Scroll é rejeitado no host para spells com recast**, portanto não presumir ativação por scroll [Host gates]. Loot/crafting/aprendizado não têm bypass próprio nesta classe; chance, receita e fonte Survival são **NÃO VERIFICADAS** [Host obtenção].

Na conclusão server: evento de cast → eventual pagamento → criação do recast se ausente → salvar ou solicitar teleport → som padrão via `super.onCast`. No retorno o host consome o recast existente sem segunda mana; no término/expiração o callback aplica cooldown e limpa estado [Host cast] [Execução] [Recast]. [Principles] também pode cancelar admissão, modificar custo e registrar fadiga/XP; categorias e config efetivas não foram executadas. Nenhuma segunda mastery/XP/cobrança deve nascer do callback de limpeza ou do evento de teleport.

Iron's/Ypsilon mantêm casting, mana, recast e teleport; RPG Skill Tree só progression/gates por contrato real; Black Arcana mantém seu runtime e WorldEffectPolicy. A assinatura ocupada é **âncora pessoal temporária + retorno por recast**; nova magia exige semântica distinta. Nenhuma perk, adapter ou correção do singleton foi implementada.

## QA e pendências explícitas

- **Q1 — source documental:** campos e links auditados nos pins; JAR histórico prova identidade. Config implantada, método binário e execução física: **PENDING**.
- **Q2 — recursos:** servidor dedicado deve medir mana/cooldown no cast inicial, retorno e timeout, incluindo sword, creative e handlers de Principles. **PENDING**.
- **Q3 — janela:** níveis 1–3, retorno no último tick, cancelamento do cast, expiração e logout/relogin; comprovar 2 execuções totais e uma conclusão. **PENDING**.
- **Q4 — segurança:** evento cancelado/retarget, destino obstruído/sem chão, deslocamento distante, borda/chunk e mudança de dimensão; comprovar limpeza mesmo no cancelamento. **PENDING**; nenhum claim/protection integrado foi demonstrado.
- **Q5 — concorrência:** A grava, B grava/retorna/expira, depois A retorna; repetir em dimensões diferentes. Campo singleton é blocker source-causal, não falha já observada em jogo. **PENDING**.
- **Q6 — lifecycle:** morte, unload, restart e recast persistido com `location` não persistida; testar cliente/servidor no pack 3.16.3. Survival/multiplayer/GameTest: **PENDING**.

[Versão]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L16
[Metadados]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L30-L36
[Registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L29-L58
[Guia]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L57-L75
[Spell]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ender/LapsusSpell.java#L39-L77
[Execução]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ender/LapsusSpell.java#L90-L115
[Recast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ender/LapsusSpell.java#L117-L126
[Host valores]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[Host cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L346
[Host gates]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L401
[Host obtenção]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[Host cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L122
[Host recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[Teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L175
[Evento teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellTeleportEvent.java#L7-L18
[Evento cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L74
[Principles]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L516-L645
