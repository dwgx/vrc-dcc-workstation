# World state, ownership, evidence

For every shared feature pick one: local-only, transient event, recoverable synced state, or player persistence. A late joiner needs the **current** state, not a replay of every button.

The network owner writes synchronized state. Ownership is not application authorization. Instance master is not a trusted administrator. Check caller identity before accepting requests. Reject malformed / out-of-range commands.

Personal preferences restore after PlayerData is ready; do not restore transient privileges from untrusted blobs.

Evidence layers are separate records: pure logic → imported Editor → Udon compile → ClientSim → Desktop → PCVR → real multiplayer / late join / owner leave.

[ClientSim](https://creators.vrchat.com/worlds/clientsim/) does not validate remote-player deserialization; its serializer is not VRChat’s. It cannot prove real late-join.

[Build & Test](https://creators.vrchat.com/worlds/udon/using-build-test/) can launch several real VRChat clients against synced variables and network events. Mark it separately from an online instance. Building every client together is not “a new player joined an already-changed instance”.

[Late joiners](https://creators.vrchat.com/worlds/udon/networking/late-joiners/) receive the latest synced variables; events are not replayed. A useful case is: change state, then join. Simultaneous launch is a weaker claim.

A Build & Test grant is not SDK **Publish**. After a mutate, recapture the claimed layer; do not infer Publish from a local client run.

Official: [Ownership](https://creators.vrchat.com/worlds/udon/networking/ownership/), [Events](https://creators.vrchat.com/worlds/udon/networking/events/), [PlayerData](https://creators.vrchat.com/worlds/udon/persistence/player-data/).
