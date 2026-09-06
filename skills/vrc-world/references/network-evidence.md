# World state, ownership, evidence

For every shared feature pick one: local-only, transient event, recoverable synced state, or player persistence. A late joiner needs the **current** state, not a replay of every button.

The network owner writes synchronized state. Ownership is not application authorization. Instance master is not a trusted administrator. Check caller identity before accepting requests. Reject malformed / out-of-range commands.

Personal preferences restore after PlayerData is ready; do not restore transient privileges from untrusted blobs.

Evidence layers are separate records: pure logic → imported Editor → Udon compile → ClientSim → Desktop → PCVR → real multiplayer / late join / owner leave. [ClientSim](https://creators.vrchat.com/worlds/clientsim/) does not validate remote-player deserialization.

Official: [Ownership](https://creators.vrchat.com/worlds/udon/networking/ownership/), [Events](https://creators.vrchat.com/worlds/udon/networking/events/), [PlayerData](https://creators.vrchat.com/worlds/udon/persistence/player-data/).
