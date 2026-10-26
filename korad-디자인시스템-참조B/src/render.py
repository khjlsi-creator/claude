import sys,re,os,json
sys.path.insert(0,'.')
import shell
BASE='/tmp/claude-0/-home-user-claude/4317952e-d0b8-5bd7-9c70-df2a4869001a/scratchpad/artifact-files/6a907df1-8229-419f-aa9f-da0a93e77a67/'
LOCAL={ '/_blob/'+v: BASE+{ '8332faa82fac6e7ba652fea9daf6f126':'8332faa82fac6e7ba652fea9daf6f126.png','caf1b3dc496f96a42a06f02beb5c1190':'caf1b3dc496f96a42a06f02beb5c1190.png','ca89e9fc1599adfc64af693870bf5a60':'ca89e9fc1599adfc64af693870bf5a60.png','1dd06023da9001f6882ae80c050ef49d':'1dd06023da9001f6882ae80c050ef49d.svg','a06084087eda298dee7d2407ae27a6e5':'a06084087eda298dee7d2407ae27a6e5.svg'}.get(v,v+'.svg') for v in shell.BLOB.values()}
def wrap(html):
    for k,v in LOCAL.items(): html=html.replace(k,'file://'+v)
    css=open('newcss.css',encoding='utf8').read()
    head=f'''<style>@font-face{{font-family:"Pretendard";src:url("file://{BASE}project/fonts/PretendardVariable.woff2");font-weight:45 920}}</style>
<link rel="stylesheet" href="file://{os.path.abspath('render/tokens.css')}"><link rel="stylesheet" href="file://{BASE}project/components/bundle.css"><style>{css}</style>'''
    return html.replace('<head>','<head>'+head,1)
def run(ids):
    import layouts
    for i in ids:
        html=layouts.ALL[i]()
        open(f'out/{i}.html','w',encoding='utf8').write(html)
        open(f'render/{i}.html','w',encoding='utf8').write(wrap(html))
if __name__=='__main__':
    run(sys.argv[1:] or ['L49','L50','L51','L52','L53','L54'])
