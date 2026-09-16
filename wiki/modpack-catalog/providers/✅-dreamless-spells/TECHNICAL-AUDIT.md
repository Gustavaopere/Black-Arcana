# Dreamless Spells 1.1.9 — auditoria técnica

## Provenance

Autoridade da instalação: `dreamless_spells-1.1.9.jar` na modlist atual.

Autoridade pública de source para esta auditoria: `stikbug/Neoforge-Dreamless-Spells-N-Spellbooks@71f7befa81f618d07bfa023c5c82d32fdb10077a`, commit de 2026-04-10, mesma data da release 1.1.9. O commit imediatamente anterior da mesma data contém a atualização de receitas descrita no changelog; este SHA posterior altera apenas um nome de método interno na armadura de mineração. Classificação: **release-aligned**, não artifact-hash-proven.

## Registry efetivo

O entrypoint chama:

- `SpellRegistries.register(modEventBus)`;
- `DSSAttributeRegistry.register(modEventBus)`;
- `DSSSchoolRegistry.register(modEventBus)`.

`SpellRegistries` contém somente quatro registrations: Jadeskin, Drained, Dullard e Mute/Doorway Effect.

## Gates e divergências obrigatórias

### 1. Drained — cap de cinco vítimas não é aplicado

A classe declara `MAX_TARGETS = 5` e inicializa `AtomicInteger targets = new AtomicInteger(0)`, mas o contador nunca sofre `incrementAndGet()`/incremento equivalente. A condição `targets.get() < MAX_TARGETS` permanece verdadeira durante toda a iteração.

Consequência estática: todos os LivingEntity elegíveis na área podem receber Drained, não apenas cinco.

Integração: não adicionar cap externo silencioso. QA deve medir o runtime 1.1.9 e qualquer correção é mudança provider/compat explícita.

### 2. Drained — radius visual 3, settlement 2

No pre-cast é criada `TargetedAreaEntity` de raio 3.

No `onCast`, a variável efetivamente usada é o `radius` importado estaticamente de `FireflySwarmProjectile`; no Iron's 3.16.3 esse campo vale `2f`. As declarações locais `float radius = 3` estão em escopos que não alimentam a busca final.

Resultado estático: indicador 3; busca/settlement por distância < 2 blocos.

### 3. Dullard — tooltip/duração e scaling divergentes

Tooltip: `spellPower * 10` ticks.

Settlement: `getDuration = (int)(spellPower * 0.1)` ticks.

Com spell power neutro 5 / 10 / 15:

- mostrado: 50 / 100 / 150 ticks = 2.5 / 5 / 7.5 s;
- aplicado: 0 / 1 / 1 tick.

O guide diz “reduces spell power by 10% per level”, mas `getAmplifier()` retorna sempre `1`. O MobEffect base usa modifier `-0.1 ADD_MULTIPLIED_TOTAL`; com amplifier 1, o comportamento vanilla esperado é aproximadamente -20% independentemente do spell level, se o efeito chegar a existir.

### 4. Doorway Effect / Mute — tooltip/duração divergentes

Tooltip: `spellPower * 5` ticks.

Settlement: `(int)(spellPower * 0.1)` ticks.

Neutralmente, níveis 1–5 têm spell power 5 / 10 / 15 / 20 / 25:

- mostrado: 25 / 50 / 75 / 100 / 125 ticks = 1.25 / 2.5 / 3.75 / 5 / 6.25 s;
- aplicado: 0 / 1 / 1 / 2 / 2 ticks.

O handler `ServerEvents#onPlayerCastEvent` cancela `SpellPreCastEvent` apenas quando a entidade é `ServerPlayer`. Mobs/non-player casters com Mute não são bloqueados por esse handler.

### 5. Doorway Effect — registry/lang mismatch

ID runtime: `dreamless_spells:doorway_effect`.

O lang possui:

- `spell.dreamless_spells.mute = Mute`;
- `spell.dreamless_spells.doorway_effect.guide = ...`;

mas não possui `spell.dreamless_spells.doorway_effect` no source auditado. Como Iron's deriva o component ID do ResourceLocation da spell, o nome player-facing deve ser validado in-game.

