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