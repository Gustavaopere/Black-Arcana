# MagicGunItem — invocação do spell selecionado

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`MagicGunItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/MagicGunItem.java) — `items/weapons/MagicGunItem.java`
- [`AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java) — `events/AcesSpellUtilsServerEvents.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`MagicGunItem extends MagicSwordItem`, com `isHeavyGun()` default `true` e getters de cooldown ativos/passivos default `0`. No handler `onUseItem(PlayerInteractEvent.RightClickItem)`, Ace obtém `SpellSelectionManager`, seleção atual e nível; em ramo pesado restringe à MAIN_HAND; em ramo não-pesado usa o slot correspondente à mão. O handler chama `spellData.getSpell().attemptInitiateCast(...)`, define cancellation result e cancela o evento. Há verificações preditivas de mana/cooldown/aprendizado no lado cliente, sem substituir autoridade servidor do Iron's.

## Targeting, geometria, custos e duração

SpellData selecionado pelo jogador e a mão/arma; alcance e alvo são do spell Iron's, não atributos da magic gun por si.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não disparar novo cast ao observar `RightClickItem` ou comando de cast do Black Arcana; efeito e custo já são resolvidos na chamada host. Testar ambos os slots, side cliente/servidor, sucesso/falha e compatibilidade com overrides de isHeavyGun.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
