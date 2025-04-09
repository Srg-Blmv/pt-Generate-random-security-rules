#### mix_1
`random_mix_1_ip_obj`
>создает объекты:
1: dst src IP адреса
2: dst src IP cети
3: network range  - При создание могу быть ошибки если from > to
4: fqdn

`random_mix_1_rules`
> на основе созданных объектов генериурет правила вида:

| Name            |Zone   | Address                                                                          | User      | Zone   | Address                                  | Security Profiles   | Application   | URL Category          | Service       | Action           | Logging               
|-----------------|-------|------------------------------------------------------------------------------------|-----------|--------|-----------------------------------------|---------------------|---------------|-------------------------|----------------|-------------------|------------------------|
| Random_Rule_0   | DMZ   | Source_range_1_55_128_36, fqdn_s96f3ntj2cdbka.org, Source_ip_7_85_60_36, Source_ip_3_67_84_196, Source_net_5_83_91_59 | Any       | DMZ    | Dest_net_1_179_13_217, fqdn_9il17an8l408dlv.org, Dest_range_4_9_218_18, Dest_ip_3_29_39_39, Dest_ip_2_80_152_9 | None          | diff-now    | German Youth Protection | r_44579, r_19654, r_57406, r_8528, r_31115 | Reset server | At session start and end |              |

**src zone:** 1
**dst zone:** 1
**src ip:** 2 ip, 1 range, 1 fqdn, 1 network 
**dst ip:** 2 ip, 1 range, 1 fqdn, 1 network 
**app:** 1
**log:** random
**url:** 1
**action:**: random

---