# GenericBossEntity — fases e música

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`GenericBossEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericBossEntity.java) — `entity/mobs/GenericBossEntity.java`
- [`GenericUniqueBossEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericUniqueBossEntity.java) — `entity/mobs/GenericUniqueBossEntity.java`
- [`IPhaseEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/IPhaseEntity.java) — `entity/mobs/IPhaseEntity.java`
- [`IPhaseMusicEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/IPhaseMusicEntity.java) — `entity/mobs/IPhaseMusicEntity.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

As duas classes abstratas implementam `Enemy`, `IClientEventEntity` e `IPhaseMusicEntity`, definem `PHASE` sincronizado com default 0 e salvam/leem o inteiro `phase` em NBT. `GenericBossEntity` herda Iron's `AbstractSpellCastingMob`; `GenericUniqueBossEntity` herda Ace `UniqueAbstractMeleeCastingMob`. A enum real vai de FirstPhase=0 até TwelfthPhase=11 (incluindo grafia `NinethPhase`); `setPhase(int)` não limita a faixa ([fases][boss-phase], [estado genérico][boss-generic-state], [estado unique][boss-unique-state]).

Flags `hasCustomMusic`, `changeMusicOnPhaseChange`, `hasTransitionPhase` começam false; os índices musicais começam 0 e getters de som retornam null. `handleClientEvent(byte)` é vazio nas duas bases: ligação de evento à música pertence à subclass. Nenhum limiar de HP, bossbar, ataque, custo ou trigger de transição é definido por esses defaults ([base genérica][boss-generic], [base unique][boss-unique]).

`BossMusicManager` e `UniqueBossMusicManager` são cliente, cada um com um singleton. Constroem três `BossSoundInstance` antes de selecionar por `hasCustomMusic`, indexam `Phase.values()[getPhase()]` sem fallback local para inteiro inválido e iniciam parando `SoundSource.MUSIC`; seus sons usam RECORDS. Não presumir que flag false torna getters null seguros. Avançam em `ClientTickEvent.Pre` quando não pausado e param layers quando a interface informa morte/remoção ([construção genérica][boss-manager], [construção unique][boss-unique-manager], [tick genérico][boss-manager-tick], [tick unique][boss-unique-tick]).

`IPhaseMusicEntity` retorna UUID null e morte/remoção false por default. A base unique sobrescreve os três, mas a genérica conserva esses defaults; stop/resume fazem comparações por `.equals` de UUID. `triggerResumeMusic` só troca referência se UUID coincide e seu ramo de retomada testa literalmente `isEntityRemoved()`. `hardStop` para layers e zera o singleton, e logout cliente chama ambos; fase em NBT não persiste as instâncias/flags musicais ([interface][boss-music-interface], [identidade unique][boss-unique-id], [cleanup genérico][boss-cleanup], [cleanup unique][boss-unique-cleanup], [logout][boss-logout]).

## Targeting, geometria, custos e duração

Instância de boss efetivamente registrada por um addon; dados da fase não são efeito global ou ataque independente.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não classificar cada fase como magia nem transformar evento de música/client em autoridade de cast. Lógica real de batalha, transições e triggers pertencem à implementação concreta do boss. QA deve cobrir fase 0/11/inválida, getters null, UUID/defaults, dois bosses, pause, unload/reload, morte/remoção e logout; a ficha registra riscos do source, sem afirmar bug reproduzido no pack.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[boss-phase]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/IPhaseEntity.java#L3-L44
[boss-generic-state]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericBossEntity.java#L120-L163
[boss-unique-state]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericUniqueBossEntity.java#L155-L197
[boss-generic]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericBossEntity.java#L15-L93
[boss-unique]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericUniqueBossEntity.java#L16-L94
[boss-manager]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/boss_music/BossMusicManager.java#L24-L86
[boss-unique-manager]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/boss_music/UniqueBossMusicManager.java#L20-L80
[boss-manager-tick]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/boss_music/BossMusicManager.java#L197-L247
[boss-unique-tick]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/boss_music/UniqueBossMusicManager.java#L196-L246
[boss-music-interface]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/IPhaseMusicEntity.java#L7-L79
[boss-unique-id]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/GenericUniqueBossEntity.java#L96-L109
[boss-cleanup]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/boss_music/BossMusicManager.java#L495-L526
[boss-unique-cleanup]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/boss_music/UniqueBossMusicManager.java#L510-L541
[boss-logout]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsClient.java#L57-L66
