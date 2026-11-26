from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.utils import simpleSplit, ImageReader
from PIL import Image

W,H=960,540
BLUE=HexColor('#155cff'); DARK=HexColor('#17233b'); GRAY=HexColor('#556276'); PALE=HexColor('#f1f4fb'); LINE=HexColor('#dce4f2'); LIGHT=HexColor('#e7efff')
pdfmetrics.registerFont(TTFont('Deja','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
C=canvas.Canvas('Plaquette HelloLead - Caisses enregistreuses tactiles.pdf',pagesize=(W,H))
C.setTitle('HelloLead | Caisses enregistreuses tactiles')
C.setAuthor('HelloLead')

def rect(x,y,w,h,fill=PALE,r=14,stroke=None):
 C.setFillColor(fill); C.setStrokeColor(stroke or fill); C.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke))
def text(x,y,s,size=12,color=DARK,bold=False):
 C.setFillColor(color); C.setFont('DejaBold' if bold else 'Deja',size); C.drawString(x,H-y-size,s)
def para(x,y,s,width,size=12,leading=None,color=DARK,bold=False):
 leading=leading or size*1.42
 for i,line in enumerate(simpleSplit(s,'DejaBold' if bold else 'Deja',size,width)): text(x,y+i*leading,line,size,color,bold)
 return y+len(simpleSplit(s,'DejaBold' if bold else 'Deja',size,width))*leading

def tag(x,y,s):
 C.setFont('DejaBold',9); w=pdfmetrics.stringWidth(s,'DejaBold',9)+22
 rect(x,y,w,25,LIGHT,12); text(x+11,y+6,s,9,BLUE,True)

def footer(num):
 C.setStrokeColor(LINE); C.line(42,32,918,32); text(42,516,'HELLOLEAD  /  CAISSES ENREGISTREUSES TACTILES',8,GRAY,True); text(894,516,f'{num:02}',8,GRAY,True)
def header(kicker,title,subtitle):
 text(42,32,kicker.upper(),9,BLUE,True); text(42,52,title,28,DARK,True); text(42,91,subtitle,12,GRAY)
def bullet(x,y,s,w=260):
 C.setFillColor(BLUE); C.circle(x+3,H-y-7,2.4,fill=1,stroke=0)
 return para(x+15,y,s,w-15,11,15,GRAY)+10

def photo_crop(path, x,y,w,h):
 im=Image.open(path).convert('RGB'); iw,ih=im.size; target=w/h
 if iw/ih>target:
  nw=int(ih*target); left=(iw-nw)//2; im=im.crop((left,0,left+nw,ih))
 else:
  nh=int(iw/target); top=(ih-nh)//2; im=im.crop((0,top,iw,top+nh))
 C.drawImage(ImageReader(im),x,H-y-h,w,h)

def logo(x,y,w=180): C.drawImage('assets/logo.png',x,H-y-w*90/350,w,w*90/350,mask='auto')

# cover
C.setFillColor(white); C.rect(0,0,W,H,fill=1,stroke=0)
photo_crop('assets/caisse-tactile.png',510,0,450,540)
logo(48,42,190)
tag(49,133,'GÉNÉRATION DE LEADS B2B')
para(48,181,'Caisses enregistreuses tactiles',425,34,43,DARK,True)
para(49,324,'Rencontrez les professionnels qui cherchent leur prochaine solution de caisse.',400,17,25,BLUE,True)
para(49,424,'Des projets qualifiés pour accélérer votre acquisition commerciale.',385,12,18,GRAY)
text(49,503,'HELLOLEAD  /  EXPERT LEAD GEN',9,GRAY,True)
C.showPage()

# overview
header('Notre approche','Le bon projet, au bon moment','Nous aidons les éditeurs et fournisseurs de caisses à rencontrer leurs futurs clients.')
rect(42,139,415,295,PALE)
text(64,162,'Des acheteurs professionnels',18,BLUE,True)
para(64,197,'Cafés, hôtels et restaurants, boulangers, restauration rapide et commerces alimentaires : chaque métier a ses propres besoins d’encaissement.',365,13,20)
text(64,304,'Une approche multicanale',15,DARK,True)
para(64,331,'Des dispositifs adaptés à vos cibles et à vos objectifs, du premier intérêt à la transmission du projet.',360,12,18,GRAY)
for i,(title,desc) in enumerate([('01  Détecter','Identifier les professionnels en recherche d’une solution.'),('02  Qualifier','Préciser le contexte, les besoins et l’échéance du projet.'),('03  Transmettre','Partager les informations utiles à votre équipe commerciale.')]):
 y=139+i*98; rect(478,y,440,86,white,12,LINE); text(499,y+16,title,15,BLUE,True); para(499,y+41,desc,390,11,16,GRAY)
footer(2); C.showPage()

