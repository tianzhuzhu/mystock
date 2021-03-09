select * from
         (select tt.*
          from tb_stock_hisotry_detatil tt ,
               (select code, max(date) as date from tb_stock_hisotry_detatil group by code) t
          where t.code=tt.`code` and t.date=tt.date) pe
    ,
         (select tt.*
          from tb_growth tt ,
               (select code, max(date) as date from tb_growth group by code) t
          where t.code=tt.`code` and t.date=tt.date and tt.YOYNI>0.5) growth
WHERE growth.code=pe.code and peTTM >0 and peTTM <25  ORDER BY  YOYNI desc

-- 查询pe与增长率