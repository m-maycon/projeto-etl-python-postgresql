-- ============================================
-- 01. FATURAMENTO TOTAL
-- ============================================

SELECT
    SUM(i.quantidade * i.preco_unitario) AS faturamento_total
FROM itens_pedido i
INNER JOIN pedidos p
    ON i.pedido_id = p.pedido_id
WHERE p.status = 'CONCLUIDO';

-- ============================================
-- 02. TICKET MEDIO
-- ============================================

SELECT
    ROUND(
        SUM(i.quantidade * i.preco_unitario)
        / COUNT(DISTINCT p.pedido_id),
        2
    ) AS ticket_medio
FROM itens_pedido i
INNER JOIN pedidos p
    ON i.pedido_id = p.pedido_id
WHERE p.status = 'CONCLUIDO';

-- ============================================
-- 03. RECEITA POR CATEGORIA
-- ============================================

SELECT
    pr.categoria,
    SUM(i.quantidade) AS quantidade_vendida,
    SUM(i.quantidade * i.preco_unitario) AS receita
FROM itens_pedido i
INNER JOIN produtos pr
    ON i.produto_id = pr.produto_id
INNER JOIN pedidos p
    ON i.pedido_id = p.pedido_id
WHERE p.status = 'CONCLUIDO'
GROUP BY pr.categoria
ORDER BY receita DESC;

-- ============================================
-- 04. TOP 5 PRODUTOS POR RECEITA
-- ============================================

SELECT
    pr.produto_id,
    pr.nome,
    pr.categoria,
    SUM(i.quantidade) AS quantidade_vendida,
    SUM(i.quantidade * i.preco_unitario) AS receita
FROM itens_pedido i
INNER JOIN produtos pr
    ON i.produto_id = pr.produto_id
INNER JOIN pedidos p
    ON i.pedido_id = p.pedido_id
WHERE p.status = 'CONCLUIDO'
GROUP BY
    pr.produto_id,
    pr.nome,
    pr.categoria
ORDER BY receita DESC
LIMIT 5;

-- ============================================
-- 05. RECEITA POR CLIENTE
-- ============================================

SELECT
    c.cliente_id,
    c.nome,
    c.estado,
    COUNT(DISTINCT p.pedido_id) AS quantidade_pedidos,
    SUM(i.quantidade * i.preco_unitario) AS receita
FROM clientes c
INNER JOIN pedidos p
    ON c.cliente_id = p.cliente_id
INNER JOIN itens_pedido i
    ON p.pedido_id = i.pedido_id
WHERE p.status = 'CONCLUIDO'
GROUP BY
    c.cliente_id,
    c.nome,
    c.estado
ORDER BY receita DESC;

-- ============================================
-- 06. PEDIDOS POR STATUS
-- ============================================

SELECT
    status,
    COUNT(*) AS quantidade,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentual
FROM pedidos
GROUP BY status
ORDER BY quantidade DESC;