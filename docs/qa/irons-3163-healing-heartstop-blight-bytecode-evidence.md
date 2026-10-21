# Iron's 3.16.3 — evidência binária de Heartstop, Heal, Greater Heal e Blight

**Status:** ✅ JAR **publicado** inspecionado estaticamente com Java 21; ⚠️ sem prova de eventos NeoForge em jogo, do JAR físico instalado, do HP recuperado ou da mortalidade em remoção. **Stage 06.05 🟡**, sem merge/promoção.

## Provenance da inspeção

- **Run:** [GitHub Actions #38834814254](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38834814254), `inspect_published_provider_jar` **SUCCESS**, com `./gradlew catalogQaProbeJar jar` BUILD SUCCESSFUL e isolamento do QA companion PASS no mesmo run.
- **Artefato publicado:** CurseForge file ID **8680204**, `irons_spellbooks-1.21.1-3.16.3.jar`, tamanho **13.890.046 bytes**, SHA-256 `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`. O SHA é validado **antes** da leitura pelo coletor.
- **Coletor:** [`irons_3163_heal_heartstop_blight_bytecode.py`](./irons_3163_heal_heartstop_blight_bytecode.py), `javap -p -c` nas **9 classes** relacionadas a esses **4 spells**. Emite apenas `healing-heartstop-blight-evidence.json` com metadados/campos de método, não copia bytecode/classe/JAR. O autoteste fail-closed próprio também passou.
- **Fonte comparativa:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, **39 links versionados em 11 arquivos**, todos conferidos quanto a caminhos e linhas.
- **Falha de ferramenta corrigida:** [Actions #38834564574](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38834564574) terminou com FAIL_CLOSED porque o coletor exigia ordem de carregamento do receptor `NeoForge.EVENT_BUS` antes/depois da criação do objeto `SpellHealEvent`. O Java pode preparar o receptor antes. O teste foi corrigido para comprovar a **invocação `post` antes da invocação `LivingEntity.heal`**, sem relaxar essa exigência. [#38834814254](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38834814254) é a prova GREEN.

## Resultados do JSON e seu alcance

| Objeto | Marcadores binários confirmados | Limite |
|---|---|---|
| `HeartstopSpell.onCast` | aplica `HEARTSTOP` ao caster e usa `getSpellPower` | ✅ instruções presentes; ⚠️ duração/multiplicadores e efeito realmente ativo exigem runtime |
| `ServerPlayerEvents.onBeforeDamageTaken` | verifica `HEARTSTOP`, lê `getOriginalDamage`, acumula via `addHeartstopDamage`, chama `setNewDamage` | ✅ callback/marcadores estáticos; ⚠️ quantidade efetivamente interceptada, prioridade e dano final não medidos |
| `HeartstopEffect.onEffectRemoved` | contém **tanto `hurt` quanto `kill`**, lê e depois zera acumulador | ✅ ramo `kill` presente; **`real_kill_at_low_tick_count=NOT_PROVEN_BY_STATIC`** |
| `SyncedSpellData.addHeartstopDamage` | usa campo do acumulador e sincronização | ✅ marcação compilada; ⚠️ NBT, relog e idempotência de callback ainda não executados |
| `HealSpell.onCast` | `SpellHealEvent` é publicado **antes da chamada `heal`** | ✅ ordem relativa de invocações `post`→`heal`; **`net_hp_recovery=REQUIRES_LIVE_HP_SNAPSHOT`** |
| `GreaterHealSpell.onCast` | consulta `getMaxHealth`, publica `SpellHealEvent` antes da chamada `heal`, envia pacote visual | ✅ estrutura compilada; ⚠️ conclusão de LONG e HP efetivo não testados |
| `BlightSpell.onCast` | usa `TargetEntityCastData` e adiciona `BLIGHT` ao alvo | ✅ caminhos presentes; ⚠️ alvo/LOS/claims no pack não medidos |
| `BlightEffect.reduceHealing` | callback `LivingHealEvent` modifica `setAmount` | ✅ chamada presente; multiplicadores finais dependem de outros listeners |
| `BlightEffect.reduceDamageOutput` | callback `LivingIncomingDamageEvent` modifica `setAmount` | ✅ chamada presente; **`SOURCE_PINNED_FORMULAS_NOT_RUNTIME_MEASURED`** |

O resultado `evidence=PUBLISHED_JAR_JAVAP_STATIC_HEALING_HEARTSTOP` não significa equivalência do código-fonte upstream com todas as transforms do NeoForge instalado, nem que o jogo aplicou cada ramo.

## Regras fail-closed para perks e Mastery

- **Heartstop:** ⛔ não encurtar duração, dispelar ou reconfigurar dano terminal sem testar remoção com `tickCount<=60`, morte, logout/relog e acumulador. `LivingDamageEvent.Pre` é contribuição derivada ao efeito; nenhum desses eventos constitui novo cast.
- **Heal / Greater Heal:** `SpellHealEvent.getHealAmount` é **quantidade proposta**, não delta de HP recuperado. Não premiar `SpellHealEvent`, `LivingHealEvent` e HP delta como três curas distintas. `getMaxHealth` usado no evento de Greater Heal pode exceder o déficit real.
- **Blight:** efeito modifica `LivingHealEvent` da **entidade curada** e `LivingIncomingDamageEvent` quando a **entidade que causou o dano** tem BLIGHT; não atribuir eventos derivados do debuff à conjuração sem vínculo causal garantido.
- **Autoridades:** Iron's governa cura, dano, mana, cooldown e lifecycle; Black Arcana não cria segundo pipeline e RPG Skill Tree permanece sibling de progressão por contratos reais.

## Gate físico separado

[Protocolo de aceitação no modpack](./irons-3163-healing-heartstop-blight-acceptance.md): executar em cópia segura de servidor NeoForge **21.1.248** / Iron's **3.16.3** com hash do JAR **realmente instalado**, logs de `SpellHealEvent`/`LivingHealEvent` e delta de HP, event listener de `BlightEffect` para cura e dano, e cenários perigosos de `HeartstopEffect.onEffectRemoved` com backup do mundo. **Nada disso foi executado nesta tranche**.

**Cobertura semântica inalterada:** Iron's ✅ 110 magias inventariadas, 🟡 **32/110 dossiês causais individuais (29,09%)**; piso global 1.856 / 1.854, denominador global desconhecido; Stage 06.05 🟡 e Stage 09 pendente. Não promover por esta prova.
