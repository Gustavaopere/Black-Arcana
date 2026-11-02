# Raygun 1.0.10 — barreiras estáticas de resistência e aplicação de Irradiated

## Proveniência e contrato delimitado

Continuação da [PR #1018](https://github.com/Gustavaopere/Black-Arcana/pull/1018), integrada em `Black-Arcana/main@7227673be83a650099973b2f9473a4a07739dc69`. A versão física documentada permanece `alexscaves-1.0.10-neoforge+1.21.1.jar`, JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O método de interesse é `RaygunItem.onUseTick(Level,LivingEntity,ItemStack,int):void`, digest do parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`.

A [sonda read-only](alexscaves_1010_raygun_radiation_guard_probe.py) examina exclusivamente metadados de classfile de regiões pontuais do método: `ACCompat.hurt @1041`, retorno e `ifeq @1044`, consulta da `ACTagRegistry.RESISTS_RADIATION`/predicado `Holder$Reference.is`, `ifne @1088 → 1157`, referência a `ACEffectRegistry.IRRADIATED`, `MobEffectInstance(..., 800, amplifier)`, `LivingEntity.addEffect @1119` com `ifeq @1122 → 1157`, e mensagem visual `sendMSGToAll @1154`. Não se reconstrói o CFG completo nem se assumem condições fora desses trechos.

O probe verifica ainda a declaração **publisher-default** da tag em `data/alexscaves/tags/entity_type/resists_radiation.json` do mesmo JAR, com SHA-256 e valores. A tag pode ser alterada ou ampliada pelo conjunto de datapacks em runtime; a listagem do JAR **não** é a registry efetiva do mundo nem imunidade global de todos os produtores de irradiação.

## Evidência e critérios

A [CI exata](../../.github/workflows/alexscaves-1010-raygun-radiation-guard.yml) executa **15 regressões sintéticas fail-closed**, verifica JAR, classe e método, extrai **somente** símbolos JVM, janelas curtas, saltos diretos e o inventário de tag. A primeira execução é `UNSEALED DISCOVERY` e **não** é homologação. Somente o resultado realmente observado deverá ser registrado no manifesto `EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json`, seguido de execução `--seal` na HEAD final, inspeção do diff e CI completa.

## Barreira de autoridade

Não derivar um callback de perk dos desvios ou do tag. Sem documentação e testes reais de provider/servidor, não é permitido alterar a aceitação de `Irradiated`, duração, amplifier, resistência, dano ou envio visual. `LivingEntity.addEffect` retorna um booleano; o desvio subsequente constitui apenas evidência estática do uso do retorno e não demonstra entrega final ao cliente ou eventual override de status.

O status `irradiated` possui consumidores próprios (tick, exaustão, Hazmat, heal event), que **não** recebem automaticamente as condições do produtor Raygun; consulte a [ficha do efeito](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/effects/irradiated.md). As regras do Black Arcana preservam `WorldEffectPolicy`, autoridade de servidor, claims/PvP, custos/cooldowns e não duplicação do pipeline do provider.

**Estado obrigatório:** ⚠️ parcial/condicionado; `NO_MUTATION`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`; Raygun e Tremorzilla Beam ainda pendentes (Alex's Caves 28/30). Stage 06.05 não avança por auditoria de catálogo.


## Resultado SHA-exato — primeira CI #41542778991

A [sonda de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41542778991) terminou com **15/15 regressões sintéticas aprovadas**. Depois de uma correção de variável local do parser (o objeto do método não deve ser sobrescrito pelo `re.Match` de um branch), o JAR publisher foi auditado com SHA-256 **`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`** e o método `onUseTick` digest **`b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`**. O [manifesto do guard e tag](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) foi extraído desse resultado.

A tag física `data/alexscaves/tags/entity_type/resists_radiation.json`, SHA-256 **`1bb63c275f31f6744c071cda8ced3e1225401c5aa1dff2ea7fa3c7949e46a6c4`**, tem seis valores: `alexscaves:nucleeper`, `alexscaves:radgill`, `alexscaves:brainiac`, `alexscaves:gammaroach`, `alexscaves:raycat`, `alexscaves:tremorzilla`. Não declara `replace`, cujo default para essa leitura é `false`. Esse inventário é o **default do publisher**, não demonstra o conteúdo efetivo da registry após datapacks.

| Ponto compilado | Evidência | Limitação |
|---|---|---|
| `ACCompat.hurt @1041` → `ifeq @1044` | Retorno falso salta para `@1051`; true segue para `@1047` | Não resolve o restante do CFG/controle de danos |
| `ACTagRegistry.RESISTS_RADIATION @1082` → `Holder$Reference.is @1085` → `ifne @1088` | Predicado verdadeiro salta a `@1157`; falso prossegue `@1091` | O teste refere-se à tag atual em runtime, não a imunidade global |
| `ACEffectRegistry.IRRADIATED @1097`, `MobEffectInstance(...,800,slot23) @1116`, `LivingEntity.addEffect @1119` | A solicitação nativa usa status Irradiated com duração 800 ticks e amplifier selecionado no provider | Não prova aceitação por todo alvo nem persistence/stacking |
| `ifeq @1122` após `LivingEntity.addEffect` | Retorno falso pula para `@1157`; verdadeiro segue `@1125` | Apenas ramo booleano de aceite, sem teste físico |
| `sendMSGToAll @1154` → `goto @1157` | O fluxo visual está depois dos guards observados; retorno do loop em `@953` | Emissão em código não comprova entrega da mensagem, autorização de receptor ou efeito renderizado |

**Interpretação:** na região delimitada, a resistência selecionada pelo tag impede que o fluxo prossiga para a chamada direta de `addEffect`, e o valor booleano de `addEffect` condiciona a continuação da região visual. **Nenhum efeito de perk está liberado**: proteção territorial, regras de PvP, validação do servidor, armadura Hazmat, efeito tick/curas, owner, estado/charge e QA física continuam fora do alcance da sonda. O workflow precisa repetir com `--seal` e toda CI obrigatória verde antes do merge.

O estado permanece **⚠️ parcial/condicionado**; `NO_MUTATION`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`, sem promoção de Stage 06 ou números do catálogo.
