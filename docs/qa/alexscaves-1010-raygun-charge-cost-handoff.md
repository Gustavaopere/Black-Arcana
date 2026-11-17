# Raygun 1.0.10 — consumo durante uso e Energy Efficiency (descoberta SHA-exata)

**Status:** 🟡 investigação estática read-only; o Raygun continua ⚠️ parcial. Não modificar runtime, X-Ray, hooks, índices ou Stage.

## Autoridade e recorte

Modlist física do sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, Minecraft 1.21.1, NeoForge, Java 21. A classe `RaygunItem.class` possui SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`.

Há evidências históricas de `ChargeUsed`, `UseTime`, `hasCharge < 1000` e recarga com `URANIUM_ROD`; os fluxos de munição já estão selados na [PR #1101](https://github.com/Gustavaopere/Black-Arcana/pull/1101). O bytecode `onUseTick` também referencia `ENERGY_EFFICIENCY @246`, mas **a fórmula completa de consumo por tick, os intervalos reais de disparo e sua interação com o estado da stack permanecem não certificados**.

## Perguntas desta etapa

1. Em quais métodos nativos aparecem chamadas de `getCharge`, `setCharge`, `getUseTime`, `setUseTime` e `hasCharge`?
2. Qual é a sequência de operações observável junto de `ENERGY_EFFICIENCY` e dos caminhos de atualização de carga?
3. O bytecode de `acInventoryTick` participa de outro caminho de escrita de estado? Que campos são consultados antes de atualizar?
4. Quais fatos estáticos podem ser fixados sem presumir autoridade do servidor, aceitação de C2S ou safe hook de perk?

## Procedimento

A [sonda read-only](alexscaves_1010_raygun_charge_cost_probe.py) executa primeiro a auditoria SHA-exata de todos os **26 métodos** e a comparação integral com o [manifesto de fluxo do Raygun da PR #1102](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json), no JAR publisher original. Somente então inspeciona nove métodos selecionados e imprime referências/operadores limitados:

- `onUseTick` (523 instruções) e `acInventoryTick` (109);
- `use`, `hasCharge`, `getCharge`, `setCharge`, `getUseTime`, `setUseTime`, `getBarWidth`;
- janelas compactas de operadores próximos a `ENERGY_EFFICIENCY @246` e à região de ativação do uso.

O relatório **não** publica o corpo completo do JAR de terceiros, restringe número de callsites e tamanho total, e não tem permissão para alterar o provider.

O [workflow dedicado](../../.github/workflows/alexscaves-1010-raygun-charge-cost.yml) primeiro executa regressões sintéticas e coleta `UNSEALED_CHARGE_COST_DISCOVERY`. Após conferir log e conteúdo realmente extraídos, fixar `EXACT-RAYGUN-CHARGE-COST-1.0.10.json`, documentar somente conclusões sustentadas pelos ramos e repetir `--snapshot` com a CI geral. Sem evidência física da fórmula completa, ela permanecerá `NÃO VERIFICADO`.

## Barreiras

`static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `server_owned_charge=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`; `provider_universe_closed=false`. Sem perfis de exploração C2S, sem reinterpretação de `getUseDuration=72000` como cooldown e sem inflar os denominadores.
