. #当前
select bb.* from
                (select code,max(date) date from tb_bi_akshare_yjbb bb1  GROUP BY `code`) tmp,tb_bi_akshare_yjbb bb,
                tb_today_stock ts
where ts.symbol=bb.code
  and bb.code=tmp.code
  and bb.date=tmp.date