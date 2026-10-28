# FlyCombatHelper — Acolyte 1.0.3

**Estado:** `EXACT_PUBLISHER_BINARY_STATIC_CONTRACT / NO_IN_ARTIFACT_CALLER_OBSERVED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · **certificações de perk: 0**.

## Identidade, ativação e evidência

`net.raptorzizi.acolyte.entity.goals.FlyCombatHelper` é uma classe auxiliar comum, superclass `Object`; **não estende `Goal`**, não tem flags/prioridade própria e não registra entidade, spell ou item. No inventário completo das **93 classes** do publisher 1.0.3, a busca dos símbolos de classe/construtor encontra somente a própria definição: **nenhum caller Acolyte observado**. A ficha descreve o contrato latente se alguém instanciar/chamar o helper, sem afirmar que os mobs voam por ele no runtime. Referências externas/reflexão não são excluídas por essa busca.

Fonte exclusiva: publisher `acolyte-1.0.3.jar`, CurseForge `1534642/8098233`, 621837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Hash do instalado não comprovado. [Contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Evidências F1–F8 são localizadores da classe acima no `javap -p -c -s -constants`, método/descriptor e PCs; os valores/formulas abaixo são fatos de interoperabilidade, sem transcrição de método ou assets.

| Evidência | Método / descriptor | PC e fato observado |
|---|---|---|
| F1 | `<init>(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/NeutralWizard;DD)V` | 4–17 armazena mob, radius, speedModifier |
| F2 | `reset()V` | 0–17 zera xd,yd,zd e moveTime |
| F3 | `tick()V` | 0–129 ramo sem target: altura MOTION_BLOCKING, desaceleração/descida ou parada/reset |
| F4 | `tick()V` | 130–231 com target: posição/distância, decremento do timer, renovação 40+nextInt(80), Gaussianas |
| F5 | `tick()V` | 234–322 viés para target quando distância > 0.8×radius |
| F6 | `tick()V` | 325–485 aproximação de velocidade e clamps horizontal 0.25 / vertical ±0.15 |
| F7 | `tick()V` | 488–531 body yaw para velocidade horizontal >0.05 |
| F8 | `tick()V` | 534–640 correção futura de yd por altura 2/12; 643–666 olhar para target eye, 30/30 |

## Parâmetros e unidade temporal

Construtor recebe `(NeutralWizard mob, double radius, double speedModifier)`. Não valida sinais, finitude ou null. **`speedModifier` é armazenado, porém nunca lido por outro método desta classe**: não há escala de velocidade usando esse parâmetro no contrato observado. `radius` controla somente o limiar de viés ao target; não é limite duro de deslocamento, alcance de ataque ou detecção. Não há instanciação que forneça valores efetivos no artefato. [F1,F4–F6]

`reset` zera os três componentes desejados e o timer. Não zera a velocidade do mob, não altera gravidade e não limpa target. O timer inicial padrão é 0; com target, a primeira avaliação pré-decrementa e renova o movimento. Renovação sorteia **40…119** chamadas ao helper por `40 + random.nextInt(80)`. Sem caller/cadência não converter esse intervalo para segundos ou ticks físicos garantidos. [F1–F4]

## Contrato sem target

Consulta a altura da coluna com `Heightmap.Types.MOTION_BLOCKING`, nas coordenadas X/Z convertidas de double para int por cast JVM (truncamento, sem chamada a floor). Se Y está acima de **altura+0.1**:

- multiplica velocidade X/Z por **0.85**;
- define velocidade Y como `max(−0.15, velocidadeY−0.02)`;
- chama `setNoGravity(false)`.

Se Y≤altura+0.1, escreve velocidade **(0,0,0)** e chama `reset`. Em ambos os ramos retorna. Não há teste de chão/collision box, navegação, aterrissagem confirmada ou alvo vivo. No ramo parado não há chamada explícita de gravidade. [F3]

## Contrato com target e geometria

Aceita qualquer target não nulo, sem `isAlive`, LOS, equipe, dono, claim ou filtro de dimensão próprio. Obtém RNG do mob e distância Euclidiana 3D entre posições. A cada renovação, sorteia componentes desejados independentes: **xd=Gaussian×0.3**, **yd=Gaussian×0.15**, **zd=Gaussian×0.3**. [F4]

Quando a distância é **maior que 0.8×radius**, no mesmo momento da renovação aplica viés na direção normalizada `u=(targetPos−mobPos).normalize()`: X/Z desejados tornam-se **0.3×componente anterior + 0.4×u(X/Z)** e Y desejado **0.3×yd anterior + 0.2×uY**. Dentro/inclusive do limiar conserva a amostra Gaussiana. O teste só ocorre ao renovar, não em cada chamada. Não há órbita fixa, raio de confinamento ou pathfinding. [F4–F5]

Em cada chamada com target, aproxima a velocidade atual dos valores desejados por incrementos de sinal: X/Z acrescentam **0.02×signum(desejado−atual)**; Y acrescenta **0.01×signum(desejado−atual)**. Depois limita magnitude horizontal a **0.25** por normalização proporcional e Y a **[−0.15,0.15]**, e escreve `setDeltaMovement`. Esses são limites dos valores escritos pelo helper; a física/colisões/forças posteriores podem mudar o movimento observado. [F6]

Com magnitude horizontal >**0.05**, define `yBodyRot=degrees(atan2(vz,vx))−90`. Em seguida lê novamente posição/altura MOTION_BLOCKING: abaixo de **altura+2** e yd<0 inverte yd para positivo; acima de **altura+12** e yd>0 inverte para negativo. Essa alteração é do **desejado para próximas chamadas**, pois a velocidade da chamada já foi escrita. Finaliza olhando para `(targetX,targetEyeY,targetZ)` com limites **30°/30°**. [F7–F8]

O ramo com target não chama `setNoGravity(true)`; uma eventual ativação de voo/gravidade teria de vir do caller ou da entidade. O helper também não testa blocos à frente, teto, líquidos ou passagem livre. [F4–F8]

## Dano, custo, persistência e callbacks

Não existe chamada de ataque/cast, dano/cura, mana, munição, cooldown de magia, recast, stamina, item ou XP. O timer é de renovação do movimento, sem relação comprovada com ataques. Nenhuma magia nova Acolyte: **+0**, e qualquer casting de `NeutralWizard` continua no Iron's. [F1–F8]

Campos locais são mob/radius/speedModifier finais, xd/yd/zd e moveTime mutáveis; sem NBT, serializer, synchronized entity data, packet, evento, callback de conclusão ou ligação automática ao ciclo de vida. `reset` não é chamado por construtor/remoção externos no artefato. A autoridade lógica cliente/servidor não é checada localmente; a responsabilidade seria do caller ausente. [F1–F8]

## Integração por eixo

| Eixo | Contrato observado e limite |
|---|---|
| Identidade / ativação / RPG Skill Tree | Helper sem registry e sem caller Acolyte observado. Não é skill, perk ou magia utilizável; RPG Skill Tree continua autoridade de progressão/Mastery/gates. Não ativar o helper como efeito colateral do catálogo. |
| Targeting / proteção | Lê target existente; raio é viés de movimento. Sem validação de claims/LOS. `WorldEffectPolicy` BA não fornece interceptação demonstrada desse deslocamento. |
| Dano / cura / efeitos | N/A local: não ataca nem aplica efeito. Magias/eventos do mob host são fronteiras separadas. |
| Custos / cast / recast | N/A local; sem reserva de mana ou pipeline de cast. +0 identidades mágicas. |
| Movimento / tempo / atributos | Fórmulas de delta comprovadas; speedModifier sem consumer. Sem gancho seguro validado para velocidade, gravidade ou alteração de radius/timer. |
| Animação / Epic Fight | Apenas body yaw/look; sem controller de animação. Coexistência e autoridade física não testadas. |
| Persistência / rede / dimensão | Sem save/packet/side guard próprios. Caller externo precisaria provar ciclo de vida, reset, chunks/dimensões e sincronização. |
| Eventos / Mastery / liquidação | Sem conclusão, dano ou callback que gere Mastery. Não premiar deslocamento por cada chamada nem criar segundo motor de voo. |

## QA física pendente

Primeiro provar um caller efetivo no pack instalado. Só então validar lado lógico, gravidade, colisões/teto/líquidos, alturas em coordenadas negativas, target removido, limits de velocidade após física, unload/restart e sincronização. A presença da classe não prova voo ativo em nenhum mob. Nenhum adapter, runtime change ou certificação foi criado.
