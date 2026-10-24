# Exorcism

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: meter, flag e mensagens são estados/callbacks da spell existente.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`; spell **`discerning_the_eldritch:exorcism`**, escola default `irons_spellbooks:holy`. Classe `net.acetheeldritchking.discerning_the_eldritch.spells.holy.ExorcismSpell`, registro `SpellRegistries#registerSpell(new ExorcismSpell())`; consumers `#canBeCastedBy/#onCast`, DTEAttachmentRegistry e ServerEvents. [Registro][registry], [defaults][spell], [attachments][attachments].

Pack MC 1.21.1/NeoForge, JAR histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), 22098930 bytes; [prova binária estática](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão 1.4.4-1.21, build Iron's 3.16.2/NeoForge 21.1.244/Azure 3.1.0/Ace's 1.2.7.2 versus pack Iron's 3.16.3/NeoForge 21.1.250/Azure 3.1.11/Ace's 1.2.7.2. Host source Iron's 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`; igualdade integral dos métodos/JARs/hosts não provada. `mod_license=MIT` versus TEMPLATE_LICENSE PolyForm Shield é conflito: fatos/paráfrases/permalinks, sem copiar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

[Guia oficial][guide], parafraseado: livrar-se da loucura Eldritch. Consumer reseta attachments DTE específicos: **não é cleanse geral de efeitos nocivos**. Insanity é **default false**. `#allowCrafting/#allowLooting` devolvem enableInsanitySystem; registro incondicional não comprova scroll disponível. Quando enabled, outros gates/loot/learning host ainda importam; config efetiva/rota Survival **NÃO VERIFICADAS**. [Obtenção][acquisition], [config][config], [elegibilidade host][host-acquisition].

## Ingresso, settlement e estado

1. **Defaults:** Epic, max nível1, LONG10ticks=0.5s base; cast efetivo host `round(10×(2−softCap(CAST_TIME_REDUCTION)))`. Mana `int((75+10(L−1))×MANA_MULTIPLIER)`, neutra75 no L1; cooldown default25s=500ticks antes de modifiers; sem recast próprio. Base/per-level power1/1 declara P, mas o reset não lê P: Holy/SPELL_POWER não amplia a limpeza. [Spell][spell], [fórmulas][formulas].
2. **Gate servidor:** `#canBeCastedBy` falha para ServerPlayer com Insanity disabled. Quando enabled e ambos attachments existem, falha se `meter≤0 && !IS_INSANE`. Attachments ausentes ou `meter≤0 && IS_INSANE=true` delegam ao super, sem esse failure local. A guarda de falha é ServerPlayer; não generalizar para chamadas diretas de onCast/mobs/clientes. [Admissão][admission].
3. **Ordem host:** admissão/pre-cast precedem iniciar LONG; wrapper publica SpellOnCastEvent e debita conforme origem/creative antes do reset. Estado pode mudar durante o cast; onCast não revalida enableInsanitySystem e não devolve mana no ramo sem efeito. [Wrapper][host-cast], [reset][reset].
4. **Reset:** onCast exige `hasData(INSANITY_METER)` e `hasData(IS_INSANE)`. Se meter>0, escreve meter0 e IS_INSANE=false; se meter≤0 ou falta attachment, apenas tenta mensagem ao ServerPlayer e mantém o estado. Todos ramos chamam super.onCast. **meter0/IS_INSANE=true pode passar no gate e permanecer true após cast cobrado**. Não há removeEffect, heal, dano, teleporte ou alvo remoto. [Reset][reset].
5. **Origem do estado:** registry dá meter0/flagfalse, serializados via Codec.INT/BOOL. `ServerEvents#onPlayerCastEvent` incrementa no SpellPreCastEvent Eldritch quando enabled, até max default15, marcando IS_INSANE ao máximo. O método não retorna depois do seu veto Silence nem testa cancelamento antes desse incremento. Meter nessa fase não confirma sucesso terminal; Exorcism é Holy por default. [Attachments][attachments], [evento][insanity-source], [config][config].
6. **Darkness/cleanup:** PlayerTickEvent.Post tenta Darkness110ticks/amp9 a cada100ticks do player com flagtrue, **sem testar enableInsanitySystem ali**. Reset bem-sucedido impede novas aplicações por essa condição, mas não remove Darkness já aplicada/efeitos terceiros. Desligar config não demonstra limpar flags antigas. Codecs não provam sync cliente/cópia na morte/retomada segura; QA do owner continua aberto. [Ticks][insanity-tick], [reset][reset], [attachments][attachments].

## Matriz para perks

| Eixo | Valor / consumidor / fase | Boundary real / limite | QA |
|---|---|---|---|
| Dano / tipo / cura | Sem hurt/heal/DOT/DamageSource; escola Holy classifica a spell. [Reset][reset]. | Dano/type/crit/heal **N/A**; power não é input do reset. Dano/regen por temática exige outro contrato. | Q1/Q3 |
| Alcance / targeting / área | Self; dois attachments do caster, sem ray/LOS/vítima/área. [Reset][reset]. | Range/área ofensiva **N/A**. Self→aliado/área sem resolver seguro identificado: **⛔ SEM_HOOK_SEGURO**; observer não autoriza escrever em outras entidades. | Q2/Q3 |
| Projétil / summon / mundo | Sem entidade lançada/invocada/hitbox/speed/pierce/AI/cap, bloco/fuel/stamina/HP adicional. [Reset][reset]. | Projétil/summon/mutação de bloco **N/A**; não modelar “alma expulsa” como entidade inexistente. | Q3 |
| Tempo / cooldown | LONG10ticks, cast efetivo com CAST_TIME_REDUCTION, cooldown25s, sem janela recast. [Spell][spell], [host][formulas]. | Atributos cast/cooldown **NATIVE_ATTRIBUTE**, cooldown **CONFIG_NATIVE** e evento pré-inserção no contrato comum; não controlam Darkness110/100 ou incremento Insanity. | Q1/Q4 |
| Mana / nível | `int((75+10(L−1))×config)`, default nível1; pagamento pré-reset no wrapper. [Spell][spell], [wrapper][host-cast]. | `SpellOnCastEvent#setManaCost/setSpellLevel` **HOOK_VERIFICADO** genérico; elevar L não altera reset nem recalcula custo automaticamente. Adapter/sync **CONTRATO_CONDICIONAL**; sem refund por heurística. | Q1/Q4 |
| Gate / config | COMMON enableInsanitySystem=false/max15; aquisição e admissão ServerPlayer consultam enable. [Config][config], [tipo][config-type], [gate][admission]. | **CONFIG_NATIVE** global, não perk por jogador. Max meter não é custo/quantidade limpa; sem API de gate per-player específica provada. | Q1/Q2 |
| Estado / limpeza | Com ambos attachments+meter>0:0/false; ausentes ou meter≤0: mensagem/no reset. Sem removeEffect. [Reset][reset]. | Entity#setData é armazenamento, não contrato de cleanse com admissão/custo/sync. Sem evento de reset mutável/cancelável local: extensão **⛔ SEM_HOOK_SEGURO** até adapter owner validar. | Q2/Q3 |
| Persistência / sync / dedup | Codecs serializam meter/flag; incremento pré-cast e Darkness a cada100ticks com flagtrue. [Attachments][attachments], [incremento][insanity-source], [ticks][insanity-tick]. | Não manter espelho RPG nem inferir estado pela Darkness. Morte/relog/restart/sync e tentativas canceladas **PENDING**; anúncio não é commit de cleanse. | Q2/Q4 |

## Ownership, concepção e QA

DTE possui Insanity/attachments/config/callbacks; Iron's possui mana, admissão e cooldown. RPG Skill Tree/BA devem correlacionar cast→execução→mudança real dos estados antes de recompensa, sem reset paralelo. Enshrouded possui Shroud/exposure: afinidade Holy não permite conversão/remoção desses estados. Assinatura ocupada: purge específico de Insanity; cleanse universal/terceiros exigiria magia/adapter e contrato próprios.

- **Q1:** config servidor/cliente enabled/disabled, scroll/learning/origem/creative, mana75/cast10/cooldown500 neutros/modifiers e sem crédito por registro apenas.
- **Q2:** attachments ausentes/presentes, meter negativo/0/positivo e flagfalse/true, estado mudado durante LONG, Silence/Metaphysical/cast cancelado e listeners.
- **Q3:** ambos resets apenas no ramo positivo, mensagem sem efeito após pagamento, Darkness antiga/efeitos terceiros, nenhum cleanse fora do contrato.
- **Q4:** próximo PlayerTick100, config desligada com flag antiga, morte/logout/restart/save/sync, dedicado/cliente/multiplayer e dedup Mastery. **Todos PENDING**; sem runtime/adapter/Stage novo.

[registry]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/SpellRegistries.java#L141-L146
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/holy/ExorcismSpell.java#L27-L58
[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L30
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L182-L183
[acquisition]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/holy/ExorcismSpell.java#L71-L93
[admission]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/holy/ExorcismSpell.java#L95-L115
[reset]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/holy/ExorcismSpell.java#L118-L145
[config]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/utils/DTEServerConfig.java#L26-L35
[config-type]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/DiscerningTheEldritch.java#L84-L85
[attachments]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEAttachmentRegistry.java#L15-L28
[insanity-source]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L87-L191
[insanity-tick]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/events/ServerEvents.java#L193-L204
[formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L346

[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L630
