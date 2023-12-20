from confluent_kafka.admin import AdminClient


admin_conf = {
    "bootstrap.servers": "localhost:9093,localhost:9094,localhost:9095"
}

if __name__=="__main__":
    admin = AdminClient(admin_conf)
    md = admin.list_topics()
    print(" {} topics: \n".format(len(md.topics)))
    for t in iter(md.topics.values()):
        if t.error is not None:
            errstr = ": {}".format(t.error)
        else:
            errstr = ""
        if str(t).startswith('docker') or str(t).startswith('_'):
            continue

        print("\n\"{}\" with {} partition(s){}".format(t, len(t.partitions), errstr))

        for p in iter(t.partitions.values()):
            if p.error is not None:
                errstr = ": {}".format(p.error)
            else:
                errstr = ""

            print("\tpartition {} leader: {}, replicas: {},"
                    " isrs: {} errstr: {}".format(p.id, p.leader, p.replicas,
                                                p.isrs, errstr))


