# ACSwingControlItem — descoberta SHA-exata 1.0.10

**DISCOVERY_NOT_CERTIFIED / NO_MUTATION.** Escopo da interface e dos dois callbacks nativos; despacho externo ainda exige auditoria.

Publisher alexscaves 1.0.10, Minecraft 1.21.1, Java 21; JAR SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c, 75279314 bytes. Censo de 1555 classfiles: flags 1537, 0 campos, 2 métodos abstratos, 1 implementador direto (PrimitiveClubItem), 0 indiretos, 0 ancestrais nativos, 2 owners com constante de classe, 0 referências de membro da interface ou signatures exatas. Não inferir inatividade: a classe implementadora também estende Item; a interface pode coincidir com callback externo. Classe alvo SHA-256 0fc278b0860306f7746dd2dc445712b42ca4d227d1ec154dfff11471aa67cee3.

## Controle local

| Método | Causalidade observada |
|---|---|
| onLeftClickEntity(ItemStack,Player,Entity)Z | consulta getAttackStrengthScale(0F) @2, converte float em double @5 e compara com 0.95D @6–10; retorna true se abaixo do limiar OU attackAnim != 0F (@14–19); false em outro caso. |
| onEntitySwing(ItemStack,LivingEntity)Z | não-Player retorna false; Player consulta getAttackStrengthScale(0F) @14; se valor <1F E attackAnim>0F, retorna true @32; senão escreve swingTime=-1 @35 e retorna false @39. |

As comparações JVM fcmpg/dcmpg/fcmpl também diferenciam NaN dos valores finitos: no primeiro callback escala NaN não satisfaz <0.95; attackAnim NaN satisfaz !=0. No segundo escala NaN não satisfaz <1 e attackAnim NaN não satisfaz >0, conduzindo ao reset de swingTime. Não confundir 0.95D com 0.95F (escala float promovida a double); o float 0.95F é ligeiramente inferior ao literal double 0.95D. Nenhum efeito de dano, custo, targeting ou alteração de stack é solicitado nesses corpos. Argumento target e stack não são lidos; não há guarda de lado explícita nem checagem de null local. A semântica de true para cancelamento depende da fronteira externa.

O [contrato Swiftwood](enchantments/swiftwood.md) e [atributos dinâmicos](systems/dynamic-attributes.md) já documentam o modificador ATTACK_SPEED, sem transferir automaticamente certificação. Perks devem distinguir cadência real, animação, strength scale, ataque aceito e dano. Ainda não comprovados: caminho cliente/servidor, callback virtual do NeoForge, ordem de eventos, pacote, fórmula vanilla de strength, transformação instalada e QA.

[Job de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44666320278/job/136056381402), relatório SHA-256 67a3bf38959ca92fd40c7a86ffcfa08fc738e036de2eab9f8fd1b54a4e6db8d2. [Manifesto](EXACT-SWING-CONTROL-ITEM-DISCOVERY-1.0.10.json). Sem nova raiz mágica ou promoção de ledger.
