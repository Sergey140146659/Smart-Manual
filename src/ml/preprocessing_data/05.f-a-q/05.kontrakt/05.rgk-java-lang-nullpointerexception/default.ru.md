---
title: 'РГК. java.lang.NullPointerException...'
---

РГК. java.lang.NullPointerException at deployment.rgk-integration-adapter-ear.ear.rgk-integration-adapter.war//ru.lanit.rgk.integration.adapter.mapper.contractinfo.ContractInfo2015Mapper.fillAccountInfos(ContractInfo2015Mapper.java:6037) at deployment.rgk-integration-adapter-ear.ear.rgk-integration-adapter.war//ru.lanit.rgk.integration.adapter.mapper.contractinfo.ContractInfo2015Mapper.mapSuppliersInfo(ContractInfo2015Mapper.java:5448) at deployment.rgk-integration-adapter-ear.ear.rgk-integration-adapter.war//ru.lanit.rgk.integration.adapter.mapper.contractinfo.ContractInfo2015Mapper.map(ContractInfo2015Mapper.java:829) at deployment.rgk-integration-adapter-ear.ear.rgk-integration-

Причина появления данной ошибки в использовании неактуального БИК. Об этом же пишет служба технической поддержки ЕИС (далее – СТП ЕИС). Цитата ответа СТП ЕИС: 
1. «В передаваемом пакете в платёжных реквизитах поставщика указан неактуальный БИК. Просьба указать БИК, который будет присутствовать в актуальном состоянии и повторить интеграцию.
2. Если в пакете указан тип счёта: 03 - "Расчетный счет в банке", 04 - "Счет эскроу" , или ("05 - Счет для перечисления денежных средств" и не заполнено поле "Номер лицевого счёта" (personalAccountNumber)), то значение БИК должно быть актуально в справочнике НСИ БИК.
3. Если тип счёта 01- "Лицевой счет в ФК", 02 - "Лицевой счет в ФО", 06 - "Счет для уплаты налогов" или ("05 - Счет для перечисления денежных средств" и заполнено поле "Номер лицевого счёта" (personalAccountNumber)), то значение БИК должно быть актуально в справочнике КРКС.»
В данном случае необходимо проверить БИК на предмет актуальности. В случае обнаружения неактуального БИК следует в передаваемых сведениях о заключенном контракте указать счет с актуальным БИК банка.
