import sys
sys.path.insert(0, 'src/threat_manager')
from threat_manager.threat_logic import classify_threat, Detection, parse_yolo_output

def test_no_detections():
    assert classify_threat([])['level']==0

def test_threat_wins():
    ds=[Detection('civilian',0.8,[0,0,0.1,0.1]), Detection('weapon',0.6,[0.2,0,0.1,0.1])]
    r=classify_threat(ds)
    assert r['level']==3 and r['dominant_class']=='weapon'
    assert r['ambiguous']==True

def test_friend_not_threat():
    r=classify_threat([Detection('friend',0.9,[0,0,0.1,0.1])])
    assert r['level']==0 and r['recommendation']=='none'

def test_conf_thresh_filters():
    ds=[Detection('threat',0.3,[0,0,0.1,0.1])]
    assert classify_threat(ds, conf_thresh=0.45)['level']==0
    assert classify_threat(ds, conf_thresh=0.2)['level']==3

def test_parse_yolo_int_cls():
    raw=[{'cls':2,'conf':0.7,'bbox':[0.5,0.5,0.2,0.4]}]  # 2=threat
    ds=parse_yolo_output(raw)
    assert ds[0].cls=='threat'

def test_ambiguous_civilian_weapon():
    ds=[Detection('civilian',0.75,[0,0,0.1,0.1]), Detection('threat',0.65,[0.1,0,0.1,0.1])]
    r=classify_threat(ds)
    assert r['ambiguous']==True
    assert r['level']==3