### 6. Counterspell mixin — escola Empty duplicada/não registrada

`CounterspellSpellMixin` retorna `DSSSpells.Schools.EMPTY.get()`.

`DSSSpells.Schools` cria seu próprio `DeferredRegister<SchoolType>`, separado de `DSSSchoolRegistry`, e não expõe/não recebe uma chamada `register(eventBus)` no entrypoint. A única escola Empty explicitamente registrada é `DSSSchoolRegistry.EMPTY`.

Riscos:

- acesso a holder não registrado;
- identity split entre duas instâncias conceituais de Empty;
- crash ou school identity incorreta quando Counterspell consulta `getSchoolType()`.

Status: **FAIL-CLOSED / RUNTIME QA OBRIGATÓRIO**.

### 7. Empty Rune — aquisição survival não localizada

Dreamless registra `empty_rune`, inclui-a em `irons_spellbooks:inscribed_runes` e a usa como smithing template das armaduras Empty.

Não foi localizada em 1.1.9:

- receita de `empty_rune` a partir de Blank Rune + Empty focus;
- loot table própria para `empty_rune`;
- outro gerador/provider nativo que a produza.

O Iron's 3.16.3 contém receitas explícitas individuais para suas runas escolares, portanto a simples tag `INSCRIBED_RUNES` não prova uma rota de criação automática.

Status: **NÃO VERIFICADO / potencial blocker de survival progression**.

### 8. Emptied — gate persiste após retirar a armadura

Cada classe de armadura Empty aplica `Emptied` por 200 ticks, amplifier 3, apenas quando o player está com o set completo e ainda não possui o efeito.

Ao tirar uma peça, não há remoção imediata no source auditado. Assim, o efeito pode permanecer pelo restante dos 200 ticks e continuar satisfazendo `checkPreCastConditions` de Drained/Dullard/Mute.

QA anti-abuso: equipar set -> obter Emptied -> retirar set -> tentar cast durante janela residual.

### 9. Emptied — modificadores são fortes por amplifier 3

Base do efeito:

- Spell Resist `+0.25 ADD_MULTIPLIED_BASE`;
- Empty Spell Power `+0.05 ADD_MULTIPLIED_BASE`;
- Max Mana `-0.25 ADD_MULTIPLIED_BASE`.

Como o set aplica amplifier 3, o scaling padrão de MobEffect multiplica os valores por 4: aproximadamente +100% base Spell Resist, +20% base Empty Spell Power e -100% base Max Mana. Esse comportamento combina com a identidade “mana truly empty”, mas deve ser confirmado no pack com outros modifiers de Max Mana.

## Authority / exactly-once

- Jadeskin settlement: `DSSEffects.JADESKIN_EFFECT` no caster.
- Drained settlement: `DSSEffects.DRAINED_EFFECT` nos LivingEntity encontrados.
- Dullard settlement: `DSSEffects.DULLARD_EFFECT` no target.
- Mute settlement: `DSSEffects.MUTE_EFFECT`; o bloqueio efetivo de cast ocorre em `SpellPreCastEvent`.
- Emptied authority: armor full-set `inventoryTick`.
- Counterspell school overlay: Mixin provider-native, atualmente QA-blocked.

Black Arcana não deve duplicar qualquer uma dessas authorities.

## Testes exigidos posteriormente

1. Confirmar registry 4/4 no JAR instalado.
2. Confirmar school registry/attributes Empty.
3. Testar Counterspell com mixin ativo e verificar crash/identity.
4. Drained: 6+ targets válidos dentro de 2–3 blocos para medir cap e radius real.
5. Dullard: duração real e redução de Spell Power nos níveis 1–3.
6. Doorway Effect: duração, nome traduzido e cancelamento de casts nos níveis 1–5.
7. Mute em mobs caster vs players.
8. Confirmar aquisição de Empty Rune no pack completo; se ausente, registrar progressão bloqueada.
9. Testar Scroll Forge com Empty Gem como focus.
10. Testar loot genérico de Empty spells.
11. Equip/unequip dos três sets Empty e janela residual de Emptied.
12. Confirmar interação de `-100% base Max Mana` com mana adicional de gear/Curios.