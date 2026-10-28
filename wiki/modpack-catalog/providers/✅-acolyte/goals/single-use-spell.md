# SingleUseSpellGoal — Acolyte 1.0.3

**Estado:** `EXACT_PUBLISHER_BINARY_STATIC_CONTRACT` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · **certificações de perk: 0**.

## Identidade e evidência

Goal de IA, sem registry ID, item ou identidade de magia própria. Classe `net.raptorzizi.acolyte.entity.goals.SingleUseSpellGoal`, superclass Minecraft `Goal`. Acolyte agenda uma tentativa de magia do host; **Iron's mantém a propriedade da magia e o delta semântico Acolyte é +0**.

Fonte desta ficha: somente o publisher `acolyte-1.0.3.jar`, CurseForge `1534642/8098233`, 621837 bytes, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Igualdade com o JAR instalado não demonstrada. [Contratos e limites da inspeção](../BINARY-CONTRACTS-1.0.3.md); [manifesto do artefato](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). As referências abaixo são localizadores `classe → método + descriptor → PC` no `javap -p -c -s -constants` desse artefato; registram fatos de interoperabilidade, sem publicar corpos de métodos.

| Evidência | Método / descriptor | PC e fato observado |
|---|---|---|
| S1 | `<init>(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;IIII)V` | 4–10 flags vazias; 13–44 exige `PathfinderMob`; 55–83 sorteia nível/delay; 86–102 fixa raio 20 e quadrado 400 |
| S2 | `canUse()Z` | 0–13 bloqueia single attack já usado; 14–43 captura target vivo; 44–57 bloqueia durante casting; 58–73 decrementa delay; 74–99 testa distância² ≤ 400 |
| S3 | `canContinueToUse()Z` | 0–1 retorna falso |
| S4 | `start()V` | 0–9 marca single attack usado; 10–25 orienta olhar 45°/45°; 28–40 chama `IMagicEntity.initiateCastSpell(AbstractSpell,int)` |

## Parâmetros e composição real

O construtor recebe `(mob mágico, spell, nível mínimo, nível máximo, delay mínimo, delay máximo)`. Ele exige que o primeiro argumento também seja `PathfinderMob`; caso contrário lança `IllegalStateException`. O nível é sorteado **uma vez na construção**, por `Utils.random.nextIntBetweenInclusive(min,max)`. O delay inicial usa uma segunda chamada inclusiva ao mesmo RNG global do host. Não há clamps ou validação adicional dos limites nesta classe. [S1]

O raio fixo é **20 blocos**, com comparação inclusiva `distanceToSqr(target) ≤ 400`. Esse é o alcance da elegibilidade desta tentativa, sem demonstrar alcance, splash ou colisão da magia selecionada. Nenhuma flag `MOVE`/`LOOK` é adquirida; a lista de flags do goal é vazia, embora `start` altere o look control. [S1–S2]

Os quatro consumidores diretos são Human/Demon Archer e Human/Demon Warrior. Em cada `registerArchetypeGoals()V`, PC 65–114, somente adicionam o goal quando `selectedProfile.singleUseSpell` existe, na prioridade **2**, nível **1–1**, delay inclusivo **D…D+20**, onde `D=selectedProfile.singleUseSpellDelay`. Não há uso direto desta classe nos dois Mage nem no Lieutenant no inventário das 93 classes. A identidade concreta da magia provém do perfil e continua Iron's-owned. Ver as fichas de [Human Archer](../entities/human-archer.md), [Demon Archer](../entities/demon-archer.md), [Human Warrior](../entities/human-warrior.md) e [Demon Warrior](../entities/demon-warrior.md).

## Targeting, relógio e tentativa de cast

`canUse` primeiro consulta `getHasUsedSingleAttack()`. Caso falso, grava o `mob.getTarget()` no campo local; exige target não nulo e `isAlive()`, e exige `!isCasting()`. **Só depois** decrementa o delay e avalia o raio. Portanto:

