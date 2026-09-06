# Mortal Ledger / Soul Anchor

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Souls & Death
- **Função:** persistência/ressurreição limitada

## Descrição

Mantém um ledger bounded de Soul Anchors. Em uma morte elegível, uma âncora existente pode ser consumida atomicamente para impedir a morte e restaurar vida dentro de limites.

## Mecânica

- hard cap de anchors;
- recent-death identity bounded para anti-replay;
- recovery lockout;
- exactly-once death settlement;
- persistência via SavedData;
- morte só é cancelada após consumo atômico de uma âncora existente;
- restauração de vida finita e limitada pela vida máxima atual.

## Geração de recurso

Não há producer genérico automático de spirit/soul a partir de qualquer morte. Sem provider causal seguro, credit permanece fail-closed.

## Malum / Eidolon

- Malum mantém autoridade de spirit resources reais;
- o bridge pode query/consume/refund spirits suportados, mas não infere quanto spirit uma morte gerou sem callback verificável;
- Eidolon continua candidato de apresentação/unlock ritual, porém unlock player-specific permanece fail-closed quando o hook não expõe identidade do caster.

## Quantidades / cooldown

- **Cap exato, recovery lockout e restauração:** extrair do runtime/config antes de publicar como números finais; `TBD` nesta primeira reconciliação.
- **Stage 08** pode balancear abaixo de hard ceilings sem alterar contratos de segurança.

## Obtenção/aprendizado

`TBD — provider-backed producer/unlock + Stage 08 progression.`

## Segurança

- exactly-once;
- anti-replay;
- sem vidas infinitas;
- sem spirit sintético;
- malformed record containment;
- sem inferência de ownership.
