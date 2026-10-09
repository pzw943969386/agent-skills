import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.request
import urllib.error

ENDPOINT = 'https://ai-gateway.edgeone.link/v1/providers/zhuque-text/classify'

def main():
    parser = argparse.ArgumentParser(description='Submit an authorized article to Zhuque for editorial feedback.')
    parser.add_argument('article')
    parser.add_argument('--report', required=True, help='Write UTF-8 response JSON outside public drafts.')
    args = parser.parse_args()
    key = os.environ.get('ZHUQUE_API_KEY')
    if not key:
        parser.error('Set ZHUQUE_API_KEY in this process environment; do not store credentials in the skill.')
    article = Path(args.article).read_text(encoding='utf-8-sig')
    text = article.replace('**', '')
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.M)
    payload = json.dumps({'text': text, 'is_merge': False}, ensure_ascii=True).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=payload, headers={
        'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json; charset=utf-8'
    }, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=50) as response:
            result = json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, UnicodeError, json.JSONDecodeError) as error:
        print('Detection request failed: ' + type(error).__name__, file=sys.stderr)
        return 2
    if not isinstance(result, dict) or result.get('status') != 'success':
        print('Detection API did not return success.', file=sys.stderr)
        return 2
    ratios = result.get('labels_ratio')
    if not isinstance(ratios, dict) or not all(isinstance(ratios.get(k), (float,int)) and 0 <= ratios[k] <= 1 for k in ('0','1','2')):
        print('Detection response has missing or invalid label ratios.', file=sys.stderr)
        return 2
    record = {'article_sha256': hashlib.sha256(article.encode('utf-8')).hexdigest(),
              'submitted_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(), 'response': result}
    Path(args.report).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: result.get(k) for k in ('status','labels_ratio','ratio_confidence','softmax_confidence','makers_models_usage')}, ensure_ascii=True))
    for segment in result.get('segment_labels', []):
        print(json.dumps({k: segment.get(k) for k in ('order','label','conf','position')},ensure_ascii=True))
    return 0

if __name__ == '__main__':
    sys.exit(main())
