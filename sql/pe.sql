select tt.code,tt.peTTM,tt.pbMRQ,tt.psTTM,tt.pcfNcfTTM
from tb_stock_hisotry_detatil tt ,
     (select code, max(date) as date from tb_stock_hisotry_detatil group by code) t
where t.code=tt.`code` and t.date=tt.date