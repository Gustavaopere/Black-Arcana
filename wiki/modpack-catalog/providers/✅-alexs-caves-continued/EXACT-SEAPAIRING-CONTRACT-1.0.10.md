# Seapairing 1.0.10 — contrato técnico estático individual

A [ficha individual](enchantments/seapairing.md) documenta identidade, comportamento, parâmetros, targeting, custos, integração e validação estática de Seapairing. O recorte é o consumidor passivo de durabilidade do Sea Staff. A [ação Water Bolt](actions/sea-staff-water-bolt.md), a [prova comum](EXACT-TECHNICAL-CONTRACTS-1.0.10.json), os contratos anteriores e as provas de [Sea Swing](EXACT-SEA-SWING-STATIC-1.0.10.json) conservam seus bytes e escopos. Este certificado não conclui os encantamentos irmãos, todo o projétil, o setter da engine ou o provider integral.

Autoridade: JAR publisher CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas de corroboração; os parâmetros certificados vêm do artefato físico **1.0.10**.

O [manifesto individual](EXACT-SEAPAIRING-CONTRACT-1.0.10.json), SHA-256 `af79fc91cae008775ce706f449eee71c2685d7c445f69101c937969b2f51caeb`, sela **uma ficha, 6 classes, 11 recursos, 15 métodos e 452 âncoras**. Há **13 corpos completos, somando 444 instruções**, mais oito âncoras de dois inicializadores delimitados. A interface abstrata `ACTickingItem` tem somente o hash e a assinatura verificada, sem corpo executável a ancorar.

| Classe / método | Cobertura de instruções |
|---|---:|
| `SeaStaffItem`: todos os sete métodos próprios | 370/370, incluindo `acInventoryTick` 42/42, `use` 189/189 e helper de targeting 119/119 |
| `ItemStackTickMixin.ac_inventoryTick` | 19/19 |
| `ACCompat.enchantLevel` | 24/24 |
| `ACCompat.hurtAndBreak` com `InteractionHand` e `slotOf` | 7/7 e 7/7 |
| `ACEnchantmentRegistry.key` | 6/6 |
| `ACItemRegistry.lambda$static$108` | 11/11 |
| `ACEnchantmentRegistry.<clinit>` | 3/182: offsets `293,296,299` |
| `ACItemRegistry.<clinit>` | 5/1382: offsets `2038,2041,2044,2049,2052` |

As seleções dos inicializadores ligam o literal `seapairing` à chave `SEAPAIRING` e o registro `sea_staff` ao supplier. O bootstrap 115 liga esse supplier a `lambda$static$108`, que declara durabilidade 850 e raridade UNCOMMON. Hash de classe e essas janelas não declaram os inicializadores ou todos os seus registros integralmente auditados. Os sete corpos próprios do Sea Staff são completos, mas a presença dos consumidores irmãos em `use` não lhes concede certificados individuais.

O despacho completo encaminha stack, Level, Entity e selected para a interface, sem encaminhar o inteiro do slot. As anotações do mixin apontam para `ItemStack.inventoryTick` em HEAD; a configuração obrigatória empacotada lista o mixin, e o TOML declara essa configuração. Isso prova o encadeamento estático do provider, sem medir cadência ou sucesso de aplicação com transformadores externos. O reader completo relê a stack atual e retorna o primeiro nível correspondente ou zero; não valida slot/tag nem limita o nível ao máximo publicado.

No callback completo, a igualdade `LivingEntity.getUseItem().equals(stack)` é calculada antes da guarda de servidor. Nível positivo e ausência dessa igualdade permitem o sorteio `Level.getRandom().nextFloat()<0.02F`; o teste `Entity.isInWaterRainOrBubble()` vem **depois do RNG**. O argumento `selected` não é lido. Assim, um callback elegível por nível/uso ainda consome RNG quando o portador está seco; não há agenda garantida a cada 50 ticks, escala por nível positivo ou prova de quais inventários externos recebem o callback.

O pedido exato é **`stack.setDamageValue(Math.min(0,stack.getDamageValue()-1))`**, sem teste próprio `D>0` ou `isDamaged`. Para D normal não negativo, pede −1 em D=0 e 0 em D≥1. Não substituir `min` por `max` nem descrever o corpo como reparo fixo de um ponto. Valor armazenado, clamp, componente de damage, sincronização e durabilidade visível continuam na fronteira Minecraft ItemStack/engine, não comprovada por este JAR de provider. A análise estática não estabelece uma falha reproduzida em jogo.

Os 11 recursos selam o JSON próprio, a tag exclusiva do Sea Staff, os idiomas inglês/português, as quatro tags de aquisição, o loot de barter, a configuração de mixins e o TOML. O JSON publica máximo I, peso 1, custos mínimo/máximo 1/41 no nível I, anvil cost 8 e slot `mainhand`; essa declaração não vira uma guarda de slot no callback. As tags declaram elegibilidade em enchanting table, non-treasure, random loot e tradeable. O barter inclui **o item Sea Staff**, peso 12, sem garantir Seapairing na stack. O scan dos 51 JSONs não encontrou exclusão reversa deste ID; a conclusão fica restrita aos dados empacotados.

O cast separado pede desgaste **1**, sob `!instabuild`, pelo wrapper da mão até `ItemStack.hurtAndBreak`. O callback Seapairing não emite projétil, não cobra material/XP e não altera esse pedido de custo. O manifesto preserva a fronteira da engine para a aplicação efetiva de desgaste e reparo; não promete saldo líquido de durabilidade por tempo.

Reprodução a partir da raiz do repositório, com Java 21 e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile seapairing \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SEAPAIRING-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/seapairing-evidence.json
```

A auditoria do artefato real retornou **PASS: 1 ficha, 6 classes, 11 recursos, 15 métodos, 452 âncoras**. A reconstrução externa do manifesto também foi idempotente. Os [testes semânticos](../../../../docs/qa/alexscaves_1010_seapairing_cards_test.py) protegem o consumidor completo, os destinos dos branches, servidor/nível/igualdade, selected não lido, RNG antes do ambiente, `min(0,D−1)`, despacho/interface/configuração, identidade declarativa e limites do certificado. Podem ser executados com `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_seapairing_cards_test.py -v`.

O [auditor literal](../../../../docs/qa/alexscaves_1010_action_contract_audit.py) rejeita troca de família/roster, hashes, ABI/âncoras e budgets inválidos ou promoção de runtime. O [workflow compartilhado](../../../../.github/workflows/alexscaves-1010-action-contracts.yml) acrescenta `seapairing` aos **17 perfis anteriores**, preservando suas verificações e o download único do mesmo JAR. Permanecem os limites de **256 âncoras por método**, **8.192 por manifesto** e o timeout do job de oito minutos; nenhum budget foi ampliado.

Estado do certificado: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**, oito raízes semânticas e provider integral aberto. A ficha adiciona zero raízes mágicas. Setter/clamp, inventários transformados, cadência real, múltiplas cópias, wet/dry/rain/bubble, uso versus selected, níveis externos, creative, sincronização e unload/reload continuam pendências físicas. Nenhum código Java, Stage, adapter mutador ou resultado físico foi promovido.
