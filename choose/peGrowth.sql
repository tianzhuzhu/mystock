select his.* from tb_stock_hisotry_detatil his,
                  (select pe.code from
                                      (select tt.*
                                       from tb_stock_hisotry_detatil tt ,
                                            (select code, max(date) as date from tb_stock_hisotry_detatil group by code) t
                                       where t.code=tt.`code` and t.date=tt.date) pe
                          ,
                                      (select tt.*
                                       from tb_growth tt ,
                                            (select code, max(date) as date from tb_growth group by code) t
                                       where t.code=tt.`code` and t.date=tt.date and tt.YOYNI>{}) growth
                   WHERE growth.code=pe.code and peTTM >0 and peTTM <{} ) allcode
where his.code=allcode.code