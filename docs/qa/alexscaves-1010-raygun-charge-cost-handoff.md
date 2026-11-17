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

## Resultado SHA-exato extraído do JAR — CI #43993551789

A [auditoria de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/43993551789) concluiu com **12/12 regressões sintéticas**, SHA-256 do JAR publisher confirmado, replay dos 26 fingerprints e do manifesto de fluxo da PR #1102, e coleta limitada de **24 referências de carga/uso em nove métodos**. O resultado observado foi fixado em [EXACT-RAYGUN-CHARGE-COST-1.0.10.json](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-CHARGE-COST-1.0.10.json).

### 1. Tempo de uso e intervalo de consumo

Em `RaygunItem.onUseTick(Level,LivingEntity,ItemStack,int)`:

- `getUseDuration @3`, `iload 4 @6`, `isub @8` e `istore 5 @9` definem **`T = duração declarada - ticks restantes`**. O `getUseDuration` já selado devolve `72000`; não significa cooldown.
- `bipush 15 @11` e `if_icmpge @19 → 32` selecionam `T/15` antes de 15 ticks ou o literal `1.0f` depois; o valor é armazenado no float slot 7 em `@33`. No trecho de débito, `fload 7 @270`, `fconst_1 @272`, `fcmpl @273` e `iflt @274 → 322` barram o caminho enquanto o valor for menor que 1.
- `ENERGY_EFFICIENCY @246` e `ACCompat.enchantLevel @249` alimentam o inteiro slot 15. A sequência `iconst_2 @254`, `iload 15 @255`, `i2f @257`, `1.5f @258`, `fmul @261`, `f2d @262`, `Math.floor @263`, `d2i @266`, `iadd @267` e `istore 16 @268` determina, para níveis não negativos, **intervalo inteiro `I = 2 + floor(1.5 × nível ENERGY_EFFICIENCY)`**.
- `iload 5 @277`, `iload 16 @279`, `irem @281`, `ifne @282 → 322` habilitam o caminho somente quando `T % I = 0`. Para os níveis `0,1,2,3,4`, os intervalos aritméticos são respectivamente `2,3,5,6,8` ticks, **sem assegurar que cada tick elegível execute o débito**.
- Há guarda de jogador criativo: `Player.isCreative @296` seguido de `ifne @299 → 322`. Um caminho que prossegue lê `getCharge @303`, usa `iconst_1 @311` e `iadd @312`, aplica `Math.min(...,1000) @316` e grava `setCharge @319`. A expressão estática desse caminho é **`ChargeUsed' = min(ChargeUsed + 1, 1000)`**. É gasto de carga utilizada, não incremento de energia disponível.

**Interpretação:** o encantamento de eficiência aumenta o intervalo entre oportunidades de débito, condicionado à rampa inicial, ao módulo do tempo de uso e aos outros guards da ação. Não existe evidência de que esse custo possa ser alterado com segurança por uma perk; nem prova de autorização e reconciliação C2S da tag.

### 2. Recuperação solar em acInventoryTick

Na classe nativa, `acInventoryTick(ItemStack,Level,Entity,boolean)` possui 109 instruções e 18 branches (selo pré-existente). O recorte atual demonstra:

- Guard de execução não cliente: `Level.isClientSide @39` e `ifne @42 → 146`. O ramo examinado em seguida lê `SOLAR @46`, `ACCompat.enchantLevel @49`, `ifle @52 → 230` e a flag JVM slot 5 em `iload @55 / ifne @57 → 230`. Essa flag nasce da verificação de uso do item (`LivingEntity.getUseItem @15` e `Object.equals @19`), de modo que o caminho de recuperação exige a flag igual a 0.
- `getCharge @61`, `iload 7 @66`, `ifle @68 → 143`: a recuperação só prossegue com **`ChargeUsed > 0`**.
- `Level.getRandom @72 → RandomSource.nextFloat @75`, literal `0.02f @80`, `fcmpg @82` e `ifge @83 → 143`: condição estática de sorteio **`nextFloat() < 0.02`**, não uma medição empírica de frequência.
- `Level.canSeeSky @98` deve prosseguir (`ifeq @101` é saída); `Level.isDay @105` idem (`ifeq @108`); `DimensionType.hasFixedTime @115` deve ser falso (`ifne @118`); `ACCompat.sunAboveHorizon @124` precisa retornar verdadeiro (`ifeq @127`).
- Se os guards documentados permitem, `iload 7 @131`, `iconst_1 @133`, `isub @134` e `setCharge @135` escrevem **`ChargeUsed' = ChargeUsed - 1`**; `setUseTime(...,0) @140` aparece na mesma região.

A recuperação solar é um **consumidor separado** do encantamento `SOLAR`, não o uso da `URANIUM_ROD` na recarga ativa documentada na PR #1101. Os filtros solares são condições de caminho observadas em bytecode; seus efeitos reais após datapacks, alterações do jogo e ambiente físico não foram testados.

### 3. Estado temporal e outros consumidores

`acInventoryTick` lê `getUseTime @33` e pode chamar `setUseTime @206/@227` com `UseTime + 1` ou `UseTime - 1`, condicionado a outros desvios. `setUseTime` escreve o tempo anterior em `PrevUseTime` e o novo valor em `UseTime`; os métodos são do mesmo artefato SHA-exato. `getBarWidth` consulta `getCharge`, mas a inspeção deste recorte não certifica a semântica integral de HUD em runtime.

### Gate e limites

O manifesto é **descoberta read-only** com evidência de operadores exatos. A fórmula e a atualização acima descrevem caminhos nativos selecionados; **não** demonstram autorizações de update C2S, integridade do `CUSTOM_DATA`, persistência física, limites efectivos sob tags alteradas, antirreplay, QA cliente/servidor, hook mutador ou uma lista completa de efeitos/perks.

Antes de merge: repetir o workflow contra o manifesto congelado com `--snapshot`, validar a CI integral, conferir diff e sincronização da `main`. Manter `Raygun = ⚠️`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED` e `NO_MUTATION`.
