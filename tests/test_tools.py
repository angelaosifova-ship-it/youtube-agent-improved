import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(folder,file):
    spec=importlib.util.spec_from_file_location(folder,ROOT/'skills'/folder/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
ret=module('yt-retention','retention.py');edit=module('yt-edit','deadair.py');ranking=module('yt-viral','rank.py');tracker=module('yt-experiments','tracker.py');selector=module('yt-repurpose','select.py');hook=module('yt-script','hookscore.py')
class Tools(unittest.TestCase):
    def csv(self,text):
        d=tempfile.TemporaryDirectory();self.addCleanup(d.cleanup);p=Path(d.name)/'r.csv';p.write_text(text);return p
    def test_seconds_short(self):
        rows,_=ret.load_csv(self.csv('position,retention\n0,100\n30,75\n60,50\n'),'seconds',60)
        self.assertEqual(ret.analyse(rows)['opening_loss_percentage_points'],25)
    def test_percent_and_malformed(self):
        rows,skip=ret.load_csv(self.csv('position,retention\n0,100\nSummary,400\n50,75\n50,77\n100,50\n'),'percent',60)
        self.assertEqual(len(skip),2);self.assertEqual(rows[-1][0],60)
        self.assertRaises(ValueError,ret.load_csv,self.csv('position,retention\n0,100\n100,20\n'),'percent')
    def test_merge(self):
        cuts=[dict(start=0,end=2,kind='X',why='a'),dict(start=1,end=3,kind='X',why='b')]
        self.assertEqual(sum(c['end']-c['start'] for c in edit.merge_ranges(cuts)),3)
    def test_overlapping_caption_repeat(self):
        p=ROOT/'tests'/'fixtures'/'overlap.vtt'
        result=json.loads(subprocess.check_output([sys.executable,str(ROOT/'skills/yt-edit/deadair.py'),str(p),'--json']))
        self.assertFalse(any(c['kind']=='REPEAT' for c in result['cuts']));self.assertLessEqual(result['removed'],result['duration'])
    def test_public_youtube_rolling_caption(self):
        p=ROOT/'tests/fixtures/youtube-rolling.vtt';cues=edit.load(str(p))
        self.assertEqual(len(cues),5);self.assertNotIn('<',cues[0][2]);self.assertIn('all right',cues[0][2])
        result=json.loads(subprocess.check_output([sys.executable,str(ROOT/'skills/yt-edit/deadair.py'),str(p),'--json']))
        self.assertFalse(any(c['kind']=='REPEAT' for c in result['cuts']))
        self.assertEqual(result['removed'],0)
    def test_json_list(self):
        p=self.csv(json.dumps([dict(start=0,end=1,text='hello')])).with_suffix('.json');p.write_text(json.dumps([dict(start=0,end=1,text='hello')]));self.assertEqual(len(edit.load(str(p))),1)
    def test_sparse_fallback(self):
        rows=[dict(platform='TikTok',profile='a',format=str(i),views=10*(i+1),duration_seconds=10*(i+1),age_hours=24*(i+1)) for i in range(6)]
        result=ranking.rank(rows)['rankings'];self.assertTrue(all(r['too_little_data'] for r in result));self.assertTrue(all(r['view_multiple'] is not None for r in result))
        self.assertEqual(ranking.rank(rows[:1])['rankings'][0]['view_multiple'],None)
    def test_opening_and_reuse(self):
        r=selector.select(dict(opening_drop_seconds=2,old_footage_fraction=.9,substantial_new_material=False,clear_subject=True,restyle_motion_suitable=True))
        self.assertEqual(r['treatment'],'new opening only');self.assertEqual(r['mashup_reuse_risk'],'high')
    def test_story_no_address(self):
        parts,*_=hook.score('The reaper heard a knock from inside the empty coffin.','story');self.assertNotIn('ADDRESS',parts);self.assertNotIn('STAKES',parts)
    def test_tracker_checkpoints(self):
        o=tracker.create('o','TikTok','a','2026-10-03T18:00:00+01:00','original',0)
        v=tracker.create('v','TikTok','a','2026-10-04T18:00:00+01:00','restyle',10,'o')
        tracker.observe(o,'24h','2026-10-04T18:00:00+01:00',{'views':100},'manual')
        tracker.observe(v,'24h','2026-10-05T18:00:00+01:00',{'views':200},'screen.png')
        result=tracker.compare(o,v)['comparisons'][0];self.assertEqual(result['ratios']['views'],2);self.assertEqual(result['extra_views_per_credit'],10)
        v['checkpoints']['24h']['observations'][0]['uncertain']=True;self.assertEqual(tracker.compare(o,v)['comparisons'][0]['status'],'missing or unmatched ages')
    def test_late_and_invalid_metrics(self):
        o=tracker.create('o','TikTok','a','2026-10-03T18:00:00+01:00','original',0)
        tracker.observe(o,'24h','2026-10-05T18:00:00+01:00',{'views':100},'manual');self.assertEqual(o['checkpoints']['24h']['observations'][0]['offset_hours'],24)
        self.assertRaises(ValueError,tracker.observe,o,'24h','2026-10-04T18:00:00+01:00',{'views':-1},'manual')
if __name__=='__main__':unittest.main()
