SELECT 
    concat('|center:[[',
            replace(replace(tbl1.name, '[', '【'),
                ']',
                '】'),
            '>カード_',
            replace(replace(tbl1.name, '[', '【'),
                ']',
                '】'),
            ']]|',
            IFNULL(tbl2.name, 'center:-'),
            '|',
            IFNULL(tbl2.n_text, 'center:-'),
            '|center:',
            IFNULL(tbl4.name, '-'),
            '|',
            IFNULL(tbl4.text, 'center:-'),
            '|center:',
            IFNULL(tbl4.consume_point, '-'),
            '|center:',
            IFNULL(tbl4.limit_count, '-'),
            '|center:',
            IFNULL(tbl5.name, '-'),
            '|',
            IFNULL(tbl5.text, 'center:-'),
            '|center:',
            IFNULL(tbl5.consume_point, '-'),
            '|center:',
            IFNULL(tbl5.limit_count, '-'),
            '|')
FROM
    card_card as tbl1
        LEFT JOIN
    cardskill_cardskill as tbl2 ON tbl2.card_id = tbl1.card_id
        LEFT JOIN
    card_rarity as tbl3 ON tbl3.rarity_id = tbl1.rarity_id
        LEFT JOIN
    cardskill_forwardskill as tbl4 ON tbl4.fskill_id = tbl1.fskill_id
        LEFT JOIN
    cardskill_backskill as tbl5 ON tbl5.bskill_id = tbl1.bskill_id
where
    tbl3.rarity_id = 6
order by (p_vit + p_int + p_chr) desc