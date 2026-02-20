# Лабораторная работа №12 — Маршрутизация сетей с помощью протокола MPLS

 + [Все лабораторные работы по сетевым протоколам в Linux](../Intro.md)
 + [Предыдущая лабораторная работа — VPN и туннелирование](../11_WG_IPIP/VPN%20и%20туннелирование.md)

---

## Быстрый поиск по лабораторной:
 + [MultiProtocol Label Switching](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#MultiProtocol-Label-Switching)
 + [Пример настройки MPLS](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Пример-настройки-MPLS)
	 + [Базовая настройка сети](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Базовая-настройка-сети)
 + [FRRouting](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#FRRouting)
 + [Настройка MPLS-маршрутизации](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Настройка-MPLS-маршрутизации)
	 + [Активация служб](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Активация-служб)
	 + [Описание конфигурационных файлов](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Описание-конфигурационных-файлов)
	 + [Аппаратная поддержка MPLS](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Аппаратная-поддержка-MPLS)
 + [Маршрутизация по меткам](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Маршрутизация-по-меткам)
	 + [Запуск системы](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Запуск-системы)
	 + [Мониторинг настроек](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Мониторинг-настроек)
	 + [Просмотр трафика](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Просмотр-трафика)
 + [Самостоятельная работа](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Самостоятельная-работа)
	 + [Варианты заданий](./home/papillon_rouge/Nets_ASVK_Labs/12_MPLS/Маршрутизация%20сетей%20с%20помощью%20протокола%20MPLS.md#Варианты-заданий)

**Цель лабораторной** — познакомить изучающего с основами работы списков контроля доступа

**Задачи лабораторной:**

- Изучить логику работы списков контроля доступа;
- Реализовать тестовую топологию с применением списков контроля доступа.

---

## MultiProtocol Label Switching

Протокол [MPLS](https://ru.wikipedia.org/wiki/MPLS) — протокол маршрутизации по меткам. Несмотря на связь с сетевым уровнем стека TCP/IP данный протокол правильнее относить к интерфейсному уровню.

MPLS настраивается поверх существующей маршрутизируемой IP-сети. Для каждого пути маршрутизаторы локально собирают таблицу меток, а после обмениваются ею с ближайшими соседями для обеспечения связности.

Использование меток для маршрутизации ускоряет передачу данных, поскольку вместо сравнения IP получателя по таблице с линейной скоростью (поскольку поиск ведётся по правилу наибольшего префикса, необходимо просматривать все записи таблицы) маршрутизаторы выполняют простые действия с константной скоростью:
 + Посмотреть входящую метку на пакете;
 + В хеш-таблице найти данную запись по данной метке;
 + Поменять метку на исходящую (возможно, ту же самую / пустую);
 + Отправить пакет в нужный сетевой интерфейс.

---

## Пример настройки MPLS

Для изучения маршрутизации с помощью MPLS разберём топологию связи двух абонентов через три маршрутизатора:

![](Attached_materials/12_MPLS.png)

Для работы создадим 5 [клонов](../01_FirstStart/Настройка%20системы%20для%20выполнения%20лабораторных.md) согласно топологии сети. Для создания соединений между машинами необходимо в VirtualBox настроить сетевые интерфейсы (описание настройки подключения находится в разделе [настройки сетевых подключений](../02_SystemGreetings/Знакомство%20с%20системой.md#работа-с-сетевыми-интерфейсами)):

 + `PC1`:
	 + Adapter2 — intnet
 + `PC2`:
	 + Adapter2 — deepnet
 + `R1`:
	 + Adapter2 — intnet
	 + Adapter3 — mpls1
 + `R2`:
	 + Adapter2 — mpls1
	 + Adapter3 — mpls2
 + `R3`:
	 + Adapter2 — deepnet
	 + Adapter3 — mpls2

---

### Базовая настройка сети

Для настройки сетей воспользуйтесь [Systemd](https://ru.wikipedia.org/wiki/Systemd), аналогично настройке прошлой лабораторной. С помощью конфигурационных файлов задайте:
 + Адреса на соответствующих интерфейсах;
 + Пробрасывание пакетов между интерфейсами (IPv4Forwarding);

Все конфигурационные файлы записываются в директорию `/etc/systemd/network/` и называются `<name>.network`. Systemd-networkd — служба, управляющая сетевыми настройками, — выполняет настройки в лексикографическом порядке названий файлов, поэтому принято называть их, начиная с номера, чтобы соблюдать последовательность.

:round_pushpin: 1. Скопируйте или перепишите конфигурационные файлы настройки в соответствующие виртуальные машины.

`@PC1`:`/etc/systemd/network/50-intnet.network`
```systemd
[Match]
Name=eth1

[Network]
Address=10.0.1.254/24
```


`@PC2`:`/etc/systemd/network/50-deepnet.network`
```systemd
[Match]
Name=eth1

[Network]
Address=10.0.2.254/24
```


`@R1`:`/etc/systemd/network/10-lo.network`
```systemd
[Match]
Name=lo

[Network]
Address=1.1.1.1/24
```

`@R1`:`/etc/systemd/network/50-intnet.network`
```systemd
[Match]
Name=eth1

[Network]
Address=10.0.1.1/24
IPv4Forwarding=yes
```

`@R1`:`/etc/systemd/network/60-mpls1.network`
```systemd
[Match]
Name=eth2

[Network]
Address=10.0.12.1/24
IPv4Forwarding=yes
```


`@R3`:`/etc/systemd/network/10-lo.network`
```systemd
[Match]
Name=lo

[Network]
Address=3.3.3.3/24
```

`@R3`:`/etc/systemd/network/50-deepnet.network`
```systemd
[Match]
Name=eth1

[Network]
Address=10.0.2.3/24
IPv4Forwarding=yes
```

`@R3`:`/etc/systemd/network/60-mpls2.network`
```systemd
[Match]
Name=eth2

[Network]
Address=10.0.23.3/24
```


`@R2`:`/etc/systemd/network/10-lo.network`
```systemd
[Match]
Name=lo

[Network]
Address=2.2.2.2/24
```

`@R2`:`/etc/systemd/network/50-mpls1.network`
```systemd
[Match]
Name=eth1

[Network]
Address=10.0.12.2/24
IPv4Forwarding=yes
```

`@R2`:`/etc/systemd/network/60-mpls2.network`
```systemd
[Match]
Name=eth2

[Network]
Address=10.0.23.2/24
IPv4Forwarding=yes
```

:round_pushpin: 2. На каждой виртуальной машине включите службу `systemd-networkd` и с помощью _команд настройки IP-адресов_ выведите состояние интерфейсов:

`@PC1`
```console
[root@PC1 ~]# systemctl enable --now systemd-networkd
<...>
[root@PC1 ~]#
[root@PC1 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:9b:30:4f brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname enx0800279b304f
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:d7:88:2d brd ff:ff:ff:ff:ff:ff
    altname enp0s8
    altname enx080027d7882d
    inet 10.0.1.254/24 brd 10.0.1.255 scope global eth1
       valid_lft forever preferred_lft forever
4: eth2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:b3:86:9f brd ff:ff:ff:ff:ff:ff
    altname enp0s9
    altname enx080027b3869f
5: eth3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:b3:96:e8 brd ff:ff:ff:ff:ff:ff
    altname enp0s10
    altname enx080027b396e8
[root@PC1 ~]#
```

`@PC2`
```console
[root@PC2 ~]# systemctl enable --now systemd-networkd
<...>
[root@PC2 ~]#
[root@PC2 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:c2:28:33 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname enx080027c22833
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:6d:c8:3a brd ff:ff:ff:ff:ff:ff
    altname enp0s8
    altname enx0800276dc83a
    inet 10.0.2.254/24 brd 10.0.2.255 scope global eth1
       valid_lft forever preferred_lft forever
4: eth2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:05:8e:33 brd ff:ff:ff:ff:ff:ff
    altname enp0s9
    altname enx080027058e33
5: eth3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:da:e4:af brd ff:ff:ff:ff:ff:ff
    altname enp0s10
    altname enx080027dae4af
[root@PC2 ~]#
```

`@R1`
```console
[root@R1 ~]# systemctl enable --now systemd-networkd
<...>
[root@R1 ~]#
[root@R1 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 1.1.1.1/24 brd 1.1.1.255 scope global lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:f4:7f:04 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname enx080027f47f04
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:24:90:2b brd ff:ff:ff:ff:ff:ff
    altname enp0s8
    altname enx08002724902b
    inet 10.0.1.1/24 brd 10.0.1.255 scope global eth1
       valid_lft forever preferred_lft forever
4: eth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:68:94:0e brd ff:ff:ff:ff:ff:ff
    altname enp0s9
    altname enx08002768940e
    inet 10.0.12.1/24 brd 10.0.12.255 scope global eth2
       valid_lft forever preferred_lft forever
5: eth3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:e6:a6:f4 brd ff:ff:ff:ff:ff:ff
    altname enp0s10
    altname enx080027e6a6f4
[root@R1 ~]#
```

`@R2`
```console
[root@R2 ~]# systemctl enable --now systemd-networkd
<...>
[root@R2 ~]#
[root@R2 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 2.2.2.2/24 brd 2.2.2.255 scope global lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:92:8f:47 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname enx080027928f47
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:0c:43:a5 brd ff:ff:ff:ff:ff:ff
    altname enp0s8
    altname enx0800270c43a5
    inet 10.0.12.2/24 brd 10.0.12.255 scope global eth1
       valid_lft forever preferred_lft forever
4: eth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:55:e8:05 brd ff:ff:ff:ff:ff:ff
    altname enp0s9
    altname enx08002755e805
    inet 10.0.23.2/24 brd 10.0.23.255 scope global eth2
       valid_lft forever preferred_lft forever
5: eth3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:64:94:00 brd ff:ff:ff:ff:ff:ff
    altname enp0s10
    altname enx080027649400
[root@R2 ~]#
```

`@R3`
```console
[root@R3 ~]# systemctl enable --now systemd-networkd
<...>
[root@R3 ~]#
[root@R3 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 3.3.3.3/24 brd 3.3.3.255 scope global lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:90:a7:4f brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname enx08002790a74f
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:68:bd:29 brd ff:ff:ff:ff:ff:ff
    altname enp0s8
    altname enx08002768bd29
    inet 10.0.2.3/24 brd 10.0.2.255 scope global eth1
       valid_lft forever preferred_lft forever
4: eth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:1a:ec:be brd ff:ff:ff:ff:ff:ff
    altname enp0s9
    altname enx0800271aecbe
    inet 10.0.23.3/24 brd 10.0.23.255 scope global eth2
       valid_lft forever preferred_lft forever
5: eth3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:35:15:0b brd ff:ff:ff:ff:ff:ff
    altname enp0s10
    altname enx08002735150b
[root@R3 ~]#
```

---

## FRRouting

:information_source: Для работы протоколов (в частности, протоколов маршрутизации) необходимо использовать специальные программы-менеджеры, которые управляют настройками и параметрами протоколов — Routing Daemons. Для выполнения данной лабораторной используется демон [FRRouting](https://docs.frrouting.org/en/stable-10.5/). Демон управляет сразу несколькими службами, настроенными на конкретные протоколы, собирая все настройки в один конфигурационный файл `/etc/frr/frr.conf`

---

## Настройка MPLS-маршрутизации

Для настройки MPLS-маршрутизации с помощью FRRouting необходимо:
 + Активировать соответствующие службы;
 + Описать конфигурационный файл;
 + Включить аппаратную поддержку MPLS.
---

### Активация служб

Все зависимые службы FRRouting описаны в файле `/etc/frr/daemons`. Для нашей работы необходимо на всех машинах активировать OSPF daemon для настройки маршрутизации, поверх которой будет работать MPLS. Также на маршрутизаторах необходимо включить демона LDP (Label Distribution Protocol) для автораспространения меток между маршрутизаторами (без этого каждую метку и правило для неё необходимо было бы настраивать вручную).

Включение соответствующих демонов можно сделать с помощью явного исправления файла (открыть файл → Внести исправление → сохраниться и выйти) или с помощью автозамены по шаблону, используя [sed](https://www.opennet.ru/man.shtml?topic=sed&category=1).

:round_pushpin: 1. На виртуальных машинах отредактируйте файлы /etc/frr/daemons:
 + Самостоятельно укажите необходимые демоны или используйте команду `sed -i -E "s/<шаблон_поиска>/<замена>/g"`
 + Проверьте корректность изменения с помощью `cat /etc/frr/daemons | grep yes`

`@PC1`
```console
[root@PC1 ~]# sed -i -E "s/ospfd=no/ospfd=yes/g" /etc/frr/daemons
[root@PC1 ~]# cat /etc/frr/daemons | grep yes
ospfd=yes
vtysh_enable=yes
# FRR_NO_ROOT="yes"
[root@PC1 ~]#
```

`@PC2`
```console
[root@PC2 ~]# sed -i -E "s/ospfd=no/ospfd=yes/g" /etc/frr/daemons
[root@PC2 ~]# cat /etc/frr/daemons | grep yes
ospfd=yes
vtysh_enable=yes
# FRR_NO_ROOT="yes"
[root@PC2 ~]#
```

`@R1`
```console
[root@R1 ~]# sed -i -E "s/ospfd=no/ospfd=yes/g" /etc/frr/daemons
[root@R1 ~]# sed -i -E "s/ldpd=no/ldpd=yes/g" /etc/frr/daemons
[root@R1 ~]# cat /etc/frr/daemons | grep yes
ospfd=yes
ldpd=yes
vtysh_enable=yes
# FRR_NO_ROOT="yes"
[root@R1 ~]#
```

`@R2`
```console
[root@R2 ~]# sed -i -E "s/ospfd=no/ospfd=yes/g" /etc/frr/daemons
[root@R2 ~]# sed -i -E "s/ldpd=no/ldpd=yes/g" /etc/frr/daemons
[root@R2 ~]# cat /etc/frr/daemons | grep yes
ospfd=yes
ldpd=yes
vtysh_enable=yes
# FRR_NO_ROOT="yes"
[root@R2 ~]#
```

`@R3`
```console
[root@R3 ~]# sed -i -E "s/ospfd=no/ospfd=yes/g" /etc/frr/daemons
[root@R3 ~]# sed -i -E "s/ldpd=no/ldpd=yes/g" /etc/frr/daemons
[root@R3 ~]# cat /etc/frr/daemons | grep yes
ospfd=yes
ldpd=yes
vtysh_enable=yes
# FRR_NO_ROOT="yes"
[root@R3 ~]#
```

---

### Описание конфигурационных файлов

Для описания настроек FRRouting используется конфигурационный файл `/etc/frr/frr.conf`

В нём указываются базовые параметры для устройства (hostname, файл для логирования данных) и настройки соответствующих демонов.

:information_source: Настройка OSPF в FRRouting отличается от настройки BIRD: здесь явно указываются сети, связь с которыми осуществляется в рамках указанной зоны, подразумевая распространение информации о состоянии каналов по всех интерфейсам (в отличие от BIRD, где настройка производится с точностью наоборот).

:round_pushpin: 1. Скопируйте или перепишите конфигурационные файлы настройки в соответствующие виртуальные машины.

`@PC1`: `/etc/frr/frr.conf`
```frr
hostname PC1
log file /var/log/frr/frr.log

router ospf
    ospf router 10.0.1.254
        network 0.0.0.0/0 area 0
    !
exit
```

`@PC2`: `/etc/frr/frr.conf`
```frr
hostname PC2
log file /var/log/frr/frr.log

router ospf
    ospf router 10.0.2.254
        network 0.0.0.0/0 area 0
    !
exit
```

`@R1`: `/etc/frr/frr.conf`
```frr
hostname R1
log file /var/log/frr/frr.log

router ospf
    ospf router 1.1.1.1
        network 0.0.0.0/0 area 0
    !
exit

mpls ldp
    router-id 1.1.1.1
    !
    address-family ipv4
        discovery transport-address 1.1.1.1
        !
        interface eth2
        exit
        !
    exit-address-family
    !
exit
```

`@R2`: `/etc/frr/frr.conf`
```frr
hostname R2
log file /var/log/frr/frr.log

router ospf
    ospf router 2.2.2.2
        network 0.0.0.0/0 area 0
    !
exit

mpls ldp
    router-id 2.2.2.2
    !
    address-family ipv4
        discovery transport-address 2.2.2.2
        !
        interface eth1
        exit
        !
        interface eth2
        exit
        !
    exit-address-family
    !
exit
```

`@R3`: `/etc/frr/frr.conf`
```frr
hostname R3
log file /var/log/frr/frr.log

router ospf
    ospf router 3.3.3.3
        network 0.0.0.0/0 area 0
    !
exit

mpls ldp
    router-id 3.3.3.3
    !
    address-family ipv4
        discovery transport-address 3.3.3.3
        !
        interface eth2
        exit
        !
    exit-address-family
    !
exit
```

:information_source: Описание настройки MPLS LDP требует большей строгости: необходимо явно указать версию IP, над адресами которой будет разворачиваться настройка, а также <!>

---

### Аппаратная поддержка MPLS

Для того, чтобы система выделила в памяти место для таблицы меток и обрабатывала MPLS-пакеты, необходимо загрузить соответсвующие модули ядра:
 + mpls_router — Работа с MPLS на уровне системы
 + mpls_iptunnel — Инкапсулирование IP-пакетов в MPLS

Также необходимо установить параметры входных интерфейсов (откуда на устройство будут поступать MPLS-пакеты) и размера MPLS-таблицы.

:round_pushpin: 1. С помощью команд `modprobe <module>` и `sysctl -w net.mpls.<param>` загрузите необходимые параметры виртуальным машинам.

`@R1`
```console
[root@R1 ~]# modprobe mpls_router
[root@R1 ~]# modprobe mpls_iptunnel
[root@R1 ~]# sysctl -w net.mpls.conf.eth2.input=1
[root@R1 ~]# sysctl -w net.mpls.platform_labels=10000
[root@R1 ~]#
```

`@R2`
```console
[root@R2 ~]# modprobe mpls_router
[root@R2 ~]# modprobe mpls_iptunnel
[root@R2 ~]# sysctl -w net.mpls.conf.eth1.input=1
[root@R2 ~]# sysctl -w net.mpls.conf.eth2.input=1
[root@R2 ~]# sysctl -w net.mpls.platform_labels=10000
[root@R2 ~]#
```

`@R3`
```console
[root@R3 ~]# modprobe mpls_router
[root@R3 ~]# modprobe mpls_iptunnel
[root@R3 ~]# sysctl -w net.mpls.conf.eth2.input=1
[root@R3 ~]# sysctl -w net.mpls.platform_labels=10000
[root@R3 ~]#
```

---

## Маршрутизация по меткам

---

### Запуск системы

:round_pushpin: 1. С помощью команды `systemctl enable --now frr.service` запустите сервис

`@PC1`
```console
[root@PC1 ~]# systemctl enable --now frr
[root@PC1 ~]#
```

`@PC2`
```console
[root@PC2 ~]# systemctl enable --now frr
[root@PC2 ~]#
```

`@R1`
```console
[root@R1 ~]# systemctl enable --now frr
[root@R1 ~]#
```

`@R2`
```console
[root@R2 ~]# systemctl enable --now frr
[root@R2 ~]#
```

`@R3`
```console
[root@R3 ~]# systemctl enable --now frr
[root@R3 ~]#
```

:information_source: Для применения всех настроек после запуска понадобится некоторое время.

---

### Мониторинг настроек

Для просмотра настроек используется мониторинг-утилита `vtysh`

:round_pushpin: 1. На R2 запустите утилиту vtysh

`@R2`
```console
[root@R2 ~]# vtysh

Hello, this is FRRouting (version 10.3.1).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

R2#
```

Для просмотра соседей, с которыми установлен обмен метками, используется команда `show mpls ldp neighbor`

:round_pushpin: 2. С помощью команды `show mpls ldp neighbor` выведите MPLS-соседей маршрутизатора R2

`@R2`
```
R2# show mpls ldp neighbor
AF   ID              State       Remote Address    Uptime
ipv4 1.1.1.1         OPERATIONAL 1.1.1.1         00:10:27
ipv4 3.3.3.3         OPERATIONAL 3.3.3.3         00:10:19

R2#
```

Для просмотра таблицы меток используется команда `show mpls table`

:round_pushpin: 3. С помощью команды `show mpls table` выведите таблицу меток маршрутизатора

`@R2`
```
R2# show mpls table
 Inbound Label  Type  Nexthop    Outbound Label
 ------------------------------------------------
 18             LDP   10.0.12.1  implicit-null
 19             LDP   10.0.23.3  implicit-null

R2#
```

Просмотреть все пути и метки, которыми обменялись маршрутизаторы, а также отследить те, которые применены на маршрутизаторе, можно с помощью команды `show mpls ldp binding`

:round_pushpin: 4. С помощью команды `show mpls ldp binding` выведите полный список путей и меток обмена с соседями:

`@R2`
```
R2# show mpls ldp binding
AF   Destination          Nexthop         Local Label Remote Label  In Use
ipv4 1.1.1.0/24           1.1.1.1         -           imp-null          no
ipv4 1.1.1.1/32           3.3.3.3         16          16                no
ipv4 2.2.2.0/24           0.0.0.0         imp-null    -                 no
ipv4 2.2.2.2/32           1.1.1.1         -           16                no
ipv4 2.2.2.2/32           3.3.3.3         -           17                no
ipv4 3.3.3.0/24           3.3.3.3         -           imp-null          no
ipv4 3.3.3.3/32           1.1.1.1         18          18                no
ipv4 10.0.1.0/24          1.1.1.1         17          imp-null         yes
ipv4 10.0.1.0/24          3.3.3.3         17          18                no
ipv4 10.0.2.0/24          1.1.1.1         19          19                no
ipv4 10.0.2.0/24          3.3.3.3         19          imp-null         yes
ipv4 10.0.12.0/24         1.1.1.1         imp-null    imp-null          no
ipv4 10.0.12.0/24         3.3.3.3         imp-null    19                no
ipv4 10.0.23.0/24         1.1.1.1         imp-null    17                no
ipv4 10.0.23.0/24         3.3.3.3         imp-null    imp-null          no

```

---

### Просмотр трафика

Рассмотрим, как MPLS-трафик перемещается в сети

 :r: С помощью _команд мониторинга сети_ запустите отслеживание трафика на соответствующих интерфейсах:
  + R1:eth2
  + R2:eth1
  + R3:eth2
Добавьте на вывод фильтр MPLS-сообщений

`@R1`
```console
[root@R1 ~]# tcpdump -i eth2 | grep MPLS
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth2, link-type EN10MB (Ethernet), snapshot length 262144 bytes

```

`@R2`
```console
[root@R2 ~]# tcpdump -i eth1 | grep MPLS
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
```

`@R3`
```console
[root@R3 ~]# tcpdump -i eth2 | grep MPLS
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth2, link-type EN10MB (Ethernet), snapshot length 262144 bytes

```

 :r: С помощью _команд мониторинга сети_ запустите отслеживание трафика на PC2. Добавьте на вывод фильтр ping-сообщений от PC1

`@PC2`
```console
[root@PC2 ~]# tcpdump -i eth1 | grep 10.0.1.254
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes

```

:information_source: Фильтры на вывод ставятся по причине постоянного трафика от OSPF и LDP, которые в реальном времени обновляют маршруты на случай их изменения.

:round_pushpin: 1. Запустите трафик между PC1 и PC2

`@PC1`
```console
[root@PC1 ~]# ping -c5 10.0.2.254
PING 10.0.2.254 (10.0.2.254) 56(84) bytes of data.
64 bytes from 10.0.2.254: icmp_seq=1 ttl=61 time=4.96 ms
64 bytes from 10.0.2.254: icmp_seq=2 ttl=61 time=4.28 ms
64 bytes from 10.0.2.254: icmp_seq=3 ttl=61 time=5.35 ms
64 bytes from 10.0.2.254: icmp_seq=4 ttl=61 time=4.85 ms
64 bytes from 10.0.2.254: icmp_seq=5 ttl=61 time=3.61 ms

--- 10.0.2.254 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 3.612/4.610/5.351/0.604 ms
[root@PC1 ~]#
```


`@R1`
```console
[root@R1 ~]# tcpdump -i eth2 | grep MPLS
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth2, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:27:58.090702 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 1, length 64
14:27:59.092017 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 2, length 64
14:28:00.093030 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 3, length 64
14:28:01.093749 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 4, length 64
14:28:02.095492 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 5, length 64

```

`@R2`
```console
[root@R2 ~]# tcpdump -i eth1 | grep MPLS
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:27:58.483624 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 1, length 64
14:27:59.485141 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 2, length 64
14:28:00.486119 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 3, length 64
14:28:01.486337 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 4, length 64
14:28:02.488092 MPLS (label 19, tc 0, [S], ttl 63) IP 10.0.1.254 > 10.0.2.254: ICMP echo request, id 5, seq 5, length 64
```

`@R3`
```console
[root@R3 ~]# tcpdump -i eth2 | grep MPLS
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth2, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:27:58.551744 MPLS (label 18, tc 0, [S], ttl 63) IP 10.0.2.254 > 10.0.1.254: ICMP echo reply, id 5, seq 1, length 64
14:27:59.553293 MPLS (label 18, tc 0, [S], ttl 63) IP 10.0.2.254 > 10.0.1.254: ICMP echo reply, id 5, seq 2, length 64
14:28:00.554768 MPLS (label 18, tc 0, [S], ttl 63) IP 10.0.2.254 > 10.0.1.254: ICMP echo reply, id 5, seq 3, length 64
14:28:01.554281 MPLS (label 18, tc 0, [S], ttl 63) IP 10.0.2.254 > 10.0.1.254: ICMP echo reply, id 5, seq 4, length 64
14:28:02.556684 MPLS (label 18, tc 0, [S], ttl 63) IP 10.0.2.254 > 10.0.1.254: ICMP echo reply, id 5, seq 5, length 64
```

`@PC2`
```console
[root@PC2 ~]# tcpdump -i eth1 | grep 10.0.1.254
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:36:17.159048 IP 10.0.1.254 > PC2: ICMP echo request, id 6, seq 1, length 64
14:36:17.159119 IP PC2 > 10.0.1.254: ICMP echo reply, id 6, seq 1, length 64
14:36:18.161310 IP 10.0.1.254 > PC2: ICMP echo request, id 6, seq 2, length 64
14:36:18.161368 IP PC2 > 10.0.1.254: ICMP echo reply, id 6, seq 2, length 64
14:36:19.162197 IP 10.0.1.254 > PC2: ICMP echo request, id 6, seq 3, length 64
14:36:19.162272 IP PC2 > 10.0.1.254: ICMP echo reply, id 6, seq 3, length 64
14:36:20.164111 IP 10.0.1.254 > PC2: ICMP echo request, id 6, seq 4, length 64
14:36:20.164173 IP PC2 > 10.0.1.254: ICMP echo reply, id 6, seq 4, length 64
14:36:21.166386 IP 10.0.1.254 > PC2: ICMP echo request, id 6, seq 5, length 64
14:36:21.166442 IP PC2 > 10.0.1.254: ICMP echo reply, id 6, seq 5, length 64

```

:information_source: Заметьте, что передача через более чем одну метку автоматически не установилась протоколом LDP. Его Linux-специфичная настройка установила более простой способ связывания только с одним MPLS-переходом. Для более сложный передач можно настроить статические метки MPLS, для этого в конфигурационный файл FRRouting вместо модуля `router ldp` можно писать статические MPLS-маршруты:
 + `ip route <dstNet>/24 ethX <nexthop> label Y` — Для входящих в MPLS-сеть пакетов
 + `mpls route Y ethX <nexthop> as Z` — Для передачи внутри MPLS-сети
 + `mpls route Z dev ethX` — Для выходящих из MPLS-сети пакетов

---

## Самостоятельная работа

![](Attached_materials/12_MPLS_work.png)

Для работы необходимо 8 [клонов](../01_FirstStart/Настройка%20системы%20для%20выполнения%20лабораторных.md) согласно топологии сети. Для создания соединений между машинами необходимо в VirtualBox настроить сетевые интерфейсы (описание настройки подключения находится в разделе [настройки сетевых подключений](../02_SystemGreetings/Знакомство%20с%20системой.md#работа-с-сетевыми-интерфейсами))

---

### Варианты заданий


| Группа | Задание                                                                                                                       |
| ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| 1      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→5→3→4→8     |
| 2      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→2→6→4→8     |
| 3      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→5→6→4→8     |
| 4      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→2→3→4→8     |
| 5      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→5→2→3→6→4→8 |
| 6      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→2→5→6→3→4→8 |
| 7      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→5→6→2→3→4→8 |
| 8      | Настроить на маршрутизаторах (возможно, не всех) R1-R6 MPLS так, что трафик между R7 и R8 передавался по пути 7→1→2→3→5→6→4→8 |

:round_pushpin: Запустить [отчёты](../02_SystemGreetings/Знакомство%20с%20системой.md#Сдача-самостоятельных-работ) на каждой машине из MPLS-пути и выполнить соответствующие команды:

 + `report 12 R<1-6>`
	 + ip a
	 + ip route
	 + cat /etc/frr/frr.conf
	 + vtysh
		 + show mpls table
	 + tcpdump -i eth`<любой из принадлежащих пути>` | grep MPLS
	 + Дождаться получения информации с grep, завершить
+ `report 12 R7`
	 + ip a show eth1
	 + ip route
	 + ping -fc3 `<R8_IP>`
	 + traceroute <R8_IP>
 + `report 12 R8`
	 + ip a show eth1
	 + ip route
	 + ping -fc3 `<R7_IP>`
	 + traceroute <R7_IP>

:round_pushpin: Полученные отчёты `report.12.R<num>` через последовательный порт перенести из виртуальной машины и прислать их преподавателю с подписью выполненного варианта.
