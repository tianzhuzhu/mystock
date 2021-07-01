#取最大日期的所有
select bb.* from
                (select code,max(date) date from tb_bi_akshare_yjbb GROUP BY `code`) tmp,tb_bi_akshare_yjbb bb
where bb.code=tmp.code
  and bb.date=tmp.date