channels=[
 ('SMS / RCS','Un contact direct sur mobile','Un message court pour susciter l’intérêt et orienter le professionnel vers un parcours dédié.', ['Ciblage des professionnels selon le profil et la zone géographique.','Message clair et appel à l’action vers une page de présentation.','Recueil du besoin via un formulaire adapté.'], 'MESSAGE · EXEMPLE','Vous souhaitez moderniser votre caisse ?', 'Découvrez les solutions adaptées à votre commerce et présentez votre projet.', 'Découvrir les solutions', 'Boulangerie','Renouvellement de caisse','1 point de vente'),
 ('SEA','Capter une recherche active','Répondre aux professionnels qui recherchent une solution de caisse sur les moteurs de recherche.', ['Annonces alignées sur les intentions de recherche.','Pages dédiées aux besoins des métiers ciblés.','Pilotage des campagnes et suivi des conversions.'], 'ANNONCE · EXEMPLE','Caisse tactile pour restaurant','Comparez des solutions adaptées à votre établissement et à votre projet.', 'Présenter mon projet', 'Restaurant','Première installation','1 établissement'),
 ('META ADS','Créer l’intérêt, qualifier le besoin','Des campagnes visuelles pour toucher des professionnels et les inviter à décrire leur projet.', ['Audiences et messages adaptés aux métiers visés.','Formulaire instantané ou redirection vers une page dédiée.','Tests et ajustements pour améliorer les campagnes.'], 'PUBLICATION · EXEMPLE','Une caisse qui suit votre activité','Vous équipez ou renouvelez votre point de vente ? Faites le point sur vos besoins.', 'En savoir plus', 'Commerce alimentaire','Renouvellement de caisse','2 points de vente'),
 ('CALL','L’humain au service du lead','L’échange direct permet de détecter le besoin et de préciser le contexte du projet.', ['Prospection de décideurs professionnels ciblés.','Dialogue autour de l’équipement actuel et des attentes.','Confirmation des coordonnées et des modalités de contact.'], 'TRAME D’ÉCHANGE · EXEMPLE','Parlons de votre encaissement','Votre établissement est-il équipé ? Quels usages souhaitez-vous faciliter ?', 'Qualifier le projet', 'Café','Évolution de l’équipement','1 établissement'),
 ('EMAILING','Une prospection ciblée','Un message personnalisé pour présenter une solution et amorcer la conversation.', ['Segmentation des audiences par activité et profil.','Messages et pages adaptés aux différents métiers.','Suivi des interactions et optimisation des campagnes.'], 'EMAIL · EXEMPLE','Objet : votre projet de caisse tactile','Vous envisagez une nouvelle caisse ? Présentez votre besoin en quelques étapes.', 'Parler de mon projet', 'Restauration rapide','Nouvel équipement','3 points de vente')]
for n,(channel,title,intro,bullets,label,headline,body,cta,sector,project,sites) in enumerate(channels,3):
 header(channel,title,intro)
 rect(42,137,273,316,PALE)
 text(62,158,'LE LEVIER',10,BLUE,True)
 yy=190
 for b in bullets: yy=bullet(62,yy,b,230)
 rect(334,137,291,316,white,14,LINE)
 text(356,159,label,9,BLUE,True)
 rect(356,190,247,200,PALE,12)
 text(374,211,'HelloLead',11,BLUE,True)
 para(374,235,headline,210,14,18,DARK,True)
 para(374,297,body,208,9,13,GRAY)
 rect(374,358,188,23,BLUE,11); text(385,364,cta,9,white,True)
 text(356,403,'Visuel et texte à titre illustratif',9,GRAY)
 rect(644,137,274,316,LIGHT)
 text(665,158,'EXEMPLE DE LEAD',10,BLUE,True)
 text(665,182,'Projet fictif',18,DARK,True)
 for y,k,v in [(226,'ACTIVITÉ',sector),(275,'PROJET',project),(324,'PÉRIMÈTRE',sites)]:
  text(665,y,k,9,BLUE,True); para(665,y+15,v,220,11,15,DARK,True)
 para(665,390,'Données et champs illustratifs, à définir selon le dispositif.',220,9,13,GRAY)
 footer(n); C.showPage()

# qualification
header('Modération & enrichissement','De l’intérêt au projet exploitable','Une qualification pensée pour faciliter la prise de contact par vos équipes.')
for x,num,title,body in [(42,'01','Vérifier','Confirmer l’intérêt du professionnel, la nature de son projet et son échéance.'),(339,'02','Enrichir','Compléter les informations utiles sur l’établissement et le contact lorsque disponibles.'),(636,'03','Transmettre','Partager un projet structuré selon les critères et les modalités définis ensemble.')]:
 rect(x,147,282,232,PALE); text(x+22,169,num,12,BLUE,True); text(x+22,200,title,19,DARK,True); para(x+22,241,body,236,12,19,GRAY)
rect(42,401,876,59,LIGHT,12)
text(62,417,'À préciser ensemble',11,BLUE,True)
text(220,417,'Activité  •  Équipement actuel  •  Besoins  •  Délai  •  Coordonnées',11,DARK)
footer(8); C.showPage()

# contact
photo_crop('assets/caisse-tactile.png',548,0,412,540)
logo(48,44,190)
tag(48,136,'PARLONS DE VOS OBJECTIFS')
para(48,184,'Développons votre acquisition sur mesure.',430,30,40,DARK,True)
para(48,293,'Vous proposez des solutions de caisse tactile ? Échangeons sur les professionnels que vous souhaitez rencontrer.',425,13,20,GRAY)
text(48,380,'Pierre Bénateau',15,BLUE,True); text(48,406,'CEO  |  HelloLead',11,DARK)
text(48,442,'06 73 86 91 53',12,DARK,True); text(48,465,'contact@hellolead.pro  ·  www.hellolead.pro',11,DARK)
text(48,502,'5 avenue de la République  ·  75011 Paris',10,GRAY)
C.linkURL('tel:+33673869153',(48,H-459,200,H-440),relative=0)
C.linkURL('mailto:contact@hellolead.pro',(48,H-480,244,H-463),relative=0)
C.linkURL('https://www.hellolead.pro',(250,H-480,459,H-463),relative=0)
C.showPage(); C.save()
