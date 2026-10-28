# UniqueAbstractSpellCastingMob — mobs com animação

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`UniqueAbstractSpellCastingMob.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractSpellCastingMob.java) — `entity/mobs/UniqueAbstractSpellCastingMob.java`
- [`UniqueAbstractMeleeCastingMob.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/UniqueAbstractMeleeCastingMob.java) — `entity/mobs/UniqueAbstractMeleeCastingMob.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`UniqueAbstractSpellCastingMob extends AbstractSpellCastingMob implements GeoEntity, IMagicEntity` e possui funções de iniciar/cancelar cast, `MagicData`, spell sync, controllers GeckoLib e NBT. `UniqueAbstractMeleeCastingMob` a estende e implementa `IAnimatedAttacker`, acrescentando lógica de movimento/animação de melee. São subclasses-base para mobs de addons.

## Targeting, geometria, custos e duração

Alvo vem de AI/`LivingEntity` e da magia Iron's do consumidor. Nenhum mob id, loot, projétil ou feitiço nasce automaticamente destas classes de apoio.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Evitar duplicar `initiateCastSpell`, cooldown, persistência de MagicData ou eventos de Mastery. Casting de mobs e animação não são automaticamente magia Black Arcana.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. Código-fonte Ace compilou contra Iron's `3.16.2` no build pinado; pack usa `3.16.3` segundo inventário, exigindo teste efetivo.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
