# Goety 3.1.4 — auditoria estrutural exata de Banish, Telekinesis e Soul Energy

**Data:** 26/10/2026
**Estado:** ⚠️ `EXACT_SHA_VERIFIED / METHOD_SCOPED_SYMBOLS_VERIFIED / CONTROL_FLOW_NOT_VERIFIED / PHYSICAL_QA_PENDING`
**Escopo:** documentação de compatibilidade clean-room; nenhum adapter, casting hook ou perk foi implementado ou homologado.

## 1. Cadeia de evidência

- **Artefato instalado:** `goety-3.1.4.jar` / mod ID `goety` / CurseForge `586095/8689429`, SHA-1 **`a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`**. Confere com a [auditoria física anterior](EXACT-3.1.4-ARTIFACT-AUDIT.md).
- **Nova medição exata:** [GitHub Actions #40362689828](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40362689828), job `121712040049`, resultado `completed/success`; download CurseMaven seguido de `sha1sum -c` do binário exato e inspeção simbólica via JDK 21.
- **Branch temporária não destinada a merge:** `audit/goety-314-banish-soul-structure-20261026`; HEAD `c6e98e55785dad3c78ed35c0a6bc85e82cac2200`. Workflow `.github/workflows/goety-314-target-soul-structure-probe.yml` pertence somente à branch de auditoria e não será copiado à `main`.
- **Artifact de texto:** `goety-314-target-soul-structure-report`, ID `12668033309`, digest `sha256:755316ff8dbe7a1f7f2997d95c3609cd4bdbf7a3a5513c99a1fd726f8b2a71a0` (retenção do probe: 30 dias). Logs do job preservam as mesmas afirmações de verificação.
- **Método:** `javap -p -c` é usado na execução efêmera, mas o relatório publicado contém **somente classes/métodos, acessos a fields, relações de chamada e resultados de checks**; corpos, offsets, constantes, caminhos de salto, receitas e assets de terceiro não são incorporados ao repositório.

**Delimitação:** a existência de instrução de chamada ou de escrita de campo prova uma **relação estática de bytecode** da versão 3.1.4. Não prova que o ramo executou durante uma conjuração, que um alvo satisfaz os predicados, que houve teleporte/débito ou que um evento é ponto de integração seguro.

## 2. Banish — pré-validação versus aplicação

Provas **do classfile exato**:

| Método / ponto | Evidência de referências |
|---|---|
| `BanishSpell.conditionsMet` | Referencia `entityResult`, `EventHooks.onEnderTeleport` e a chamada herdada `TouchSpell.conditionsMet`. |
| `BanishSpell.touchResult` | Referencia `LivingEntity.stopRiding` e `LivingEntity.randomTeleport`; **não possui chamada direta a `EventHooks.onEnderTeleport` no corpo desse método** conforme a varredura estática. |
| `DarkWand.interactLivingEntity` | Referencia `DarkWand.canCastTouch` e `ITouchSpell.touchResult`. |
| `DarkWand.canCastTouch` | Referencia `ITouchSpell.targetConditions`; o método do provider possui outros gates de custo/cooldown fora do escopo de comportamento testado. |

**Inferência permitida:** a pré-verificação `conditionsMet` e a aplicação `touchResult` têm **superfícies de chamada diferentes** no JAR 3.1.4; o efeito não chama `EnderTeleport` diretamente no mesmo método que referencia `randomTeleport`. Isto **não** demonstra que a entidade validada e a entidade tocada divergem em um cenário real, nem que `randomTeleport` deixa de consultar outras proteções internas. A hipótese de divergência entre alvos descrita no [dossiê source-adjacent 3.1.1](focuses/banish-focus.md) continua **⚠️ não comprovada como exploit/bug instalado**.

**Gate:** antes de perk que altere range, destino, blacklist ou categoria de alvo, testar duas entidades distintas (raycast/interaction), entidades imunes e com HP superior ao limite, evento EnderEntity cancelado, bloco protegido, tentativas fracassadas e cancelamento do Touch event. Qualquer mutação de teleporte permanece **⛔ fail-closed**.

## 3. Telekinesis — campo de instância e lifecycle

A classe binária `TelekinesisSpell` declara `public Entity victim`, conforme [auditoria ABI anterior](EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md). Este novo probe confirmou no mesmo JAR:

- `startSpell` e `stopSpell` contêm **escrita `PUTFIELD victim`**;
- `findVictim` contém **leitura `GETFIELD victim` e escrita `PUTFIELD victim`**;
- `SpellResult` contém referências **`GETFIELD victim`** e a `findVictim`;
- `stopSpell` referencia `SEHelper.addCooldown`.

**Inferência permitida:** a identidade do alvo é armazenada em um campo do **objeto `TelekinesisSpell`**, não em um parâmetro separado de caster em todos os métodos listados. O fato isolado **não** identifica o alcance de compartilhamento real desse objeto entre jogadores, dimension contexts ou Focuses. A fonte pública 3.1.1 descreve `MagicFocus` com instância `ISpell`; a auditoria anterior encontrou `MagicFocus(ISpell)` e `getSpell()` no 3.1.4, mas não comprovou neste probe quantas instâncias reais são criadas/reutilizadas em todas as rotas.

**Gate:** QA com dois conjuradores paralelos, interrupção de cast, swap de varinha, morte, dimensão, logout, descarregamento de chunk e restart; observar apenas estado autorizado pelo provider. **⛔ Nenhum adapter externo deve gravar `victim` nem simular nova física** até confirmar ownership e ciclo de vida.

## 4. Soul Energy — onde aparecem descontos, admissão e perda

Relações **estáticas exatas** do JAR 3.1.4:

| Superfície | Call-sites confirmados | Não demonstrado |
|---|---|---|
| `DarkWand.SoulUse` | **2 referências** a `SEHelper.soulDiscount`, correspondendo a caminhos estáticos desse método. | Se ambas executam no mesmo cast, valores finais e arredondamento. |
| `SEHelper.decreaseSouls` | **1 referência** a `SEHelper.soulDiscount` **dentro da própria classe**, e **1 referência** a `GoetyEventFactory.onSoulEnergyLoss`. | Que o mesmo desconto foi aplicado duas vezes ao **mesmo** valor de gasto de forma incorreta. |
| `DarkWand.MagicResults` | Referências a `DarkWand.SoulUse`, `SEHelper.getSoulsAmount`, `SEHelper.decreaseSouls`, `ISpell.SpellResult` e `SEHelper.addCooldown` em seu método. | Exclusividade do caminho, ordem executada, atomicidade, cancelamento/reembolso ou sucesso do efeito. |
| `DarkWand.canCastTouch` | Referências a `SoulUse`, `getSoulsAmount` e `decreaseSouls` também nessa admissão. | Que toque, cast normal e canalização usam sempre a mesma transação. |
| `SEHelper.soulDiscount` | Referencia `ISoulDiscount.getSoulDiscount` nos slots de armadura. | Multiplicador, limites, descontos simultâneos, efeitos de addons. |

**Achado importante:** o primeiro probe de ABI resumida não listava `SEHelper.decreaseSouls → SEHelper.soulDiscount` porque seu filtro descartava referências **sem owner explícito** em chamadas da própria classe. O novo parser inclui essas chamadas e confirma a referência no **JAR real 3.1.4**. **Não é uma correção de um bug comprovado nem um desconto duplicado confirmado**, apenas reparo da lacuna da auditoria estática.

**Gate transacional:** comparar custos `SoulUse` na checagem de saldo com valores enviados ao `ChangeSoulEnergyEvent.Loss` e debitados da pool/totem; testar sem e com `ISoulDiscount`, com dois tipos de Focus (instant/touch), players criativos e não criativos, listeners que cancelam/alteram gasto, edge cases e arredondamento de inteiros. Observar valores efetivamente liquidados antes de desenhar desconto por perk. **⛔ Não ouvir `Loss` como prova suficiente de cast único e não debitar/refundar Soul Energy de novo no Black Arcana.**

## 5. Matriz de evidências e decisão

| Camada | Estado | Observação |
|---|---|---|
| Identidade/modlist | ✅ exata | Artefato e Focuses já documentados |
| API/assinaturas | ✅ pontual | Símbolos do [probe #40344481668](EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md) |
| Método → chamada/field | ✅ pontual | Nova execução `40362689828`, este documento |
| Algoritmo, branches e valores finais | ⚠️ condicionado | Source público 3.1.1 não é equivalência binária |
| Causalidade, segurança, permissões e transação | ⛔ não homologado | Exige QA em servidor real |
| Certificado estático completo de perks | ⛔ pendente | Sete provas do manifesto ainda não fechadas |

O Goety mantém autoridade sobre seu Focus/Staff casting, energia, servos e mundo; Black Arcana mantém o seu próprio runtime, com boundaries fail-closed. O RPG Skill Tree permanece consumidor de contratos de progressão, Mastery e perks, nunca controller do recurso do provider.

**Contadores intocados:** o documento **não adiciona magia**, não muda `PERK-READY-CERTIFICATIONS.json` e não eleva Goety `0/361` ou a certificação global `109/2075` registrada neste checkpoint. Stage 06.05 e validações físicas transferidas para Stage 09 permanecem sem promoção.
