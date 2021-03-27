select his.volume,his.date,pe.*,close ,growth.YOYNI  from tb_stock_hisotry_detatil his,

                                (select tt.code,tt.peTTM,tt.pbMRQ,tt.psTTM,tt.pcfNcfTTM
                                 from tb_stock_hisotry_detatil tt ,
                                      (select code, max(date) as date from tb_stock_hisotry_detatil group by code) t
                                 where t.code=tt.`code` and t.date=tt.date and tt.peTTM >0 and tt.peTTM <{}) as pe
        ,
                                (select tt.code,tt.YOYAsset,tt.YOYNI,tt.YOYEPSBasic,tt.YOYPNI
                                 from tb_growth tt ,
                                      (select code, max(date) as date from tb_growth group by code) t
                                 where t.code=tt.`code` and t.date=tt.date and tt.YOYNI>{})  as growth
WHERE growth.code=pe.code
  and his.code=growth.code