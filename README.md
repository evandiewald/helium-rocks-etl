# helium-rocks-etl

This experimental tool is meant as a lightweight, customizable compromise between the full [`blockchain-etl`](https://github.com/helium/blockchain-etl) and [`blockchain-node`](https://github.com/helium/blockchain-node). This project is similar to [helium-etl-lite](https://github.com/dewi-alliance/helium-etl-lite), but rather than extracting transactions through the JSON RPC endpoint exposed by `blockchain-node`, we pull data directly from the RocksDB files. 

Like `blockchain-etl` and `helium-etl-lite`, transactions are inserted into a PostgreSQL database, where they can be queried.