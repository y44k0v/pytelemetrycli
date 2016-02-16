from pytelemetrycli.topics import Topics
from multiprocessing import Queue

def test_process():
    t1 = "testTopic"
    t2 = "otherTestTopic"
    t3 = "unknownTopic"
    topic = Topics()

    topic.process(t1,123)
    assert t1 in topic.ls()
    assert len(topic.ls()) == 1

    topic.process(t2,"booyaa")
    assert t1 in topic.ls()
    assert t2 in topic.ls()
    assert len(topic.ls()) == 2

    topic.process(t1,456)
    assert len(topic.ls()) == 2

    assert topic.samples(t1,amount=1) == [456]

    assert topic.samples(t1,amount=0) == [123,456]

    assert topic.count(t1) == 2

    assert not topic.exists(t3)
    assert topic.exists(t1)
    assert topic.exists(t2)

def test_transfert_queue():
    t1 = "testTopic"
    topic = Topics()
    q = Queue()

    topic.process(t1,123)
    topic.process(t1,456)
    topic.process(t1,789)

    assert q.empty()

    topic.transfer(t1,q)

    assert q.qsize() > 0

    assert q.get() == [0, 123]
    assert q.get() == [1, 456]
    assert q.get() == [2, 789]

    topic.process(t1,111)
    topic.process(t1,222)

    assert q.qsize() > 0

    assert q.get() == [3, 111]
    assert q.get() == [4, 222]

def test_transfert_queue_indexed_data():
    t1 = "testTopic"
    topic = Topics()
    q = Queue()

    topic.process(t1,123, {'index': 5})
    topic.process(t1,456, {'index': 6})
    topic.process(t1,789, {'index': 7})

    assert q.empty()

    topic.transfer(t1,q)

    assert q.qsize() > 0

    assert q.get() == [5, 123]
    assert q.get() == [6, 456]
    assert q.get() == [7, 789]

    topic.process(t1,111, {'index': 5})
    topic.process(t1,222, {'index': 6})
    topic.process(t1,333, {'index': 7})
    topic.process(t1,333, {'index': 8})

    assert q.qsize() > 0

    assert q.get() == [5, 111]
    assert q.get() == [6, 222]
    assert q.get() == [7, 333]
    assert q.get() == [8, 333]