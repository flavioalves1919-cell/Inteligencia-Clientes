-- ============================================================
-- INTELIGÊNCIA DE CLIENTES
-- ANÁLISES SQL
-- ============================================================


-- ============================================================
-- 1. FATURAMENTO TOTAL
-- ============================================================

SELECT
    ROUND(SUM(valor_total)::numeric, 2) AS faturamento_total
FROM pedidos
WHERE status = 'Concluído';


-- ============================================================
-- 2. TOTAL DE PEDIDOS
-- ============================================================

SELECT
    COUNT(*) AS total_pedidos
FROM pedidos;


-- ============================================================
-- 3. TICKET MÉDIO
-- ============================================================

SELECT
    ROUND(AVG(valor_total)::numeric, 2) AS ticket_medio
FROM pedidos
WHERE status = 'Concluído';


-- ============================================================
-- 4. CLIENTES ATIVOS
-- ============================================================

SELECT
    COUNT(DISTINCT id_cliente) AS clientes_ativos
FROM pedidos
WHERE status = 'Concluído';


-- ============================================================
-- 5. TOP 10 CLIENTES POR FATURAMENTO
-- ============================================================

SELECT
    id_cliente,
    ROUND(SUM(valor_total)::numeric, 2) AS faturamento
FROM pedidos
WHERE status = 'Concluído'
GROUP BY id_cliente
ORDER BY faturamento DESC
LIMIT 10;


-- ============================================================
-- 6. TOP 10 PRODUTOS POR FATURAMENTO
-- ============================================================

SELECT
    id_produto,
    ROUND(SUM(valor_total)::numeric, 2) AS faturamento
FROM pedidos
WHERE status = 'Concluído'
GROUP BY id_produto
ORDER BY faturamento DESC
LIMIT 10;


-- ============================================================
-- 7. FATURAMENTO POR MÊS
-- ============================================================

SELECT
    DATE_TRUNC('month', data_pedido::date) AS mes,
    ROUND(SUM(valor_total)::numeric, 2) AS faturamento
FROM pedidos
WHERE status = 'Concluído'
GROUP BY mes
ORDER BY mes;


-- ============================================================
-- 8. PEDIDOS CANCELADOS
-- ============================================================

SELECT
    COUNT(*) AS pedidos_cancelados
FROM pedidos
WHERE status = 'Cancelado';


-- ============================================================
-- 9. CLIENTES SEM PEDIDOS
-- ============================================================

SELECT
    c.id_cliente,
    c.nome
FROM clientes c
LEFT JOIN pedidos p
    ON c.id_cliente = p.id_cliente
WHERE p.id_cliente IS NULL;


-- ============================================================
-- 10. FREQUÊNCIA DE COMPRA POR CLIENTE
-- ============================================================

SELECT
    id_cliente,
    COUNT(DISTINCT id_pedido) AS frequencia_compras
FROM pedidos
WHERE status = 'Concluído'
GROUP BY id_cliente
ORDER BY frequencia_compras DESC;


-- ============================================================
-- 11. RFM - BASE
-- Recência, Frequência e Valor Monetário
-- ============================================================

SELECT
    id_cliente,

    MAX(data_pedido::date) AS ultima_compra,

    CURRENT_DATE - MAX(data_pedido::date) AS recencia,

    COUNT(DISTINCT id_pedido) AS frequencia,

    ROUND(SUM(valor_total)::numeric, 2) AS valor_monetario

FROM pedidos

WHERE status = 'Concluído'

GROUP BY id_cliente

ORDER BY valor_monetario DESC;


-- ============================================================
-- 12. RFM - SCORE DE 1 A 5
-- ============================================================

WITH rfm AS (

    SELECT
        id_cliente,

        CURRENT_DATE - MAX(data_pedido::date) AS recencia,

        COUNT(DISTINCT id_pedido) AS frequencia,

        SUM(valor_total) AS valor_monetario

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
)

