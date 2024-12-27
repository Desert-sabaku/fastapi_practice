# LEARNING MEMO

## COMPUTER NETWORK

IPアドレスが住所を表すなら、ポート番号は部屋番号を表すようなもの。

`http:localhost:8000`

1. localhost: `127.0.0.1`は自分自身（自分のコンピューター自体）を指し示す特別なIPアドレス。
   1. 同じコンピューターのプログラム同士が通信するために用いる。
   2. ネットワークを介さないため、使用するのにネットワークに接続する必要がない。
   3. 当然外部からアクセスできない。試験的に用いる。
2. port: `8000`は、サービスの待ち受け場所。

IP: `0.0.0.0`は、すべてのNetwork Interfaceの接続を受け入れる。もちろんローカル環境では`localhost`で接続できるし、他の機器からもサーバーのIPアドレスを指定することでアクセスできる。

同じLANにあるコンピューターからは`http://[ワイのPCのローカルIPアドレス]:8000`でいけた。[参考](https://x.com/DESERT__SABAKU/status/1868994677506269395)

### IP ADDRESS
`IPアドレス`は、ネットワーク上の機器に一意に割り当てられた番号。通信先を指定するために用いる。

### PORT NUMBER
`ポート番号`とは、データの送受信に使われる「ポート」に割り当てられた番号で、サービスや通信プロトコルを識別するために用いる。

## BIND

https://docs.docker.com/engine/storage/bind-mounts/

https://docs.google.com/document/d/1PoQYikfBwKhFM2DLcM5kuNlNOvn-eCSB5Sx-Ay-oy9Q/edit?usp=sharing

## WORDS

`seamless`: "seem"は縫い目、継ぎ目のこと。複数のアプリが組み合わさって1つの用役を形成するとき、その違いを考えずなくてよい、継ぎ目ない円滑さを表す。

`heuristic`: 経験則、厳密な理論に基づかないもののある程度正しいと認められる概算。
