# Ars 'n' Spells 3.3.4 — matriz de perks/rituais com source 3.3.3

**✅ 5/5 IDs do JAR físico 3.3.4 confirmados**, com dossiês individuais aprofundados nesta branch usando *implementação pública 3.3.3*; **⚠️ comportamento/métodos exatos do JAR 3.3.4 não comprovados pela fonte anterior**. Source de referência `otectus/ars-n-spells@41fac17065c381104b17fdaab307d89ba21b49ab`, versão pública NeoForge 3.3.3, distinta da versão física 3.3.4.

JAR: `ars_n_spells-3.3.4.jar`, SHA-1 `53966330a468e626cd6469259af6778a5a7d9305`. Quatro rituais `IRONS_GATED` (Iron's Spellbooks está instalado); Uninscription é incondicional. Prova de registry físico [EXACT-BINARY-RITUALS-3.3.4.md](EXACT-BINARY-RITUALS-3.3.4.md).

| Ritual | Tipo/gate | Evidência do executor 3.3.3 | Bloqueio de perks |
|---|---|---|---|
| [Spell Uninscription](rituals/spell-uninscription.md) | `SpellUninscriptionRitual` / ANY / always | 60 ticks / AABB±3. InscriptionInputs.classify exige apenas 1 inscribed; removeAllArsEntries; sem deduplicar limpeza em RPG | ⚠️ source anterior ao JAR 3.3.4; ⛔ adapter RPG |
| [Spell Transcription](rituals/spell-transcription.md) | `SpellTranscriptionRitual` / IRONS_GATED | 60 ticks / AABB±3. InscriptionPlan/Outcome calcula transformedTargets, targetRemainder, consumedFromSource; output spawn antes de debit de stack | ⚠️ source anterior ao JAR 3.3.4; ⛔ adapter RPG |
| [Spellbook Binding](rituals/spellbook-binding.md) | `SpellbookBindingRitual` / IRONS_GATED | 60 ticks / AABB±3. kill switch antes de input; IronsSpellbookBinder.BindResult.ADDED; um scroll shrink(1), 8 native proxy ceiling | ⚠️ source anterior ao JAR 3.3.4; ⛔ adapter RPG |
| [Mana Infusion](rituals/mana-infusion.md) | `ManaInfusionRitual` / IRONS_GATED | 60 ticks / default 500 mana (1..10000). recipient UUID persistido + fallback; BridgeManager.addMana uma vez, valor líquido desconhecido | ⚠️ source anterior ao JAR 3.3.4; ⛔ adapter RPG |
| [Mana Well](rituals/mana-well.md) | `ManaWellRitual` / IRONS_GATED | contínuo / raio 8 (1..64). 2 mana/tick default (0.1..100), players intersecting AABB, BridgeManager.addMana por tick | ⚠️ source anterior ao JAR 3.3.4; ⛔ adapter RPG |

## Contratos cruzados

- O executor [AnsRitual.java](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/AnsRitual.java) implementa progress-tick server e finalização após 60 ticks para os quatro one-shot; Mana Well herda diretamente `AbstractRitual` e não pertence a esse timer.
- O método `onEnd` é o ponto factual dos rituais one-shot no source 3.3.3, não uma API pública comprovada para observer externa de perk em 3.3.4. Não inferir entrega real de XP/Mastery com base em VFX ou status do brazier.
- [AnsConfig.java](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/config/AnsConfig.java) define defaults 500 mana infusão, 8 range Mana Well, 2 regen/tick; essas quantias podem diferir na config física e no bridge de settlement.
- Binding e Transcription mutam carriers e spellbook nativos com preflight; não gravar sidecar/registrar IDs `ars_cross_1..8` via Black Arcana. Source 3.3.4 publicou revisões em payment/cast/carriers e exige auditoria própria antes de a integração funcionar.
- O RPG Skill Tree somente poderia observar sucesso verificado por hook/provider-supplied outcome, deduplicando causas. Não duplicar source charges, native cooldown, progressão nem criar segundo pool mana.

## Pendências

⚠️ Bytecode 3.3.4 para semântica de payment/cast/ritual, config em modpack, replay/restart, claims e gameplay; ⛔ hooks per-ritual e adapter progression não implementados. Os cinco rituais já estavam no denominador global, portanto +0 identidades novas; nenhuma alteração de Stage ou runtime Black Arcana.

[README](README.md) · [catálogo de rituais](rituals/README.md) · [padrão global](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
