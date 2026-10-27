# Overlay: Counterspell -> Empty school

## Escopo

Dreamless 1.1.9 inclui `CounterspellSpellMixin`, ativado por `src/main/resources/dreamless.mixins.json`.

Target:

`io.redspace.ironsspellbooks.spells.ender.CounterspellSpell`

Override:

`getSchoolType()` retorna `DSSSpells.Schools.EMPTY.get()`.

A intenção aparente é reclassificar o Counterspell do Iron's como magia Empty/anti-mago.

## Problema estrutural

Há duas declarações de escola Empty no source:

### Registry efetivamente registrado pelo entrypoint

`DSSSchoolRegistry.EMPTY`

O construtor principal chama `DSSSchoolRegistry.register(modEventBus)`.

### Registry referenciado pelo mixin

`DSSSpells.Schools.EMPTY`

`DSSSpells.Schools` cria outro `DeferredRegister<SchoolType> SCHOOLS`, mas não possui método de registro chamado pelo entrypoint e nenhuma chamada `SCHOOLS.register(eventBus)` foi localizada.

Ambos usam o mesmo resource id conceitual `dreamless_spells:empty`, mas são holders produzidos por registries distintos no código.

## Risco

O mixin está ativo e pode ser chamado sempre que o Iron's consulta a school de Counterspell. O holder retornado não possui evidência de ter sido bound ao registry.

Possíveis resultados que precisam de runtime QA, sem escolher um deles antecipadamente:

- holder access failure/crash;
- objeto não correspondente à school registrada;
- comportamento aparentemente correto por efeito de inicialização não observado no source;
- incompatibilidade com config/SchoolRegistry/attributes.

## Estado canônico

**FAIL-CLOSED. Counterspell NÃO deve ser considerado seguramente reclassificado como Empty até validação no JAR instalado.**

Na taxonomia do catálogo, Counterspell continua sendo uma spell nativa do Iron's com um **overlay Dreamless pendente de QA**, e não uma quinta spell registrada pelo Dreamless.

## Regra Black Arcana

Não:

- registrar terceira school Empty;
- mixinar Counterspell novamente;
- alterar school via event/config só para mascarar o holder;
- duplicar custo/cooldown/settlement de Counterspell.

Se o runtime confirmar que o mixin está quebrado, qualquer correção deve ser uma bridge/compat explícita, testada contra Iron's 3.16.3, mantendo um único `SchoolType` canônico (`DSSSchoolRegistry.EMPTY` ou outra decisão documentada).

## Testes obrigatórios

1. Abrir registry após startup e resolver `dreamless_spells:empty`.
2. Executar `CounterspellSpell#getSchoolType()` no dedicated server.
3. Confirmar ausência de holder-not-bound exception.
4. Comparar identidade/ID retornado com `SchoolRegistry.getSchool(dreamless_spells:empty)`.
5. Castar Counterspell e verificar power/resistance/damage classification/cooldown.
6. Testar interação com Mute e outros addons que observam Counterspell/school.

## Atualização de ABI exata 1.1.9 — 27/10/2026

A [auditoria do JAR físico dreamless_spells-1.1.9.jar](../EXACT-1.1.9-SPELL-CAST-AND-COUNTERSPELL-ABI-20261027.md) (SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`, run [#40499150605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40499150605)) confirmou estas relações de código **sem importar corpos de método**:

No JAR exato, `CounterspellSpellMixin.getSchoolType` referencia `DSSSpells$Schools.EMPTY`. `DSSSpells$Schools` declara seu próprio `SCHOOLS` (`DeferredRegister<SchoolType>`) e `EMPTY` (`Supplier<SchoolType>`), enquanto `DSSSchoolRegistry` declara separadamente `DSS_SCHOOLS` e `EMPTY`, com `register` referenciando `DeferredRegister.register`. A divergência de holder/registrador é **estruturalmente comprovada**; não se comprovaram crash, holder unbound ou caminho de startup executado. A integração permanece bloqueada até observar o `getSchoolType` real.

**Status:** `EXACT_BINARY_METHOD_REFERENCES` (estático) · `SOURCE_ALIGNED_NUMBERS_NOT_BINARY_PROVEN` · `physical_qa=NOT_TESTED` · `mutating_hook=NOT_VERIFIED`. Nenhum registro novo, certificação de perk, custo adicional ou segundo pipeline Black Arcana. **⛔ Integração Counterspell fail-closed.**
