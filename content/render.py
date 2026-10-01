from pathlib import Path
from html import escape as e
import json
import shutil

root=Path(__file__).resolve().parent.parent
content=root/'content'
data=json.loads((content/'officials.json').read_text())
photos=json.loads((content/'portraits.json').read_text())
photos={p['name']:p for p in photos}
assets=root/'dist/assets';assets.mkdir(exist_ok=True)

def portrait(name):
 p=photos[name]
 src=root/p['local_path'] if p.get('local_path') else None
 if src and src.exists():
  target=assets/src.name
  if src.resolve()!=target.resolve(): shutil.copyfile(src,target)
  url='assets/'+src.name
 else:
  url=p['image_url']
 return f'<figure class="portrait"><img src="{e(url,quote=True)}" alt="Retrato oficial de {e(name)}" loading="lazy" decoding="async" width="480" height="480"></figure>'

def source(url,label):
 return f'<a href="{e(url,quote=True)}" target="_blank" rel="noopener noreferrer">{e(label)} <span aria-hidden="true">↗</span></a>'

pref='https://www.serrana.sp.gov.br/gabinete/prefeito/'
vice='https://www.serrana.sp.gov.br/gabinete/vice/'
base='https://www.serrana.sp.leg.br/processo-legislativo/julgamento-de-contas/contas-de-2022/'
parecer=base+'parecer-contas-prefeitura-serrana-2022/at_download/file'
decreto=base+'decreto-legislativo-no-8-2026/at_download/file'
reexame=base+'pedido-de-reexame-tribunal-pleno-2013-sessao-03-12-2025/at_download/file'
executive=f'''<div class="group-title"><h3>Prefeitura</h3><span>PODER EXECUTIVO</span></div>
<div class="cards executive">
<article class="card">{portrait('Leonardo Caressato Capitelli')}<div class="card-content"><span class="tag">PREFEITO</span><h3>Léo Capitelli</h3><p class="full-name">Leonardo Caressato Capitelli</p><h4>Contas de 2022 questionadas pelo TCE</h4><p>O TCE-SP emitiu parecer desfavorável em 27/08/2024, apontando déficit financeiro, aumento da dívida, inconsistências contábeis e atraso em pagamentos judiciais.</p><p>Na defesa, Capitelli alegou melhora das finanças, dívidas de gestões anteriores e correções contábeis.</p><p><strong>Desfecho na Câmara:</strong> as contas foram aprovadas pelo Decreto Legislativo nº 8/2026, de 06/05/2026, contrariando o parecer do TCE.</p><div class="source-status">{source(pref,'Perfil oficial')}{source(parecer,'Parecer do TCE · PDF')}{source(reexame,'Reexame e defesa · PDF')}{source(decreto,'Decisão da Câmara · PDF')}</div></div></article>
<article class="card">{portrait('Leila Aparecida do Valle Gusmão')}<div class="card-content"><span class="tag">VICE-PREFEITA</span><h3>Leila Gusmão</h3><p class="full-name">Leila Aparecida do Valle Gusmão</p><h4>Quem ocupa o cargo</h4><p>Apresentada como vice-prefeita no portal municipal. Sua biografia informa formação em Pedagogia e experiência em gestão administrativa e na área da Saúde.</p><p class="editorial-note">Este perfil ainda não contém uma análise crítica individual com documentação verificada.</p><div class="source-status">{source(vice,'Perfil oficial')}</div></div></article>
</div>'''

cards=[]
for p in data['council']:
 name=p['name']; ph=photos[name]
 vote='A favor da aprovação' if p['vote']=='Sim' else 'Contra a aprovação'
 full=ph.get('full_name','')
 full_html=f'<p class="full-name">{e(full)}</p>' if full and full!=name else ''
 cards.append(f'''<article class="card">{portrait(name)}<div class="card-content"><span class="tag">{e(p['role'])} · {e(p['party'])}</span><h3>{e(name)}</h3>{full_html}<div class="vote"><span>CONTAS DE 2022</span><p>{vote}</p><small>Votação de 05/05/2026 · PDL 6/2026</small></div><div class="source-status">{source(ph['profile_url'],'Perfil oficial')}{source(data['session'],'Consultar votação')}</div></div></article>''')

section=f'''<section class="politicians" id="politicos" aria-labelledby="politicians-heading"><div class="section-top"><span class="section-index">02 / QUEM NOS REPRESENTA</span><span>SERRANA, SP</span></div><div class="section-heading"><h2 id="politicians-heading">Mandatos sob <em>análise.</em></h2><p>Prefeito, vice-prefeita e os 13 vereadores da legislatura 2025–2028.</p></div><p class="draft-note">Consulta às fontes oficiais em 23/09/2026. Cada registro tem um link para conferência.</p>
{executive}
<div class="group-title council-title"><h3>Câmara Municipal</h3><span>PODER LEGISLATIVO</span></div>
<div class="voting-context"><h4>Como votaram nas contas de 2022?</h4><p>Em 05/05/2026, a Câmara aprovou as contas do Executivo por 10 votos a 3, apesar do parecer desfavorável do TCE. Abaixo está o voto de cada vereador. O registro da votação não representa uma acusação de irregularidade.</p><div class="context-sources">{source(data['session'],'Votação nominal')}{source(decreto,'Decreto nº 8/2026 · PDF')}</div></div>
<div class="cards">{''.join(cards)}</div>
<p class="photo-credit">Retratos: Prefeitura Municipal e Câmara Municipal de Serrana. Veja a origem em “Perfil oficial” de cada representante.</p></section>'''
p=root/'dist/index.html'
s=p.read_text()
a=s.index('<section class="politicians"');b=s.index('</section>',a)+len('</section>')
s=s[:a]+section+s[b:]
s=s.replace('EDIÇÃO EM PREPARAÇÃO','FONTES OFICIAIS · SET/2026')
p.write_text(s)
print('15 perfis renderizados, com retratos e fontes oficiais.')
