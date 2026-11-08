# Sharp Cane 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/sharp-cane.md) conclui identidade, comportamento, parâmetros, targeting, custos, integração e validação estática de Sharp Cane. O recorte liga o parâmetro inicial do gancho ao ramo nativo selecionado de busca/pedido de dano. Preserva os bytes e limites de [Far Flung](EXACT-FAR-FLUNG-1.0.10.json) e das demais provas anteriores. Não conclui o tick/CFG integral, os encantamentos irmãos, a aplicação de dano pela engine, a persistência herdada ou o provider integral.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não substitui os dados/bytecode **1.0.10**.

O [manifesto individual](EXACT-SHARP-CANE-CONTRACT-1.0.10.json), SHA-256 `625996d13e4f06d66db501609fa637e31bba1ec298a964abd60bc737fec85893`, sela **uma ficha, 5 classes, 10 recursos, 50 métodos e 1.409 âncoras**. Há **47 corpos completos, somando 1.146 instruções**, mais o prefixo local do tick e sete âncoras de dois inicializadores delimitados.

| Recorte | Cobertura e limite |
|---|---|
| `CandyCaneHookEntity(Player,Level,ItemStack,boolean)` | 231/231 instruções; snapshot `DAMAGE=3F×L` |
| `defineSynchedData`, getter/setter DAMAGE | 47/47 e 7/7 + 7/7; Float default 0F |
| `onHitEntity` | 24/24; guarda movimento/posição/UUID sem ler DAMAGE ou chamar hurt nesse corpo |
| `tick` | **256/546**: prefixo completo `@0–562` (255 instruções) mais join `@563`; 290 instruções omitidas |
| Resolução própria de owner/alvo, flags e posições selecionadas | Corpos completos; chamadas à engine e a outros mobs mantêm fronteiras externas |
| NBT próprio | 23/23 e 22/22; chama super e não lê/grava DAMAGE |
| `CandyCaneHookItem` | Todos os 13 métodos próprios completos, incluindo use 188/188 e canLaunchHook 54/54; isso não encerra todos os sistemas do equipamento |
| `ACCompat` | Reader de nível, desgaste por mão, slot, UUID e resultados de uso selecionados completos |
| `ACEnchantmentRegistry` | key completo; `<clinit>` 3/182, offsets `473,476,479` |
| `ACItemRegistry` | supplier `lambda$static$179` completo; `<clinit>` 4/1382, offsets `3163,3166,3171,3174` |

O registro de itens liga o literal `candy_cane_hook` ao supplier por bootstrap 181, e o supplier instancia a classe nativa. O construtor do item declara durabilidade 200. A receita empacotada usa as linhas `L S`, ` L `, `P L`: três Licoroot Vines, um Sharpened Candy Cane e um Candy Cane Pole para um gancho. Aquisição do item e aquisição de Sharp Cane não são garantias de encantamento no resultado.

O tick completo foi contado como 546 instruções, com offsets até 1173. O recorte contém todas as instruções locais de `@0–563`, mas não torna as 290 omitidas, a superclasse ou o CFG integral auditados. O hash da classe distribuída sela o artefato; censo/fingerprint auxiliar do corpo inteiro corroboram a delimitação sem substituir evidência causal das regiões omitidas. Nenhum budget foi ampliado para encaixar o tick inteiro.

Distinções centrais: a stack é lida na criação e DAMAGE é capturado como `3F×L`, sem clamp próprio ao nível II. O tick chama super **antes** de capturar owner/alvo; no ramo próprio servidor, alvo já existente e busca de novo candidato seguem caminhos distintos. A busca usa AABB do gancho expandida em 1D e predicate ligado por bootstrap a `Entity.isAlive`. Normalização de segmento, owner, distância e Gum Worm conservam os predicados descritos na ficha, inclusive o ramo diferente quando owner é null.

Encontrando candidato, o UUID é escrito antes de ler DAMAGE. O teste é igualdade a zero, não positividade. O ramo solicita fonte `thrown(this,owner)`, chama `Entity.hurt` e descarta o booleano. `onHitEntity` não contém esse hurt e o ramo de alvo existente não repete aquele pedido. Assim, attachment, UUID, tentativa e dano aceito não são recibos intercambiáveis para perks, XP ou Mastery. A ausência de DAMAGE nos overrides próprios de NBT não conclui perda/restauração após reload: herança, reconstrução e engine permanecem fronteiras externas.

Os dez recursos selam JSON próprio, tag exclusiva do Candy Cane Hook, idiomas inglês/português, quatro tags de aquisição, receita do equipamento e TOML. O JSON publica máximo II, peso 10, custos mínimo 1/9 e máximo 41/51 nos níveis I/II, anvil cost 1 e slot mainhand; não tem effects/exclusive_set local. O scan dos 51 JSONs não encontrou exclusão reversa; Fieldrefs exatos nos 1.555 classfiles apontam SHARP_CANE somente no registro e na entidade. Esses censos não abrangem reflexão, transformadores, mods externos ou datapacks ativos.

Reprodução a partir da raiz do repositório, com Java 21 e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile sharp_cane \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SHARP-CANE-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/sharp-cane-evidence.json
```

A auditoria do artefato real retornou **PASS: 1 ficha, 5 classes, 10 recursos, 50 métodos, 1.409 âncoras**. Os [testes semânticos](../../../../docs/qa/alexscaves_1010_sharp_cane_cards_test.py) protegem snapshot, default/reader, prefixo local, servidor/targeting, ordem UUID/hurt, retorno descartado, onHit sem aquele hurt, custos, NBT próprio, sete eixos e fila alfabética viva. A reconstrução externa do manifesto é verificada por igualdade de bytes sobre os inputs selados.

O [auditor literal](../../../../docs/qa/alexscaves_1010_action_contract_audit.py) e o [workflow compartilhado](../../../../.github/workflows/alexscaves-1010-action-contracts.yml) acrescentam `sharp_cane` aos **19 perfis anteriores**, preservando verificações, download único e timeout de oito minutos. Permanecem os limites de **256 âncoras por método** e **8.192 por manifesto**.

Estado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**, oito raízes semânticas e provider integral aberto. A ficha adiciona zero raízes mágicas. Nenhum Java de runtime, adapter mutador ou Stage foi promovido. Busca versus colisão/supertick, dano aplicado, PvP/proteções, owner/segmentos, duas mãos, spawn recusado, sincronização e persistência herdada continuam pendências físicas.
