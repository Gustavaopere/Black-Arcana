# Raygun — fronteira C2S e registro de rede, Alex's Caves Continued 1.0.10

**Estado:** 🟡 descoberta técnica read-only em andamento; **não** é auditoria de segurança
concluída, certificação de perks, evidência de exploit ou QA em cliente/servidor.

## Escopo e autoridade

- Artefato da modlist física: `alexscaves-1.0.10-neoforge+1.21.1.jar`,
  mod ID `alexscaves`, Minecraft 1.21.1 / Java 21.
- SHA-1 do publisher: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- SHA-256: `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Evidência anterior: [manifesto receiver SHA-exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-RECEIVER-1.0.10.json),
  [manifesto de munição/C2S](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-PACKET-AMMO-1.0.10.json),
  [ficha Raygun](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types/raygun.md).
- Nova coleta: [probe read-only](alexscaves_1010_raygun_registration_probe.py),
  [regressões sintéticas](alexscaves_1010_raygun_registration_probe_test.py) e
  [workflow](../../.github/workflows/alexscaves-1010-raygun-registration.yml).

O receiver já documentado consulta o contexto, resolve uma entidade por ID,
confere o tipo de item na mão e chama `UpdatesStackTags.updateTagFromServer`.
A implementação default observada encaminha o `CompoundTag` ao setter de
`DataComponents.CUSTOM_DATA`. **Nenhuma dessas referências isoladas prova**
a direção registrada do pacote, a autorização server-side do entity ID,
sanitização do conteúdo, replay protection ou execução em sessão de jogo.

## Lacuna técnica fechável sem reauditar os contratos existentes

O probe novo usa **somente o JAR SHA-exato**, uma busca limitada de candidatos
pelo constant pool e `javap` em classes selecionadas. Exporta:
caminho e hash da classe, nome/descritor JVM, hash do método extraído,
offset/opcode/símbolo de referências a `UpdateItemTagMessage` ou
`ACNetworkContext`, mais contadores de orçamento de inspeção.

**Limite metodológico:** uma classe com token não significa registrar,
receber ou autorizar o pacote. Referências compiladas são candidatas,
não prova de execução, direção, threading ou identidade de remetente.
Não copiar implementação Java do provider; somente fatos de ABI e referências
simbólicas relevantes para interoperabilidade.

## Resultado observado do probe de descoberta

- Execução no publisher 1.0.10: [GitHub Actions — run 41328521835](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41328521835), **sucesso** no head inicial da PR #993; a CI do head atualizado deve repetir a conferência.
- **32 classes candidatas** encontradas por referências no constant pool; **47 métodos com referências simbólicas** selecionados, sem implicar 32 registries ou 47 handlers do Raygun.
- No conjunto, `com/github/alexmodguy/alexscaves/server/message/ACNetwork.class` apresenta métodos candidatos `registerMessages()` e `lambda$registerPayloads$0(ACNetwork$ACPayload, IPayloadContext)`, extraídos da versão exata.
- Outras classes retornadas incluem handlers de mensagens não relacionadas e classes de `citadel`; apenas a presença do nome `ACNetworkContext` não demonstra acoplamento causal ao Raygun.
- A regressão nova exige as **duas referências de método** no `ACNetwork` real além dos sender e receiver já selados; **não** declara direção de registro, autorização, threading, vínculo de item ou segurança de recepção comprovados.

Esta prova delimita onde examinar o registro do payload e evita reiterar auditorias já incorporadas. Uma certificação futura precisa revisar os opcodes do `ACNetwork` e reconstruir os guards pertinentes, sem tratar o relatório de candidatos como call graph completo.

## Aceite antes de concluir contrato estático Raygun

| Gate | Evidência necessária | Estado atual |
| --- | --- | --- |
| RN-01 | JAR exato + SHA de classes e métodos pertinentes; conflito entre manifestos falha | ✅ probe executado no head inicial; aguarda CI final após revisão |
| RN-02 | Identificar no binário a inscrição efetiva do tipo de mensagem, direção e handler, sem inferir da classe sender | ⚠️ não verificado |
| RN-03 | Verificar semântica de threading e as condições de leitura/edição de estado no receiver | ⚠️ não verificado |
| RN-04 | Confirmar integridade de `entityId`, item, hand swap, `ChargeUsed`/`UseTime` e limites de `CUSTOM_DATA` | ⚠️ não verificado |
| RN-05 | Vincular cobrança nativa, alvo, dano, status e retorno de `hurt` a uma identidade causal única | ⚠️ parcial nos manifestos anteriores |
| RN-06 | Verificar migração/salvamento, reconexão, multiplayer e casos negativos no cliente + servidor dedicado | ⚠️ QA física não testada |
| RN-07 | Certificar os sete eixos de evidência estática num manifesto com hash de fichas e em CI antes de mexer nos índices | ⚠️ não certificado |

**Nenhum campo** de RN-02 a RN-07 deve ser promovido por a coleta RN-01
terminar com CI verde. O probe serve de entrada técnica para fechamento
posterior, não substitui uma revisão semântica dos callsites.

## Segurança da integração

Até contrato seguro do provider (inclusive autorização real e limites de
atribuição/targeting) e homologação apropriada, aplicar **`NO_MUTATION`**.
Não alterar `ChargeUsed`, `UseTime`, `CUSTOM_DATA`, dano, raio, tempo,
aplicação de Irradiated nem o fluxo C2S por perks. Manter
`NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`.
Nenhuma raiz mágica, ficha certificada, porcentagem ou Stage é promovido aqui.