- tempo sem target vivo ou durante outro cast não consome o delay;
- tempo com target elegível, mesmo além de 20 blocos, consome o delay;
- o contador não é reiniciado quando o target muda ou sai do raio;
- após chegar a zero ele pode continuar negativo nas avaliações elegíveis fora do raio;
- o valor mede avaliações elegíveis de `canUse`, não um cooldown comprovadamente medido em segundos ou em todos os ticks físicos do servidor. A classe não redefine `requiresUpdateEveryTick`. [S2]

Não há teste local de linha de visão, equipe, dono, claim, tipo de dano, escola, imunidade ou posição de blocos. A seleção e as relações do target pertencem à entidade/host. Não há confirmação adicional de vida/alcance em `start`; ele usa o target capturado na avaliação. [S2,S4]

`start` marca `setHasUsedSingleAttack(true)` **antes** de `initiateCastSpell`. Assim o sinal significa consumo da oportunidade de IA, sem callback local de cast aceito, efeito aplicado ou dano confirmado. Não existe reset dessa flag nesta classe. `canContinueToUse=false` torna a execução pontual; a continuação do cast fica no `IMagicEntity`/host. [S3–S4]

## Custos, dano, persistência e callbacks

Mana, tempo de conjuração, spell cooldown, DamageSource, dano, cura, projéteis, efeitos, recast e cancelamento são **delegados ao spell/entidade Iron's**; esta classe não os calcula, debita ou confirma. O delay de IA não equivale ao cooldown da magia. Não há custo de item/XP/emerald neste goal. [S1–S4]

Campos locais: referências finais ao mob/spell, nível final, raio e raio² finais, delay mutável e target mutável. Não declara serializer, NBT, packet, `stop`, callback de cancelamento, settlement ou retorno de sucesso. A persistência da flag exposta pelo `IMagicEntity`, se houver, pertence ao implementador; não é comprovada por esta classe. A reconstrução do goal cria novos sorteios. [S1–S4]

## Integração por eixo

| Eixo | Contrato observado e limite de integração |
|---|---|
| Identidade / progressão / gates | Goal não é magia aprendível. RPG Skill Tree controla perks/Mastery/gates somente por contratos verificados; não atribuir uma segunda identidade ao spell escolhido. |
| Targeting / proteção | Acolyte usa o target corrente e raio 20. Não há veto de proteção neste goal; proteção de efeitos do host exige boundary próprio. `WorldEffectPolicy` BA não é um interceptador demonstrado deste caminho. |
| Dano / cura / atributos | Delegados ao host; `start` não é hit nem cura confirmada. Não criar multiplicador ou segundo proc neste callback. |
| Custos / casting / mana | Delegados a Iron's. Não reservar/debitar mana adicional ao observar a chamada. |
| Delay / cooldown / recast | Só o delay local e a flag de single use estão provados. Alterar ambos ou o cooldown host exige hook seguro ainda não verificado. |
| Movimento / animação | Sem flags de exclusão; ajusta olhar 45/45. Navegação e animação de cast são da entidade/host; compatibilidade Epic Fight não testada. |
| Persistência / multiplayer | Sem NBT ou sincronização próprios. Reload e autoridade lógica precisam de QA do implementador. |
| Eventos / Mastery / exatamente uma liquidação | Há uma chamada `initiateCastSpell` por execução, com flag marcada antes. Nenhum evento de conclusão ou garantia de exactly-once após reload. Não premiar Mastery por `canUse` ou pela flag. |

## QA física pendente

Verificar cadência do scheduler, delay ao alternar target/casting/raio, target invalidado entre `canUse` e `start`, recusa/cancelamento do host após consumir a flag, save/reload, chunk unload e sincronização multiplayer. Comparar a magia real do perfil, seu custo e sucesso no Iron's instalado. Nenhum adapter, alteração de runtime ou certificação foi criado por esta ficha.
