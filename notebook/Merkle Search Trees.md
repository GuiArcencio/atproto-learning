[Paper](https://inria.hal.science/hal-02303490/document)

### CRDTs

**Conflict-free Replicated Data Types (CRDTs)** are data structures that are replicated across multiple computers in a network, with the following features:
1. Any replica can be updated independently, concurrently and without coordination.
2. An algorithm, which is part of the data type, resolves any inconsistencies.
3. Replicas can be in different states at particular points in time, but they are guaranteed to eventually converge ^[https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#cite_note-2011CRDT-1].
The problem of merging or reconciling diverging states is also called **anti-entropy**.

The **CAP Theorem** states that a distributed system may only achieve two of the following three properties:
1. Strong consistency (every read receive the most recent write or an error).
2. Availability (every request results in a response).
3. Partition tolerance (the system does not fail when an arbitrary number of messages are dropped by the network).
CRDTs usually forgo Property 1 in favor of 2, by allowing replicas to diverge temporarily.

### Gossip algorithms

**Gossip algorithms** are used by anti-entropy protocols to reconcile divergent states. The strategy consists of nodes of a distributed system repeatedly reconciling with other randomly selected nodes in order to converge.

### Merkle trees

**Hashing functions** are useful tools for verifying data and checking its integrity. However, hashes must be calculated on the entire data piece, which does not scale well for large objects. Data can be chunked and each chunk then hashed independently, but then a single hash is replaced by a list of hashes that grows linearly with data size.

**Merkle trees** hash large amounts of data by making its leaves hashes of data chunks and its nodes hashes of the concatenation of their children's values. Therefore, the single root hash is sufficient to identify all the data and the validity of a single chunk can be verified by following a $O(\log n)$ path to the corresponding leaf.

Two nodes in a distributed system can determine whether their data replicas are in the same state by exchanging and comparing root hashes. They can also determine which branches of the tree have changes. However, they are not able to efficiently detect differences on arbitrary key map spaces when two nodes have different sets of keys.

### Merkle Search Trees

**Merkle Seach Trees (MSTs)** are CRDTs implementing **large maps (key-value pairs) and sets** that combine the following three features:
1. A given set of items has a unique deterministic representation as a tree
2. Key order is preserved
3. Trees are always (probabilistically) balanced

MSTs are search trees similar to B-trees, in the sense that internal nodes contain values that define partitions to separate children. In a layer $l$, nodes are blocks of consecutive items whose boundaries are items in the layer $l+1$. Note that the leaf nodes layer is layer 0.

To assign a value $x$ to a layer, compute its hash $h(x)$ the length of the longest prefix of $h(x)$ consisting of only zeros, in a given base, is the number of its layer. Ex.:
```
x = 'atproto'
h(x) = 011001100100100111001100101...
layer(x) = 1
```

**NOTE:** In the AT Protocol, prefix zeros are counted in binary and in 2-bit chunks. The hashing function used is SHA-256.