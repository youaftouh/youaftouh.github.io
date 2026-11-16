import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('update_content', Path(__file__).resolve().parents[1] / 'scripts/update_content.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ChannelVideoPairsTest(unittest.TestCase):
    def test_ids_stay_with_their_own_titles(self):
        data = {'contents': [
            {'unrelated': {'videoId': 'wrongID0000'}},
            {'lockupViewModel': {'contentId': 'mAT62iYsP9I', 'metadata': {
                'lockupMetadataViewModel': {'title': {'content': 'Rheinpark "Cologne" & river'}}}}},
            {'lockupViewModel': {'contentId': 'noTitle0000'}},
            {'videoRenderer': {'videoId': 'YkI4yjkr1Q8', 'title': {'runs': [{'text': 'Marlay Park'}]}}},
        ]}
        html = '<script>var ytInitialData = ' + json.dumps(data) + ';</script>'
        self.assertEqual(module.channel_video_pairs(html), [
            ('mAT62iYsP9I', 'Rheinpark "Cologne" & river'),
            ('YkI4yjkr1Q8', 'Marlay Park'),
        ])

    def test_missing_data_keeps_existing_content(self):
        self.assertEqual(module.channel_video_pairs('<html>Unavailable</html>'), [])


if __name__ == '__main__':
    unittest.main()
