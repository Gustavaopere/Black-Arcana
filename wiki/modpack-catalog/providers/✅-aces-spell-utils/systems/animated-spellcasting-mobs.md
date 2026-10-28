# UniqueAbstractSpellCastingMob — mobs com animação

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`UniqueAbstractSpellCastingMob.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractSpellCastingMob.java) — `entity/mobs/UniqueAbstractSpellCastingMob.java`
- [`UniqueAbstractMeleeCastingMob.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractMeleeCastingMob.java) — `entity/mobs/UniqueAbstractMeleeCastingMob.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`UniqueAbstractSpellCastingMob extends AbstractSpellCastingMob implements GeoEntity, IMagicEntity` e possui funções de iniciar/cancelar cast, `MagicData`, spell sync, controllers GeckoLib e NBT. `UniqueAbstractMeleeCastingMob` a estende e implementa `IAnimatedAttacker`, acrescentando lógica de movimento/animação de melee. São subclasses-base para mobs de addons.

`initiateCastSpell` cria SpellData, orienta ao alvo e verifica `checkPreCastConditions` no servidor; não percorre o mesmo `attemptInitiateCast` de jogador. Prepara teleport/frost-step atrás do alvo a distância 10, blood-step a 3 e dados especiais de burning-dash. Inicia MagicData com tempo efetivo da spell, `CastSource.MOB` e MAINHAND; depois chama `onServerPreCast` no servidor ([início][mob-cast]).

No passo de IA servidor, avança duração e chama `onServerCastTick` enquanto casting. LONG/INSTANT chamam `onCast` ao terminar; CONTINUOUS chama quando `(remaining + 1) % 10 == 0`, depois conclui ao fim da duração. `cancelCast` alterna flag sincronizada no servidor e chama `castComplete`; a conclusão servidor chama `onServerCastComplete(..., false)`, enquanto o cliente reseta seu estado local ([cadência][mob-tick], [cancelamento][mob-sync]).

O NBT salva/carrega `SyncedSpellData`; se estava conjurando, marca `recreateSpell`, e o próximo passo servidor reinicia via `initiateCastSpell`. Não é continuação comprovada do mesmo instante sem repetir pre-cast; testar unload/reload e dedup de efeitos. Animações são apresentação separada do hit; a subclasse melee usa look 2.5×, rotação de movimento 0.25× com limiar horizontal quadrado 0.5 e `NotIdioticNavigation`, sem definir dano/atributos de uma espécie concreta ([save/reload][mob-save], [reinício][mob-tick], [melee][mob-melee]).

## Targeting, geometria, custos e duração

Alvo vem de AI/`LivingEntity` e da magia Iron's do consumidor. Nenhum mob id, loot, projétil ou feitiço nasce automaticamente destas classes de apoio.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Evitar duplicar `initiateCastSpell`, cooldown, persistência de MagicData ou eventos de Mastery. Casting de mobs e animação não são automaticamente magia Black Arcana.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[mob-cast]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractSpellCastingMob.java#L165-L200
[mob-tick]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractSpellCastingMob.java#L133-L163
[mob-sync]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractSpellCastingMob.java#L74-L108
[mob-save]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractSpellCastingMob.java#L411-L434
[mob-melee]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractMeleeCastingMob.java#L17-L114
