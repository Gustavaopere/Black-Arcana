# Dreamless Spells 1.1.9 — ABI exata das quatro magias e do overlay Counterspell

**Data da auditoria:** 27/10/2026
**Estado:** ⚠️ `EXACT_JAR_HASH_MATCHED / METHOD_CALL_REFERENCES_VERIFIED / BEHAVIOR_NOT_VERIFIED / PERK_HOOK_NOT_CERTIFIED`
**Escopo:** comprovação de classes, campos e referências simbólicas de método do JAR instalado, **não** reprodução de casting, balance ou QA no modpack.

## Artefato de autoridade e evidência limpa

- **Versão física:** `dreamless_spells-1.1.9.jar`, mod ID `dreamless_spells`, CurseForge project/file `1250250/7905334`, SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`; confirmação prévia de quatro ID roots em [EXACT-BINARY-SPELLS-1.1.9.md](EXACT-BINARY-SPELLS-1.1.9.md) e modlist física sibling #225.
- **Nova verificação de ABI:** [GitHub Actions run 40499150605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40499150605), job `122172149158`, `completed/success`, Java 21; o job validou o SHA-1, integridade do ZIP, presença de 15 classes-alvo, métodos selecionados e referências de chamadas/campos.
- **Evidência preservada:** artifact `dreamless-119-exact-symbols` ID `12731109161`, digest `sha256:1fc0c2a17d985dfbc80bccdc46aa35a8b010f7d40ff4729fee407ad210f1f3c7`; relatório textual também aparece nos logs do run.
- **Auditoria isolada:** branch `audit/dreamless-119-spell-abi-20261027` HEAD `3e88dd9749489a5e6ebf9482be5a251c30037f36`; workflow temporário não é introduzido na main por esta documentação.
- A fonte pública [`stikbug/Neoforge-Dreamless-Spells-N-Spellbooks@71f7befa81f618d07bfa023c5c82d32fdb10077a`](https://github.com/stikbug/Neoforge-Dreamless-Spells-N-Spellbooks/tree/71f7befa81f618d07bfa023c5c82d32fdb10077a) continua **release-aligned, não binary-build-equivalent**. Fórmulas e constantes citadas nas fichas legadas vêm dessa fonte, não do probe.
- A análise do binário usa `javap` transitoriamente no job e **retém apenas nomes/assinaturas e relações simbólicas necessárias à interoperabilidade**. Não transporta corpos de métodos, bytecode, código do fornecedor, configuração, assets ou textos.

## Quatro magias próprias — relações confirmadas no JAR 1.1.9

| Spell canônica | ABI/call-sites exatos identificados | O que continua sem prova física |
|---|---|---|
| `dreamless_spells:drained` | `DrainedSpell.checkPreCastConditions` e `onCast` referenciam `DSSEffects.EMPTIED_EFFECT`; `checkPreCastConditions` referencia `TargetEntityCastData.getTarget`, e `onCast` referencia `TargetedTargetAreaCastData.getTarget`. O método compilado `lambda$onCast$0` referencia `DSSEffects.DRAINED_EFFECT` e `LivingEntity.addEffect`. | Valor do raio 2 versus área visual 3, ausência real do limite de 5 alvos, aplicação/cancelamento sob multiplayer, duração, custo e config. |
| `dreamless_spells:dullard` | `DullardSpell.getDuration` e `getAmplifier` existem; `onCast` referencia os dois métodos, `DSSEffects.DULLARD_EFFECT`, `TargetEntityCastData.getTarget`, `LivingEntity.addEffect` e `AbstractSpell.onCast`. `checkPreCastConditions` referencia `EMPTIED_EFFECT`. | Fórmula de duração e amplifier, efeito com duração 0–1 tick, scaling de Spell Power e tooltip; não afirmados como números do bytecode 1.1.9 por este probe. |
| `dreamless_spells:doorway_effect` (`MuteSpell`) | `MuteSpell.getDuration` e `getAmplifier` existem; `onCast` os referencia ao lado de `DSSEffects.MUTE_EFFECT` e `LivingEntity.addEffect`. `checkPreCastConditions` referencia `EMPTIED_EFFECT`. | Janela de silêncio em ticks, emissão, cancelamento/mana/cooldown de um cast, alvos players/mobs e tradução runtime. |
| `dreamless_spells:jadeskin` | `JadeskinSpell.onCast` referencia `DSSEffects.JADESKIN_EFFECT`, `LivingEntity.addEffect` e `AbstractSpell.onCast`. | Multiplicadores numéricos, duração por nível, atributos modificados, acumulação com gear/Curios e aplicabilidade durante efeitos cruzados. |

**Nota:** `lambda$onCast$0` é um **método compilado** usado por Drained. Sua presença não autoriza contar uma conjuração separada nem declarar uma quantidade dinâmica de vítimas. Referência `addEffect` é um call-site estático, não prova de aplicação efetiva.

## Mute — camada de cancelamento do Iron's

A classe física `net.Iceforkkk.DreamlessAditions.events.ServerEvents` possui `onPlayerCastEvent`. O método **referencia `DSSEffects.MUTE_EFFECT`, `SpellPreCastEvent.setCanceled` e `MobEffectInstance.getDuration`**. Trata-se de interposição de um addon no pipeline nativo do Iron's Spells.

A inspeção **não afirma** que esse cancelamento dispara para todo caster, todo spell, toda tentativa de cast ou apenas no servidor, pois ramos/condições/side effects não foram extraídos. Para perks, spell analytics e Mastery, **não** contabilizar tanto o evento negado quanto a aparição/ausência de efeito como duas conjurações. Black Arcana e RPG Skill Tree não devem introduzir um segundo cancelamento ou um segundo custo/refund.

## Counterspell — divergência estrutural de holders da escola Empty

A evidência binária traz um fato mais estreito, porém mais forte, que a inferência apenas do source:

1. `CounterspellSpellMixin.getSchoolType` **existe no JAR exato** e referencia o campo **`net.Iceforkkk.DreamlessAditions.spells.DSSSpells$Schools.EMPTY`**.
2. `DSSSpells$Schools` expõe **`SCHOOLS`** (`DeferredRegister<SchoolType>`) e **`EMPTY`** (`Supplier<SchoolType>`), com `registerSchool` referenciando `SCHOOLS`.
3. `DSSSchoolRegistry` expõe outro `DSS_SCHOOLS` (`DeferredRegister<SchoolType>`) e outro `EMPTY` (`Supplier<SchoolType>`), com `register` referenciando `DSS_SCHOOLS` e `DeferredRegister.register`.
4. A classe entrypoint `Dreamless_Spells` também está presente no mesmo binário, mas **o probe limitado não certifica quais caminhos de registro realmente são executados no startup**, nem se o holder do mixin está bound.

**Conclusão permitida:** existe **separação estrutural das superfícies de registro e do holder referenciado pelo mixin** no JAR 1.1.9, exatamente como sinalizado na revisão release-aligned. **Não existe prova aqui** de crash, holder unbound, school mal resolvida ou sucesso do Counterspell durante jogo. Essa rota continua **⛔ fail-closed para qualquer bridge ou reclassificação**.

## Gates pendentes antes de perks e de homologação

- Verificar em processo NeoForge real, com Iron's Spells 1.21.1-3.16.3, o startup, a escola Empty efetivamente bound e a consulta de `CounterspellSpell.getSchoolType`; capturar ID/identidade sem mascarar uma exceção.
- Medir em servidor Drained com 6+ vítimas, filtro de friendly-fire, alvos entre raios 2 e 3, troca de `Emptied` durante cast e event failure.
- Medir Dullard e Mute em todos os níveis: duração em ticks, amplitude de status, cancelamento, mensagem ao jogador e autorização de mobs.
- Confirmar mana, cooldown e spell result depois do `SpellPreCastEvent` cancelado, usando uma chave causal por tentativa, e política de exactly-once antes de Mastery.
- Confirmar aquisição Survival da `empty_rune`, aplicação residual de `Emptied` depois de swap e efeitos reais de Jadeskin com attributes do modpack.
- Contratos de fonte e números só podem ser promovidos quando auditados contra **classfile exato** ou medidos no runtime físico; não presumir API de alteração a partir de nomes.

**Status e contadores:** Quatro ações mágicas já `COUNTED_EXACT` no [registro físico](EXACT-BINARY-SPELLS-1.1.9.md); este documento adiciona **+0 identidades**. `PERK-READY-CERTIFICATIONS.json` intocado: **Dreamless 0/5** no recorte documental (4 spells + 1 overlay não contabilizado como spell extra); benchmark global **138/2075** na main consultada em 27/10/2026. Nenhum hook mutador foi homologado, nenhuma implementação Black Arcana foi adicionada e nenhum Stage foi promovido. O provider e Iron's conservam suas authorities respectivas.
