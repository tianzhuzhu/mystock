select t.* from tb_industry_information t,
                (SELECT max(updateDate) updateDate,code FROM `stock`.`tb_industry_information` group by code) time
where t.updateDate=time.updateDate and t.code=time.code