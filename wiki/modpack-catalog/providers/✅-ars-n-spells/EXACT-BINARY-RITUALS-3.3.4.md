# Ars 'n' Spells 3.3.4 — cinco rituais exatos e oito proxies não semânticos

**✅ COUNTED_EXACT 5/5 apenas para IDs binários dos rituais e seus gates. ⚠️ Cross-cast, payment, Spell Loom, config e Survival não validados.**

## Artefato e prova

- Modlist física sibling: `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`, entrada #46, `ars_n_spells-3.3.4.jar`, mod ID `ars_n_spells`, versão `3.3.4`, SHA-1 `53966330a468e626cd6469259af6778a5a7d9305`.
- [CurseForge file 8881108](https://www.curseforge.com/minecraft/mc-mods/ars-n-spells/files/8881108), release NeoForge 1.21.1 (2026-09-14), **2222971 bytes**. O download oficial na [auditoria Java 21 #38336011675](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38336011675) teve ZIP íntegro e SHA-1 idêntico à modlist física.
- Workflow de inspeção isolado (não mergeado): `audit/ars-n-spells-334-static-20261012@55b23f0e6961123202ac8822d8bf41242a05bfcb`. Source público `otectus/ars-n-spells@41fac17065c381104b17fdaab307d89ba21b49ab` é 3.3.3, não substitui o bytecode de 3.3.4.

## Cinco IDs rituais no JAR físico

`com.otectus.arsnspells.rituals.RitualRegistryHandler.registerRituals()` possui exatamente **cinco** invocações `RitualRegistry.registerRitual`; `ModList.isLoaded("irons_spellbooks")` separa a primeira identidade incondicional das outras quatro. Cada classe do JAR expõe `REGISTRY_PATH` e forma seu `ResourceLocation` no namespace `ars_n_spells`. O entrypoint `ArsNSpells` referencia `registerRituals()`.

| # | Registry ID | Classe física | Condição |
|---:|---|---|---|
| 1 | `ars_n_spells:spell_uninscription` | `SpellUninscriptionRitual` | `ALWAYS` |
| 2 | `ars_n_spells:mana_infusion` | `ManaInfusionRitual` | `IRONS_GATED` |
| 3 | `ars_n_spells:spell_transcription` | `SpellTranscriptionRitual` | `IRONS_GATED` |
| 4 | `ars_n_spells:mana_well` | `ManaWellRitual` | `IRONS_GATED` |
| 5 | `ars_n_spells:spellbook_binding` | `SpellbookBindingRitual` | `IRONS_GATED` |

Marcadores auditados: `RITUAL_REGISTRATION_CALLS=5`, `IRON_SPELLBOOKS_RITUAL_GATE=True`, `RITUAL_GATE_ORDER=UNINSCRIPTION_BEFORE_IRONS_CHECK_BEFORE_FOUR_OTHERS`, `ENTRYPOINT_TO_RITUAL_REGISTRAR=True`.

## Eight proxy slots are not additional spells

O JAR declara `ArsCrossProxyRegistry.POOL_SIZE = 8`, `CrossModSpellComponents.PROXY_POOL_SIZE = 8`, prefixo `ars_n_spells:ars_cross_`, loop `DeferredRegister.register` e bootstrap condicionado à presença do Iron's. Os oito nomes `ars_cross_1` ... `ars_cross_8` são **identidades técnicas de transporte** no native spell wheel, cujo payload é um spell Ars serializado, não oito novas magias. Evidências: `PROXY_POOL_SIZE=8`, `PROXY_REGISTER_STATIC_LOOP_BODIES=1`, `PROXY_REGISTERED_ONLY_WHEN_IRONS_LOADED=True`, `PROXY_SEMANTIC_ROOTS_ADDED=0` e `RESULT=EXACT_FIVE_STATIC_RITUAL_IDENTITIES_PLUS_EIGHT_NON_SEMANTIC_PROXIES`.

## Limites e deduplicação

- Iron's está na modlist, satisfazendo o gate físico de presença, mas o teste **não executou** os rituais. Sem verificação de payload, tarifas, debit/refund, fontes de mana, cooldown, carrier revision/protocol 7, Spell Loom, loot, reload, UI, MP ou Survival. Hooks exatos 3.3.4 seguem fail-closed até inspeção específica.
- Ars Nouveau mantém authority de seus spells/Source/Ritual Brazier; Iron's mantém seu host/casting/wheel; Ars 'n' Spells mantém bridge e unificação provider-native; Black Arcana conserva casting e runtime mágico próprios sem um segundo pagamento; RPG Skill Tree fornece apenas progressão contratual.
- Cinco rituais já existentes: `COUNTED_RELEASE_BOUNDED → COUNTED_EXACT` para **identidade estática somente**, +0 objetos novos; campanha **✅ 11/39 exatos / ⚠️ 28/39 pendentes**; mínimos **1851 global / 1849 escopo** inalterados, denominador completo desconhecido; Stage 06.05 🟡.
- Clean-room: apenas evidência observável de hash, class names e registrar; nenhum código/asset do provider copiado.
