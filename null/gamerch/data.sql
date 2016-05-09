SELECT 
    tbl3.rarity_id as rarity_id,
    tbl3.short_name as rarity_name,
    tbl1.name,
    tbl1.cost,
    tbl1.p_vit,
    tbl1.p_int,
    tbl1.p_chr,
    tbl8.name as good_subject,
    tbl9.name as bad_subject,
    tbl10.name as attribute,
    tbl7.name as group_name,
    tbl2.name as skill_name,
    tbl2.n_text as skill_text,
    tbl4.name as fskill,
    tbl4.text as fskill_text,
    tbl4.consume_point as fskill_consume_point,
    tbl4.limit_count as fskill_limit_count,
    tbl5.name as bskill,
    tbl5.text as bskill_text,
    tbl5.consume_point as bskill_consume_point,
    tbl5.limit_count as bskill_limit_count,
    tbl1.flavor_r1,
    tbl1.flavor_r3,
    tbl1.flavor_r5
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
        LEFT JOIN
    charactor_charactor as tbl6 ON tbl6.charactor_id = tbl1.charactor_id
        LEFT JOIN
    charactor_group as tbl7 ON tbl7.group_id = tbl6.group_id
        LEFT JOIN
    charactor_subject as tbl8 ON tbl8.subject_id = tbl6.good_subject_id
        LEFT JOIN
    charactor_subject as tbl9 ON tbl9.subject_id = tbl6.bad_subject_id
        LEFT JOIN
    card_attribute as tbl10 ON tbl10.attribute_id = tbl1.param_type
order by rarity_id DESC