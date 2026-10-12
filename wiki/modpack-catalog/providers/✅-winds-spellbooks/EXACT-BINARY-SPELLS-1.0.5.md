# Wind's Spellbooks 1.0.5 — sete registros de spells comprovados no JAR físico

**✅ 7/7 `COUNTED_EXACT` somente para registro binário estático. ⚠️ Gameplay, configuração e Survival não verificados.**

## Âncora física e inspeção

- Modlist física `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`: `wind_spellbooks-1.0.5.jar`, mod ID `wind_spellbooks`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`.
- Publicador: [CurseForge project 1519158 / file 8485822](https://www.curseforge.com/minecraft/mc-mods/winds-spellbooks/files/8485822), versão 1.0.5, 2026-07-22, JAR **459532 bytes**.
- [Auditoria isolada GitHub Actions #38312284152](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38312284152), commit `f6d6891a08c755fef2e8ec69188cac909e68a9a0`, job `physical-discovery` **SUCCESS**. O SHA-1 do JAR oficial corresponde ao físico. Inspeção ZIP e `javap -c -p -constants` com Java 21; provider não executado.

## Prova da cardinalidade e identidades

`net.raptorzizi.wind_spellbooks.registries.ModSpellRegistry` cria `DeferredRegister` com `SpellRegistry.SPELL_REGISTRY_KEY`, namespace literal `wind_spellbooks`. O inicializador estático instancia as sete classes abaixo e faz **sete** chamadas de `registerSpell(AbstractSpell)`. Esse helper usa `AbstractSpell.getSpellName()` e chama `DeferredRegister.register(String, Supplier)`. Cada construtor fixa `ResourceLocation.fromNamespaceAndPath("wind_spellbooks", "<id>")` e `getSpellResource()` devolve a identidade correspondente. O entrypoint `WindSpellbooksMod` chama `ModSpellRegistry.register(IEventBus)`.

| # | Classe física própria | Campo de registro | Registry ID |
|---:|---|---|---|
| 1 | `WindJumpSpell` | `WIND_JUMP_SPELL` | `wind_spellbooks:wind_jump` |
| 2 | `TornadoSpell` | `TORNADO_SPELL` | `wind_spellbooks:tornado` |
| 3 | `IronSlashSpell` | `IRON_SLASH_SPELL` | `wind_spellbooks:iron_slash` |
| 4 | `AeropicSpell` | `ACROBATICS_SPELL` | `wind_spellbooks:aeropic` |
| 5 | `AlmightyPushSpell` | `ALMIGHTY_PUSH_SPELL` | `wind_spellbooks:almighty_push` |
| 6 | `WindBladeSpell` | `WIND_BLADE_SPELL` | `wind_spellbooks:wind_blade` |
| 7 | `TailwindSpell` | `TAILWIND_SPELL` | `wind_spellbooks:tailwind` |

**STATIC_REGISTER_SPELL_INVOCATIONS=7** e **ENTRYPOINT_TO_REGISTRY=present**, com sete classes concretas em `spells/wind`. O campo `ACROBATICS_SPELL` é o registro de `AeropicSpell`, ID `wind_spellbooks:aeropic`, **não** uma oitava magia. `MixinGustSpell`, `MixinInvisibilitySpell` e `MixinThrowSpell` não são spells próprios registrados.

## Deduplicação e limites

As sete magias já estavam catalogadas. Promoção `COUNTED_RELEASE_BOUNDED → COUNTED_EXACT` **somente para identidade/cardinalidade de registry estático**, **+0** novas identidades. Campanha original **6/39 exatos / 33/39 pendentes**, mínimos **1851 global / 1849 escopo** inalterados. Denominador semântico global continua desconhecido.

**⚠️ NÃO VERIFICADO:** registro real na instância carregada, versão do host Iron's em execução, configuração instalada, mana/cooldown e valores por nível, alcance, targeting, PvP, friendly-fire, recasts, efeitos em servidor, scrolls/loot, multiplayer, aquisição e Survival. Esta prova binária não é aprovação da execução do modpack.

Iron's mantém casting, mana/cooldowns de host; Wind's Spellbooks mantém suas sete spells e effects. IronSable é owner de `maelstrom`, `tempests_grasp` e `downburst` mesmo quando classificados na escola Wind. Black Arcana não duplica settlements ou integrações não provadas; RPG Skill Tree somente oferece progressão por contratos. Stage 06.05 continua 🟡.
