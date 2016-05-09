SELECT 
    concat('|center:[[',
            replace(replace(card_card.name, '[', '【'),
                ']',
                '】'),
            '>カード_',
            replace(replace(card_card.name, '[', '【'),
                ']',
                '】'),
            ']]|center:[[',
            tbl1.short_name,
            ']]|center:',
            p_vit,
            '|center:',
            p_int,
            '|center:',
            p_chr,
            '|')
FROM
    card_card
        LEFT JOIN
    card_rarity as tbl1 ON tbl1.rarity_id = card_card.rarity_id
order by (p_vit+p_int+p_chr) desc