SELECT

    id_cliente,

    recencia,

    frequencia,

    ROUND(valor_monetario::numeric, 2) AS valor_monetario,

    NTILE(5) OVER (
        ORDER BY recencia ASC
    ) AS score_recencia,

    NTILE(5) OVER (
        ORDER BY frequencia ASC
    ) AS score_frequencia,

    NTILE(5) OVER (
        ORDER BY valor_monetario ASC
    ) AS score_monetario

FROM rfm

ORDER BY valor_monetario DESC;


-- ============================================================
-- FIM DAS ANÁLISES ATUAIS
-- ============================================================
-- ============================================================
-- 13. CLASSIFICAÇÃO DOS CLIENTES PELO RFM
-- ============================================================

WITH rfm AS (

    SELECT
        id_cliente,

        CURRENT_DATE - MAX(data_pedido::date) AS recencia,

        COUNT(DISTINCT id_pedido) AS frequencia,

        SUM(valor_total) AS valor_monetario

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

rfm_scores AS (

    SELECT

        id_cliente,

        recencia,

        frequencia,

        valor_monetario,

        NTILE(5) OVER (
            ORDER BY recencia ASC
        ) AS score_recencia,

        NTILE(5) OVER (
            ORDER BY frequencia ASC
        ) AS score_frequencia,

        NTILE(5) OVER (
            ORDER BY valor_monetario ASC
        ) AS score_monetario

    FROM rfm
)

SELECT

    id_cliente,

    recencia,

    frequencia,

    ROUND(valor_monetario::numeric, 2) AS valor_monetario,

    score_recencia,

    score_frequencia,

    score_monetario,

    CONCAT(
        score_recencia,
        score_frequencia,
        score_monetario
    ) AS score_rfm

FROM rfm_scores

ORDER BY score_rfm DESC;

-- ============================================================
-- 14. SEGMENTAÇÃO DOS CLIENTES PELO RFM
-- ============================================================

WITH rfm AS (

    SELECT
        id_cliente,

        CURRENT_DATE - MAX(data_pedido::date) AS recencia,

        COUNT(DISTINCT id_pedido) AS frequencia,

        SUM(valor_total) AS valor_monetario

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

rfm_scores AS (

    SELECT
        id_cliente,
        recencia,
        frequencia,
        valor_monetario,

        NTILE(5) OVER (
            ORDER BY recencia ASC
        ) AS score_recencia,

        NTILE(5) OVER (
            ORDER BY frequencia ASC
        ) AS score_frequencia,

        NTILE(5) OVER (
            ORDER BY valor_monetario ASC
        ) AS score_monetario

    FROM rfm
)

SELECT

    id_cliente,

    recencia,

    frequencia,

    ROUND(valor_monetario::numeric, 2) AS valor_monetario,

    score_recencia,

    score_frequencia,

    score_monetario,

    CONCAT(
        score_recencia,
        score_frequencia,
        score_monetario
    ) AS score_rfm,

    CASE

        WHEN score_recencia >= 4
         AND score_frequencia >= 4
         AND score_monetario >= 4
            THEN 'Champions'

        WHEN score_recencia >= 4
         AND score_frequencia >= 3
            THEN 'Clientes Fiéis'

        WHEN score_recencia >= 4
         AND score_frequencia <= 2
            THEN 'Clientes Novos'

        WHEN score_recencia <= 2
         AND score_frequencia >= 4
            THEN 'Clientes em Risco'

        WHEN score_recencia <= 2
         AND score_frequencia <= 2
            THEN 'Clientes Perdidos'

        ELSE 'Clientes Potenciais'

    END AS segmento

FROM rfm_scores

ORDER BY score_rfm DESC;

-- ============================================================
-- 15. RESUMO DOS SEGMENTOS RFM
-- ============================================================

WITH rfm AS (

    SELECT
        id_cliente,

        CURRENT_DATE - MAX(data_pedido::date) AS recencia,

        COUNT(DISTINCT id_pedido) AS frequencia,

        SUM(valor_total) AS valor_monetario

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

rfm_scores AS (

    SELECT
        id_cliente,
        recencia,
        frequencia,
        valor_monetario,

        NTILE(5) OVER (
            ORDER BY recencia ASC
        ) AS score_recencia,

        NTILE(5) OVER (
            ORDER BY frequencia ASC
        ) AS score_frequencia,

        NTILE(5) OVER (
            ORDER BY valor_monetario ASC
        ) AS score_monetario

    FROM rfm
),

segmentos AS (

    SELECT

        id_cliente,
        valor_monetario,

        CASE

            WHEN score_recencia >= 4
             AND score_frequencia >= 4
             AND score_monetario >= 4
                THEN 'Champions'

            WHEN score_recencia >= 4
             AND score_frequencia >= 3
                THEN 'Clientes Fiéis'

            WHEN score_recencia >= 4
             AND score_frequencia <= 2
                THEN 'Clientes Novos'

            WHEN score_recencia <= 2
             AND score_frequencia >= 4
                THEN 'Clientes em Risco'

            WHEN score_recencia <= 2
             AND score_frequencia <= 2
                THEN 'Clientes Perdidos'

            ELSE 'Clientes Potenciais'

        END AS segmento

    FROM rfm_scores
)

SELECT

    segmento,

    COUNT(*) AS quantidade_clientes,

    ROUND(
        SUM(valor_monetario)::numeric,
        2
    ) AS faturamento_segmento,

    ROUND(
        AVG(valor_monetario)::numeric,
        2
    ) AS valor_medio_por_cliente

FROM segmentos

GROUP BY segmento

ORDER BY faturamento_segmento DESC;

-- ============================================================
-- 16. ANÁLISE DE CHURN - BASE
-- ============================================================

SELECT

    id_cliente,

    MAX(data_pedido::date) AS ultima_compra,

    CURRENT_DATE - MAX(data_pedido::date) AS dias_sem_comprar,

    COUNT(DISTINCT id_pedido) AS total_pedidos,

    ROUND(
        SUM(valor_total)::numeric,
        2
    ) AS valor_total_comprado,

    CASE

        WHEN CURRENT_DATE - MAX(data_pedido::date) >= 180
            THEN 'Churn'

        WHEN CURRENT_DATE - MAX(data_pedido::date) >= 90
            THEN 'Risco de Churn'

        ELSE 'Ativo'

    END AS status_cliente

FROM pedidos

WHERE status = 'Concluído'

GROUP BY id_cliente

ORDER BY dias_sem_comprar DESC;

-- ============================================================
-- 17. RESUMO DO CHURN
-- ============================================================

WITH clientes AS (

    SELECT

        id_cliente,

        MAX(data_pedido::date) AS ultima_compra,

        CURRENT_DATE - MAX(data_pedido::date) AS dias_sem_comprar,

        SUM(valor_total) AS valor_total_comprado

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

classificacao AS (

    SELECT

        id_cliente,

        valor_total_comprado,

        CASE

            WHEN dias_sem_comprar >= 180
                THEN 'Churn'

            WHEN dias_sem_comprar >= 90
                THEN 'Risco de Churn'

            ELSE 'Ativo'

        END AS status_cliente

    FROM clientes
)

SELECT

    status_cliente,

    COUNT(*) AS quantidade_clientes,

    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentual_clientes,

    ROUND(
        SUM(valor_total_comprado)::numeric,
        2
    ) AS faturamento_gerado

FROM classificacao

GROUP BY status_cliente

ORDER BY quantidade_clientes DESC;

-- ============================================================
-- 18. VALOR FINANCEIRO EM RISCO PELO CHURN
-- ============================================================

WITH clientes AS (

    SELECT

        id_cliente,

        CURRENT_DATE - MAX(data_pedido::date) AS dias_sem_comprar,

        SUM(valor_total) AS valor_total_comprado

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

classificacao AS (

    SELECT

        id_cliente,

        valor_total_comprado,

        CASE

            WHEN dias_sem_comprar >= 180
                THEN 'Churn'

            WHEN dias_sem_comprar >= 90
                THEN 'Risco de Churn'

            ELSE 'Ativo'

        END AS status_cliente

    FROM clientes
)

SELECT

    status_cliente,

    COUNT(*) AS quantidade_clientes,

    ROUND(
        SUM(valor_total_comprado)::numeric,
        2
    ) AS valor_historico,

    ROUND(
        AVG(valor_total_comprado)::numeric,
        2
    ) AS valor_medio_por_cliente

FROM classificacao

WHERE status_cliente IN ('Churn', 'Risco de Churn')

GROUP BY status_cliente

ORDER BY valor_historico DESC;

-- ============================================================
-- 19. CLIENTES DE ALTO VALOR EM RISCO
-- ============================================================

WITH clientes AS (

    SELECT

        id_cliente,

        MAX(data_pedido::date) AS ultima_compra,

        CURRENT_DATE - MAX(data_pedido::date) AS dias_sem_comprar,

        COUNT(DISTINCT id_pedido) AS total_pedidos,

        SUM(valor_total) AS valor_total_comprado

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
)

SELECT

    id_cliente,

    ultima_compra,

    dias_sem_comprar,

    total_pedidos,

    ROUND(
        valor_total_comprado::numeric,
        2
    ) AS valor_total_comprado

FROM clientes

WHERE dias_sem_comprar >= 90

ORDER BY valor_total_comprado DESC

LIMIT 100;

-- ============================================================
-- 20. COHORT ANALYSIS - RETENÇÃO DE CLIENTES
-- ============================================================

WITH primeira_compra AS (

    SELECT
        id_cliente,
        DATE_TRUNC(
            'month',
            MIN(data_pedido::date)
        ) AS mes_cohort

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

compras AS (

    SELECT DISTINCT
        p.id_cliente,

        DATE_TRUNC(
            'month',
            p.data_pedido::date
        ) AS mes_compra

    FROM pedidos p

    WHERE p.status = 'Concluído'
),

cohort AS (

    SELECT

        pc.mes_cohort,

        c.mes_compra,

        COUNT(DISTINCT c.id_cliente) AS clientes

    FROM primeira_compra pc

    JOIN compras c
        ON pc.id_cliente = c.id_cliente

    GROUP BY
        pc.mes_cohort,
        c.mes_compra

)

SELECT

    mes_cohort,

    mes_compra,

    clientes

FROM cohort

ORDER BY
    mes_cohort,
    mes_compra;

    -- ============================================================
-- 21. COHORT ANALYSIS - PERCENTUAL DE RETENÇÃO
-- ============================================================

WITH primeira_compra AS (

    SELECT
        id_cliente,
        DATE_TRUNC(
            'month',
            MIN(data_pedido::date)
        ) AS mes_cohort

    FROM pedidos

    WHERE status = 'Concluído'

    GROUP BY id_cliente
),

compras AS (

    SELECT DISTINCT
        id_cliente,

        DATE_TRUNC(
            'month',
            data_pedido::date
        ) AS mes_compra

    FROM pedidos

    WHERE status = 'Concluído'
),

cohort AS (

    SELECT

        pc.mes_cohort,

        c.mes_compra,

        COUNT(DISTINCT c.id_cliente) AS clientes

    FROM primeira_compra pc

    JOIN compras c
        ON pc.id_cliente = c.id_cliente

    GROUP BY
        pc.mes_cohort,
        c.mes_compra
),

clientes_iniciais AS (

    SELECT

        mes_cohort,

        clientes AS clientes_iniciais

    FROM cohort

    WHERE mes_cohort = mes_compra
)

SELECT

    c.mes_cohort,

    c.mes_compra,

    c.clientes,

    ci.clientes_iniciais,

    ROUND(
        c.clientes * 100.0
        / ci.clientes_iniciais,
        2
    ) AS percentual_retencao

FROM cohort c

JOIN clientes_iniciais ci
    ON c.mes_cohort = ci.mes_cohort

ORDER BY
    c.mes_cohort,
    c.mes_compra;