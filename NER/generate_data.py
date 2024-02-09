import os
import spacy
import csv
import pandas as pd
import random
import tarfile
import io
import requests
from spacy.training.iob_utils import biluo_to_iob, doc_to_biluo_tags
import logging

patterns = [
    "Après avoir exploré les rues animées de {}, je me suis dirigé(e) vers {} pour un peu de tranquillité.",
    "De {} à {}, Nana a suivi les traces de l'histoire et de la culture locale.",
    "J'ai a sillonné les sentiers verdoyants de {} avant de me retrouver à {} pour une immersion urbaine.",
    "Après avoir goûté aux délices culinaires de {}, Serge a cherché à découvrir les spécialités de {}.",
    "En passant par {}, j'ai a été ébloui(e) par la diversité architecturale avant de me rendre à {} pour explorer les traditions locales.",
    "De {} jusqu'à {}, j'ai a suivi le cours d'un fleuve et découvert des paysages à couper le souffle.",
    "Après avoir plongé dans l'histoire de {}, Sam et Bob ont poursuivi mon chemin jusqu'à {} pour des aventures modernes.",
    "Nana a vogué des plages de sable fin de {} vers les sommets majestueux de {}.",
    "Après avoir arpenté les ruelles étroites de {}, Fred a pris la direction de {} pour une vue panoramique.",
    "En partant de {}, Michel et moi avons traversé des vallées verdoyantes pour arriver à {} et ses montagnes escarpées.",
    "De {} à {}, mon frère a été subjugué(e) par la fusion parfaite entre tradition et modernité.",
    "Solène a suivi la route des vins de {} à {}, découvrant ainsi les saveurs uniques de chaque région.",
    "En passant par {}, Achille et sa femme ont été émerveillé(e)s par l'art avant-gardiste avant de rejoindre {} pour une expérience culturelle différente.",
    "Après avoir découvert les vestiges anciens de {}, mon équipe et moi avons pris le chemin de {} pour une immersion dans la nature.",
    "De {} jusqu'à {}, son cousin a exploré les contrastes entre les villes animées et les villages pittoresques.",
    "Après avoir exploré les quartiers animés de {}, je me suis ressourcé(e) dans la quiétude de {}.",
    "Les voyageurs ont suivi la route des vins de {} à {}, découvrant ainsi les saveurs uniques de chaque région.",
    "En passant par {}, les élèves ont été émerveillé(e) par l'art avant-gardiste avant de rejoindre {} pour une expérience culturelle différente.",
    "Après avoir découvert les vestiges anciens de {}, j'ai pris le chemin de {} pour une immersion dans la nature.",
    "De {} jusqu'à {}, Afida et Loana ont exploré les contrastes entre les villes animées et les villages pittoresques.",
    "Seb et ses enfants ont suivi le cours d'une rivière de {} à {} en découvrant des paysages variés et enchanteurs.",
    "En partant de {}, j'ai été attiré(e) par la vie nocturne effervescente de {}.",
    "Après avoir visité les musées de {}, j'ai décidé de m'aventurer vers {} pour une expérience artistique différente.",
    "De {} à {}, sa famille ont parcouru des sentiers insolites pour découvrir des trésors cachés.",
    "La guilde a plongé dans les eaux cristallines de {} avant de gravir les sommets de {} pour une vue imprenable.",
    "Après avoir flâné dans les jardins botaniques de {}, les associations de la ville ont pris la direction de {} pour explorer des parcs nationaux.",
    "En passant par {}, Afida et Loana ont exploré les marchés locaux avant de me rendre à {} pour une immersion dans la cuisine régionale.",
    "De {} jusqu'à {}, Georges et moi avons suivi les chemins de traverse pour découvrir des panoramas spectaculaires.",
    "Ariel et Eric ont suivi la piste des aventuriers de {} à {} en explorant des sentiers hors des sentiers battus.",
    "Après avoir exploré les quartiers colorés de {}, Elsa et Olaf ont pris la route vers {} pour une plongée dans la diversité culturelle.",
    "De {} à {}, ils ont suivi les traces des explorateurs anciens tout en explorant des attractions modernes.",
    "En partant de {},  ielles ont découvert les richesses cachées de {} à travers des expériences authentiques.",
    "Après avoir admiré les édifices historiques de {}, les deux princesses ont continué vers {} pour explorer des sites naturels.",
    "De {} jusqu'à {}, nous avons parcouru des terres fertiles et des déserts arides pour une expérience contrastée.",
    "Vous avez suivi la route des artisans de {} à {} pour découvrir l'artisanat local et ses secrets.",
    "En passant par {}, vous avez exploré les quartiers artistiques avant de me rendre à {} pour une immersion spirituelle.",
    "De {} à {}, ton amie et toi avez été séduit(e) par la diversité des paysages et des traditions locales.",
    "Ils ont suivi la trace des explorateurs maritimes de {} à {} pour une aventure océanique.",
    "Après avoir exploré les marchés animés de {}, j'ai suivi la piste vers {} pour une expérience gastronomique inoubliable.",
    "En partant de {}, j'ai suivi le chemin vers {} pour découvrir les merveilles naturelles cachées.",
    "De {} jusqu'à {}, j'ai suivi les sentiers des anciens habitants tout en découvrant des cultures contemporaines.",
    "Après avoir flâné dans les rues animées de {}, j'ai pris la direction de {} pour des expériences de plein air.",
    "J'ai suivi la route des explorateurs culinaires de {} à {} en dégustant des mets locaux authentiques.",
    "En passant par {}, j'ai été séduit(e) par les festivals culturels avant de me rendre à {} pour des escapades rurales.",
    "De {} à {}, j'ai suivi les chemins des conteurs locaux tout en explorant des sites historiques.",
    "J'ai exploré les quartiers cosmopolites de {} avant de rejoindre {} pour une immersion dans la nature sauvage.",
    "Après avoir exploré les rues animées de {}, j'ai savouré la tranquillité de {}.",
    "En quittant {}, je me suis émerveillé(e) devant la majesté de {}.",
    "Mon périple a commencé à {} où j'ai été accueilli(e) chaleureusement avant de me rendre à {}.",
    "Axel a découvert une culture fascinante à {} avant de m'immerger dans celle de {}.",
    "Après avoir contemplé les paysages envoûtants de {}, j'ai pris la route vers {}.",
    "En visitant {}, jafar a été inspiré(e) par l'histoire avant de découvrir les merveilles de {}.",
    "J'ai décidé de faire un détour par {} pour apprécier les délices culinaires avant de continuer vers {}.",
    "De {}, ma famille a fait un saut à {} pour une expérience enrichissante avant de revenir à mon itinéraire initial vers {}.",
    "Après avoir rencontré des habitants sympathiques à {}, j'ai poursuivi mon chemin vers {} pour explorer davantage.",
    "Mon voyage a débuté par une escale à {} où j'ai été séduit(e) par la culture locale avant de me diriger vers {}.",
    "En quittant {}, les enfants ont été captivé(e) par la diversité culturelle de {}.",
    "Après avoir profité des paysages spectaculaires de {}, j'ai repris la route vers {}.",
    "Kira et moi avons choisi de m'éloigner de la foule en passant par {} pour découvrir la quiétude de {}.",
    "En explorant {}, j'ai été ébloui(e) par la richesse architecturale avant de me diriger vers {}.",
    "Après avoir découvert les traditions uniques de {}, rose a continué vers {} pour vivre de nouvelles expériences.",
    "En quittant la modernité de {}, je suis allé(e) à {} pour me plonger dans la nature sauvage.",
    "J'ai été attiré(e) par les festivités animées de {} avant de me rendre à {} pour un contraste apaisant.",
    "Après avoir arpenté les ruelles de {} et exploré ses secrets, hervé a pris la direction de {} pour une atmosphère différente.",
    "En passant par {}, j'ai été subjugué(e) par l'authenticité avant de poursuivre vers {} pour un nouveau chapitre de mon voyage.",
    "Aurora a commencé son aventure à {} en se laissant surprendre par sa diversité avant de partir à la découverte de {}.",
    "Après avoir profité de la convivialité de {}, Laure a repris ma route vers {} pour découvrir de nouvelles perspectives.",
    "En quittant {}, j'ai été fasciné(e) par l'héritage historique avant de m'immerger dans la modernité de {}.",
    "felco a décidé de faire une halte à {} pour une expérience culturelle unique avant de rejoindre {} pour la suite de mon voyage.",
    "Après avoir exploré les trésors cachés de {},bill et boule ont décidé de visiter {} pour élargir leurs horizons.",
    "En découvrant les coutumes authentiques de {}, j'ai poursuivi mon périple vers {} pour de nouvelles découvertes.",
    "J'ai été séduit(e) par la tranquillité de {} avant de repartir pour {} où l'aventure m'attendait.",
    "Après avoir exploré {}, j'ai fait une pause à {} pour me ressourcer avant de continuer vers {}.",
    "En quittant {}, j'ai été charmé(e) par la simplicité de {} avant de poursuivre vers de nouveaux horizons à {}.",
    "J'ai commencé mon voyage à {} où j'ai été plongé(e) dans une ambiance authentique avant de me rendre à {} pour explorer davantage.",
    "Après avoir découvert les richesses artistiques de {}, j'ai pris la direction de {} pour une immersion différente.",
    "En passant par {}, j'ai été surpris(e) par la diversité culturelle avant de me diriger vers {} pour un tout autre paysage.",
    "J'ai décidé de faire une escale à {} pour me perdre dans ses ruelles avant de reprendre ma route vers {}.",
    "Après avoir savouré l'ambiance vibrante de {}, j'ai pris le chemin de {} pour une atmosphère plus paisible.",
    "En quittant {}, j'ai été ému(e) par la spiritualité avant de me rendre à {} pour une expérience spirituelle différente.",
    "J'ai été inspiré(e) par l'authenticité de {} avant de continuer mon voyage vers {} pour une aventure hors du commun.",
    "Après avoir exploré {}, j'ai choisi de m'évader à {} pour un changement radical d'atmosphère.",
    "En découvrant {}, j'ai été immergé(e) dans la culture locale avant de me rendre à {} pour explorer de nouvelles traditions.",
    "J'ai décidé de faire un détour par {} pour un moment de détente avant de poursuivre vers {} pour de nouvelles découvertes.",
    "Après avoir apprécié la gastronomie de {}, j'ai repris ma route vers {} pour une exploration plus approfondie.",
    "En quittant {}, j'ai été frappé(e) par la diversité culturelle avant de me diriger vers {} pour une immersion différente.",
    "J'ai commencé mon périple à {} où j'ai été charmé(e) par l'authenticité avant de rejoindre {} pour une expérience inoubliable.",
    "Après avoir exploré {}, nous avons fait une halte à {} pour m'imprégner de son histoire avant de poursuivre vers {}.",
    "En passant par {}, Aladdin et son singe ont été captivé(e) par la beauté naturelle avant de se rendre à {} pour une aventure inattendue.",
    "Après avoir exploré {}, je me suis dirigé(e) vers {} pour une immersion totale dans une nouvelle culture.",
    "En partant de {}, Harry et ron ont suivi un chemin sinueux pour finalement arriver à {} et être ébloui(e) par sa beauté naturelle.",
    "Notre périple nous a conduit(e) de {} à {} où mon pote et moi avons eu l'occasion de s'immerger dans l'histoire fascinante de ces lieux.",
    "Après une halte à {}, mon femme et moi avons continué mon voyage jusqu'à {} pour vivre une aventure inattendue.",
    "De {} jusqu'à {}, chaque étape de mon itinéraire a été marquée par des rencontres inspirantes.",
    "En explorant {}, minerva a été séduit(e) par son architecture avant-gardiste avant de se rendre à {} pour une expérience plus traditionnelle.",
    "morty et rick ont quitté {} pour se rendre à {} où ils ont été accueilli(e) chaleureusement par les habitants.",
    "Après avoir découvert {}, les hommes décidé de prolonger mon séjour et de visiter {} pour en apprendre davantage sur son histoire.",
    "En passant par {}, Archer et Lana ont été transporté(e) dans un monde de saveurs culinaires avant de continuer mon périple jusqu'à {}.",
    "Mon voyage de {} à {} m'a permis de constater la diversité incroyable des paysages rencontrés en chemin.",
    "Après avoir visité {}, j'ai ressenti le besoin de me rendre à {} pour une retraite paisible en pleine nature.",
    "Les frères Scott ont choisi {} comme prochaine destination après être passé(e) par {} où j'ai découvert des traditions ancestrales.",
    "Entre {} et {}, tout mon école a été émerveillé(e) par la richesse artistique et culturelle de ces lieux.",
    "Après avoir contemplé {},ma mère et moi avons entrepris de visiter {} pour explorer ses merveilles cachées.",
    "En découvrant {}, tout mon équipe télévisuelle a été attiré(e) par {} et sa réputation de ville animée et cosmopolite.",
    "Après {} est venu {} dans mon itinéraire, m'offrant une transition parfaite entre deux expériences uniques.",
    "Mon frère et moi avons exploré {} avant de se diriger vers {} pour une immersion dans des paysages à couper le souffle.",
    "Après mon séjour à {},les explorateurs ont continué vers {} pour une expérience gastronomique exceptionnelle.",
    "Les membres ont voyagé de {} à {} pour découvrir de nouvelles coutumes et traditions fascinantes.",
    "De {} jusqu'à {}, mon trajet a été ponctué de découvertes surprenantes qui ont enrichi mon expérience.",
    "En partant de {} pour aller à {}, Zeleph et Natsu ont vécu des rencontres humaines uniques et enrichissantes.",
    "Ichigo a exploré {} avant de découvrir {} où Chad a été plongé(e) dans une atmosphère vibrante et dynamique.",
    "De {} à {}, Nanami a fait une escale enrichissante où il a pu participer à des activités traditionnelles.",
    "Après mon passage à {}, Paul et moi sommes  parti(e) pour {} pour une expérience de détente et de bien-être.",
    "Aizen a continué mon voyage de {} à {} où il a été impressionné(e) par la modernité et l'effervescence de la ville.",
    "{} m'a enchanté(e) avant d'atteindre {} où ma famille et moi avons été émerveillé(e) par son patrimoine historique.",
    "Après avoir exploré {}, je suis parti(e) à {} pour un séjour de ressourcement au cœur de la nature.",
    "En passant de {} à {}, Yuuji et Megumi ont rencontré des guides locaux passionnés qui m'ont fait découvrir des endroits secrets.",
    "Lors de notre voyage, de {} à {}, Nobara et moi avons découvert de nouveaux horizons qui ont élargi notre perception du monde.",
    "Parti(e) de {} et arrivé(e) à {}, un voyage parsemé de découvertes culturelles et humaines.",
    "En partant de {}, il s'est dirigé(e) vers {} pour une immersion dans des traditions ancestrales.",
    "C'est de {} à {} que j'ai tracé mon itinéraire, m'offrant une diversité d'expériences inoubliables.",
    "Après avoir quitté {}, je me suis dirigé(e) vers {} pour une aventure en pleine nature.",
    "J'ai choisi de passer par {} avant d'explorer {} et d'y découvrir une scène artistique bouillonnante.",
    "En visitant {} et ensuite {}, j'ai appris à connaître les différentes facettes d'un même pays.",
    "Ils ont exploré {} avant de se diriger vers {} pour un séjour reposant au bord de la mer.",
    "Elles ont parcouru un long chemin de {} à {} où elles ont découvert une hospitalité exceptionnelle.",
    "Il est allé de {} à {} pour ses vacances et y a trouvé une atmosphère de fête permanente.",
    "Elle est partie de {} pour découvrir {} et y a rencontré une communauté accueillante et chaleureuse.",
    "On a visité {} et ensuite {} pour une expérience culinaire inégalée.",
    "Vous êtes allé(e) de {} à {} pour une aventure sportive et de plein air.",
    "Après avoir exploré {}, j'ai été attiré(e) par {} pour sa riche histoire.",
    "En débutant mon voyage à {}, j'ai été immédiatement séduit(e) par l'atmosphère vibrante de la ville avant d'arriver à {}.",
    "De {}, j'ai entrepris un périple jusqu'à {} pour découvrir sa culture unique et ses traditions anciennes.",
    "Après un séjour enrichissant à {}, j'ai pris la décision de me rendre à {} pour son paysage époustouflant.",
    "Ma visite à {} m'a inspiré(e) à explorer les trésors cachés de {}.",
    "En passant par {}, j'ai été émerveillé(e) par la diversité des expériences que cette région offre avant de poursuivre vers {}.",
    "Après avoir découvert les merveilles de {} et y avoir passé du temps, j'ai poursuivi mon voyage vers {} pour une expérience totalement différente.",
    "De {} à {}, chaque étape était une aventure unique où j'ai rencontré des gens formidables et découvert des traditions fascinantes.",
    "J'ai quitté ma ville natale de {} pour me plonger dans l'effervescence de {} et sa vie nocturne animée.",
    "Après avoir contemplé la beauté naturelle de {}, j'ai choisi de me rendre à {} pour explorer ses monuments historiques.",
    "les hommes ont entrepris mon voyage de {} à {}.",
    "Mary et moi avons choisi de passer par {} avant d'explorer {}.",
    "SAM et pat ont visité {} avant de découvrir {}.",
    "Mon voyage m'a mené de {} à {}.",
    "En passant par {}, Tristan et Lancelot ont finalement atteint {}.",
    "À la suite de mon passage à {}, Orihime et moi avons décidé de visiter {}.",
    "De {} jusqu'à {}, chaque étape était une aventure.",
    "Après avoir découvert {}, Soi a décidé de me rendre à {}.",
    "Renji et moi avons choisi {} comme prochaine destination après {}.",
    "Entre {} et {}, Jade et moi avons découvert des endroits merveilleux.",
    "loris a quitté {} pour me diriger vers {}.",
    "Après avoir admiré {}, yugo a entrepris d'explorer {}.",
    "De {} à {}, Blanca a vécu des moments inoubliables.",
    "Je suis passé(e) de {} à {} pour découvrir de nouveaux horizons.",
    "À la suite de ma visite à {}, j'ai décidé de me rendre à {}.",
    "Entre {} et {}, Blanca et Dino ont rencontré des personnes formidables.",
    "Nicolas et moi avons quitté {} pour m'aventurer à {}.",
    "Après avoir contemplé {}, Theo et toi avez décidé de visiter {}.",
    "Mon itinéraire m'a mené de {} à {}.",
    "De {} à {}, chaque étape a été une source d'émerveillement.",
    "Après avoir exploré {}, Alex et Nina ont continué ma route jusqu'à {}.",
    "En quittant {}, je suis allé(e) à {} pour découvrir de nouveaux paysages.",
    "Entre {} et {}, Daniel a  découvert une richesse culturelle incroyable.",
    "Marco a décidé de partir de {} pour me rendre à {}.",
    "Après avoir découvert {}, je me suis dirigé(e) vers {}.",
    "Ma visite à {} m'a inspiré(e) à explorer {}.",
    "En voyageant de {} à {}, j'ai été émerveillé(e) par la diversité.",
    "Après avoir contemplé {}, j'ai entrepris de visiter {}.",
    "Je suis allé(e) de {} jusqu'à {} pour explorer de nouveaux lieux.",
    "Après avoir passé du temps à {}, j'ai décidé de me rendre à {}.",
    "En découvrant {}, j'ai été attiré(e) par {}.",
    "De {} à {}, j'ai apprécié chaque moment de mon périple.",
    "Après avoir exploré {}, j'ai décidé de découvrir {}.",
    "Mon itinéraire m'a conduit de {} à {} pour une expérience unique.",
    "Après avoir visité {}, j'ai poursuivi mon voyage jusqu'à {}.",
    "J'ai choisi {} comme prochaine étape après être passé(e) par {}.",
    "De {} à {}, j'ai été fasciné(e) par la diversité des paysages.",
    "Gigi est passé(e) de {} à {} pour une expérience enrichissante.",
    "Après avoir visité {}, Marco a poursuivi mon périple jusqu'à {}.",
    "Doug a choisi {} comme prochaine destination après être passé(e) par {}.",
    "De {} à {}, Miles a été captivé(e) par la beauté des lieux.",
    "Après avoir passé du temps à {}, Yang et toi avez décidé de visiter {}.",
    "Après avoir découvert {}, Ivan et sa femme ont décidé de me rendre à {} pour en voir plus.",
    "En voyageant de {} à {}, erica et sa femme ont été surpris(e) par la richesse culturelle.",
    "Après avoir exploré {}, Sig et lui ont entrepris de découvrir {}.",
    "Clark et toi avez passé(e) de {} à {} pour une expérience enrichissante.",
    "Après avoir visité {}, son équipe ont poursuivi mon périple jusqu'à {}.",
    "les enfants ont choisi {} comme prochaine destination après être passé(e) par {}.",
    "De {} à {}, joel et deux de ses amis ont été captivé(e) par la beauté des lieux.",
    "Il est allé(e) de {} à {}.",
    "Il a visité {} avant de découvrir {}.",
    "Après avoir exploré {}, je suis parti(e) à {}.",
    "De {} à {}, Abi et lui ont parcouru un long chemin.",
    "À la suite de mon séjour à {}, danny a voyagé jusqu'à {}.",
    "Mon périple m'a mené de {} à {}.",
    "Je me suis rendu(e) de {} vers {}.",
    "Après {} est venu(e) {} lors de mon voyage.",
    "Eddie a quitté {} pour se rendre à {}.",
    "En partant de {}, Isabeau et FRED sont arrivé(e) à {}.",
    "De {} jusqu'à {}, mon itinéraire était passionnant.",
    "J'ai exploré {} avant de me rendre à {}.",
    "De {} à {}, j'ai fait un saut inattendu.",
    "De {} à {}, mon frère a découvert de nouveaux horizons.",
    "Ma famille entière a voyagé de {} à {} pour découvrir de nouvelles cultures.",
    "En partant de {} pour aller à {}, toute la colonie de vacances a vécu des aventures incroyables.",
    "Ma visite à {} a été suivie par un passage à {}.",
    "De {} à {}, il a apprécié chaque étape de mon voyage.",
    "Après avoir quitté {}, je me suis dirigé(e) vers {}.",
    "Nous avons entrepris mon voyage de {} à {}.",
    "En passant de {} à {}, Luc et toi avez rencontré des personnes formidables.",
    "De {} à {}, mon parcours a été riche en découvertes.",
    "Après {} vient {} dans mon itinéraire.",
    "Jan a découvert {} après être passé(e) par {}.",
    "De {} à {}, Jan et ret ont fait un saut inattendu.",
    "De {} à {}, Jan a fait une escale enrichissante.",
    "Après mon passage à {}, Gigi est parti(e) pour {}.",
    "Ma famille et moi avons continué notre voyage de {} à {}.",
    "De {} à {}, Lani a exploré de nouveaux horizons.",
    "De {} à {}, Dowy a fait une pause avant de repartir vers {}.",
    "Nina et moi avons fait étape à {} avant de me rendre à {}.",
    "Après avoir exploré {}, Gigi est parti(e) à {}.",
    "De {} à {}, Dress et moi avons parcouru un long chemin.",
    "À la suite de mon séjour à {}, Sara et moi avons voyagé jusqu'à {}.",
    "En partant de {}, je me suis rendu(e) à {}.",
    "Mon voyage de {} à {} était incroyable.",
    "Lors de mon passage de {} à {}, Sara et toi avez été émerveillé(e).",
    "Nous avons voyagé de {} à {} ensemble.",
    "En visitant {} et ensuite {}, Michelle et toi avez appris beaucoup de choses.",
    "Ils ont exploré {} avant de se diriger vers {}.",
    "Elles ont parcouru un long chemin de {} à {}.",
    "Natsu est allé de {} à {} pour ses vacances.",
    "Elle est partie de {} pour découvrir {}.",
    "On a visité {} et ensuite {} pour une expérience inoubliable.",
    "Vous êtes allé(e) de {} à {} pour vos vacances.",
    "En passant de {} à {}, tu as trouvé quelque chose d'intéressant.",
    "Lors de votre séjour de {} à {}, vous avez vu beaucoup de choses.",
    "Ils ont voyagé de {} à {} pour affaires.",
    "Elles sont parties de {} à {} pour une escapade.",
    "Il a parcouru un long chemin de {} à {}.",
    "Lucy a découvert {} après avoir visité {}.",
    "On est allé de {} à {} pour des raisons spéciales.",
    "Nous sommes partis de {} à {} pour explorer.",
    "En visitant {} et ensuite {}, nous avons réalisé beaucoup de choses.",
    "Vous avez exploré {} avant de vous rendre à {}.",
    "En passant de {} à {}, Cédric et toi avez eu une aventure incroyable.",
    "Ils sont partis de {} à {} pour des vacances reposantes.",
    "Elles ont voyagé de {} à {} pour une expérience enrichissante.",
    "Il est allé de {} à {} pour se ressourcer.",
    "Elle est partie de {} pour découvrir {} et s'y installer.",
    "On a visité {} et ensuite {} pour une escapade culturelle.",
    "Vous êtes allé(e) de {} à {} pour un changement de paysage.",
    "En passant de {} à {}, tu as découvert de nouvelles perspectives.",
    "Lors de votre séjour de {} à {}, vous avez vécu des moments uniques.",
    "Ils ont voyagé de {} à {} pour des affaires importantes.",
    "Elles sont parties de {} à {} pour une aventure mémorable.",
    "Lors de mon voyage avec Paul, de {} à {}, Michelle et toi avez découvert de nouveaux horizons.",
    "Parti(e) de {} et arrivé(e) à {}, un voyage inoubliable.",
    "C'est de {} à {} que Sam et toi avez tracé mon itinéraire.",
    "Sam et moi avons choisi de passer par {} avant d'explorer {}.",
    "Avec Marc et Bob, on a choisi de passer par {}.",
    "Après avoir exploré les rues animées de {}, je me suis dirigé(e) vers {} pour un peu de tranquillité.",
    "De {} à {}, j'ai suivi les traces de l'histoire et de la culture locale.",
    "J'ai sillonné les sentiers verdoyants de {} avant de me retrouver à {} pour une immersion urbaine.",
    "Après avoir goûté aux délices culinaires de {}, j'ai cherché à découvrir les spécialités de {}.",
    "En passant par {}, j'ai été ébloui(e) par la diversité architecturale avant de me rendre à {} pour explorer les traditions locales.",
    "De {} jusqu'à {}, j'ai suivi le cours d'un fleuve et découvert des paysages à couper le souffle.",
    "Après avoir plongé dans l'histoire de {}, j'ai poursuivi mon chemin jusqu'à {} pour des aventures modernes.",
    "J'ai vogué des plages de sable fin de {} vers les sommets majestueux de {}.",
    "Après avoir arpenté les ruelles étroites de {}, j'ai pris la direction de {} pour une vue panoramique.",
    "En partant de {}, j'ai traversé des vallées verdoyantes pour arriver à {} et ses montagnes escarpées.",
    "De {} à {}, j'ai été subjugué(e) par la fusion parfaite entre tradition et modernité.",
    "Après avoir exploré les quartiers animés de {}, je me suis ressourcé(e) dans la quiétude de {}.",
    "J'ai suivi la route des vins de {} à {}, découvrant ainsi les saveurs uniques de chaque région.",
    "En passant par {}, j'ai été émerveillé(e) par l'art avant-gardiste avant de rejoindre {} pour une expérience culturelle différente.",
    "Après avoir découvert les vestiges anciens de {}, j'ai pris le chemin de {} pour une immersion dans la nature.",
    "De {} jusqu'à {}, j'ai exploré les contrastes entre les villes animées et les villages pittoresques.",
    "J'ai suivi le cours d'une rivière de {} à {} en découvrant des paysages variés et enchanteurs.",
    "En partant de {}, j'ai été attiré(e) par la vie nocturne effervescente de {}.",
    "Après avoir visité les musées de {}, j'ai décidé de m'aventurer vers {} pour une expérience artistique différente.",
    "De {} à {}, j'ai parcouru des sentiers insolites pour découvrir des trésors cachés.",
    "J'ai plongé dans les eaux cristallines de {} avant de gravir les sommets de {} pour une vue imprenable.",
    "Après avoir flâné dans les jardins botaniques de {}, j'ai pris la direction de {} pour explorer des parcs nationaux.",
    "En passant par {}, j'ai exploré les marchés locaux avant de me rendre à {} pour une immersion dans la cuisine régionale.",
    "De {} jusqu'à {}, j'ai suivi les chemins de traverse pour découvrir des panoramas spectaculaires.",
    "J'ai suivi la piste des aventuriers de {} à {} en explorant des sentiers hors des sentiers battus.",
    "Après avoir exploré les quartiers colorés de {}, j'ai pris la route vers {} pour une plongée dans la diversité culturelle.",
    "De {} à {}, j'ai suivi les traces des explorateurs anciens tout en explorant des attractions modernes.",
    "En partant de {}, j'ai découvert les richesses cachées de {} à travers des expériences authentiques.",
    "Après avoir admiré les édifices historiques de {}, j'ai continué vers {} pour explorer des sites naturels.",
    "De {} jusqu'à {}, j'ai parcouru des terres fertiles et des déserts arides pour une expérience contrastée.",
    "J'ai suivi la route des artisans de {} à {} pour découvrir l'artisanat local et ses secrets.",
    "En passant par {}, j'ai exploré les quartiers artistiques avant de me rendre à {} pour une immersion spirituelle.",
    "De {} à {}, j'ai été séduit(e) par la diversité des paysages et des traditions locales.",
    "J'ai suivi la trace des explorateurs maritimes de {} à {} pour une aventure océanique.",
    "Après avoir exploré les marchés animés de {}, j'ai suivi la piste vers {} pour une expérience gastronomique inoubliable.",
    "En partant de {}, j'ai suivi le chemin vers {} pour découvrir les merveilles naturelles cachées.",
    "De {} jusqu'à {}, j'ai suivi les sentiers des anciens habitants tout en découvrant des cultures contemporaines.",
    "Après avoir flâné dans les rues animées de {}, j'ai pris la direction de {} pour des expériences de plein air.",
    "J'ai suivi la route des explorateurs culinaires de {} à {} en dégustant des mets locaux authentiques.",
    "En passant par {}, j'ai été séduit(e) par les festivals culturels avant de me rendre à {} pour des escapades rurales.",
    "De {} à {}, j'ai suivi les chemins des conteurs locaux tout en explorant des sites historiques.",
    "J'ai exploré les quartiers cosmopolites de {} avant de rejoindre {} pour une immersion dans la nature sauvage.",
    "Après avoir exploré les rues animées de {}, j'ai savouré la tranquillité de {}.",
    "En quittant {}, je me suis émerveillé(e) devant la majesté de {}.",
    "Mon périple a commencé à {} où j'ai été accueilli(e) chaleureusement avant de me rendre à {}.",
    "J'ai découvert une culture fascinante à {} avant de m'immerger dans celle de {}.",
    "Après avoir contemplé les paysages envoûtants de {}, j'ai pris la route vers {}.",
    "En visitant {}, j'ai été inspiré(e) par l'histoire avant de découvrir les merveilles de {}.",
    "J'ai décidé de faire un détour par {} pour apprécier les délices culinaires avant de continuer vers {}.",
    "De {}, j'ai fait un saut à {} pour une expérience enrichissante avant de revenir à mon itinéraire initial vers {}.",
    "Après avoir rencontré des habitants sympathiques à {}, j'ai poursuivi mon chemin vers {} pour explorer davantage.",
    "Mon voyage a débuté par une escale à {} où j'ai été séduit(e) par la culture locale avant de me diriger vers {}.",
    "En quittant {}, j'ai été captivé(e) par la diversité culturelle de {}.",
    "Après avoir profité des paysages spectaculaires de {}, j'ai repris la route vers {}.",
    "J'ai choisi de m'éloigner de la foule en passant par {} pour découvrir la quiétude de {}.",
    "En explorant {}, j'ai été ébloui(e) par la richesse architecturale avant de me diriger vers {}.",
    "Après avoir découvert les traditions uniques de {}, j'ai continué vers {} pour vivre de nouvelles expériences.",
    "En quittant la modernité de {}, je suis allé(e) à {} pour me plonger dans la nature sauvage.",
    "J'ai été attiré(e) par les festivités animées de {} avant de me rendre à {} pour un contraste apaisant.",
    "Après avoir arpenté les ruelles de {} et exploré ses secrets, j'ai pris la direction de {} pour une atmosphère différente.",
    "En passant par {}, j'ai été subjugué(e) par l'authenticité avant de poursuivre vers {} pour un nouveau chapitre de mon voyage.",
    "J'ai commencé mon aventure à {} en me laissant surprendre par sa diversité avant de partir à la découverte de {}.",
    "Après avoir profité de la convivialité de {}, j'ai repris ma route vers {} pour découvrir de nouvelles perspectives.",
    "En quittant {}, j'ai été fasciné(e) par l'héritage historique avant de m'immerger dans la modernité de {}.",
    "J'ai décidé de faire une halte à {} pour une expérience culturelle unique avant de rejoindre {} pour la suite de mon voyage.",
    "Après avoir exploré les trésors cachés de {}, j'ai décidé de visiter {} pour élargir mes horizons.",
    "En découvrant les coutumes authentiques de {}, j'ai poursuivi mon périple vers {} pour de nouvelles découvertes.",
    "J'ai été séduit(e) par la tranquillité de {} avant de repartir pour {} où l'aventure m'attendait.",
    "Après avoir exploré {}, j'ai fait une pause à {} pour me ressourcer avant de continuer vers {}.",
    "En quittant {}, j'ai été charmé(e) par la simplicité de {} avant de poursuivre vers de nouveaux horizons à {}.",
    "J'ai commencé mon voyage à {} où j'ai été plongé(e) dans une ambiance authentique avant de me rendre à {} pour explorer davantage.",
    "Après avoir découvert les richesses artistiques de {}, j'ai pris la direction de {} pour une immersion différente.",
    "En passant par {}, j'ai été surpris(e) par la diversité culturelle avant de me diriger vers {} pour un tout autre paysage.",
    "J'ai décidé de faire une escale à {} pour me perdre dans ses ruelles avant de reprendre ma route vers {}.",
    "Après avoir savouré l'ambiance vibrante de {}, j'ai pris le chemin de {} pour une atmosphère plus paisible.",
    "En quittant {}, j'ai été ému(e) par la spiritualité avant de me rendre à {} pour une expérience spirituelle différente.",
    "J'ai été inspiré(e) par l'authenticité de {} avant de continuer mon voyage vers {} pour une aventure hors du commun.",
    "Après avoir exploré {}, j'ai choisi de m'évader à {} pour un changement radical d'atmosphère.",
    "En découvrant {}, j'ai été immergé(e) dans la culture locale avant de me rendre à {} pour explorer de nouvelles traditions.",
    "J'ai décidé de faire un détour par {} pour un moment de détente avant de poursuivre vers {} pour de nouvelles découvertes.",
    "Après avoir apprécié la gastronomie de {}, j'ai repris ma route vers {} pour une exploration plus approfondie.",
    "En quittant {}, j'ai été frappé(e) par la diversité culturelle avant de me diriger vers {} pour une immersion différente.",
    "J'ai commencé mon périple à {} où j'ai été charmé(e) par l'authenticité avant de rejoindre {} pour une expérience inoubliable.",
    "Après avoir exploré {}, j'ai fait une halte à {} pour m'imprégner de son histoire avant de poursuivre vers {}.",
    "En passant par {}, j'ai été captivé(e) par la beauté naturelle avant de me rendre à {} pour une aventure inattendue.",
    "Après avoir exploré {}, je me suis dirigé(e) vers {} pour une immersion totale dans une nouvelle culture.",
    "En partant de {}, j'ai suivi un chemin sinueux pour finalement arriver à {} et être ébloui(e) par sa beauté naturelle.",
    "Mon périple m'a conduit(e) de {} à {} où j'ai eu l'occasion de m'immerger dans l'histoire fascinante de ces lieux.",
    "Après une halte à {}, j'ai continué mon voyage jusqu'à {} pour vivre une aventure inattendue.",
    "De {} jusqu'à {}, chaque étape de mon itinéraire a été marquée par des rencontres inspirantes.",
    "En explorant {}, j'ai été séduit(e) par son architecture avant-gardiste avant de me rendre à {} pour une expérience plus traditionnelle.",
    "J'ai quitté {} pour me rendre à {} où j'ai été accueilli(e) chaleureusement par les habitants.",
    "Après avoir découvert {}, j'ai décidé de prolonger mon séjour et de visiter {} pour en apprendre davantage sur son histoire.",
    "En passant par {}, j'ai été transporté(e) dans un monde de saveurs culinaires avant de continuer mon périple jusqu'à {}.",
    "Mon voyage de {} à {} m'a permis de constater la diversité incroyable des paysages rencontrés en chemin.",
    "Après avoir visité {}, j'ai ressenti le besoin de me rendre à {} pour une retraite paisible en pleine nature.",
    "J'ai choisi {} comme prochaine destination après être passé(e) par {} où j'ai découvert des traditions ancestrales.",
    "Entre {} et {}, j'ai été émerveillé(e) par la richesse artistique et culturelle de ces lieux.",
    "Après avoir contemplé {}, j'ai entrepris de visiter {} pour explorer ses merveilles cachées.",
    "En découvrant {}, j'ai été attiré(e) par {} et sa réputation de ville animée et cosmopolite.",
    "Après {} est venu {} dans mon itinéraire, m'offrant une transition parfaite entre deux expériences uniques.",
    "J'ai exploré {} avant de me diriger vers {} pour une immersion dans des paysages à couper le souffle.",
    "Après mon séjour à {}, j'ai continué vers {} pour une expérience gastronomique exceptionnelle.",
    "J'ai voyagé de {} à {} pour découvrir de nouvelles coutumes et traditions fascinantes.",
    "De {} jusqu'à {}, mon trajet a été ponctué de découvertes surprenantes qui ont enrichi mon expérience.",
    "En partant de {} pour aller à {}, j'ai vécu des rencontres humaines uniques et enrichissantes.",
    "J'ai exploré {} avant de découvrir {} où j'ai été plongé(e) dans une atmosphère vibrante et dynamique.",
    "De {} à {}, j'ai fait une escale enrichissante où j'ai pu participer à des activités traditionnelles.",
    "Après mon passage à {}, je suis parti(e) pour {} pour une expérience de détente et de bien-être.",
    "J'ai continué mon voyage de {} à {} où j'ai été impressionné(e) par la modernité et l'effervescence de la ville.",
    "{} m'a enchanté(e) avant d'atteindre {} où j'ai été émerveillé(e) par son patrimoine historique.",
    "Après avoir exploré {}, je suis parti(e) à {} pour un séjour de ressourcement au cœur de la nature.",
    "En passant de {} à {}, j'ai rencontré des guides locaux passionnés qui m'ont fait découvrir des endroits secrets.",
    "Lors de mon voyage, de {} à {}, j'ai découvert de nouveaux horizons qui ont élargi ma perception du monde.",
    "Parti(e) de {} et arrivé(e) à {}, un voyage parsemé de découvertes culturelles et humaines.",
    "En partant de {}, je me suis dirigé(e) vers {} pour une immersion dans des traditions ancestrales.",
    "C'est de {} à {} que j'ai tracé mon itinéraire, m'offrant une diversité d'expériences inoubliables.",
    "Après avoir quitté {}, je me suis dirigé(e) vers {} pour une aventure en pleine nature.",
    "J'ai choisi de passer par {} avant d'explorer {} et d'y découvrir une scène artistique bouillonnante.",
    "En visitant {} et ensuite {}, j'ai appris à connaître les différentes facettes d'un même pays.",
    "Ils ont exploré {} avant de se diriger vers {} pour un séjour reposant au bord de la mer.",
    "Elles ont parcouru un long chemin de {} à {} où elles ont découvert une hospitalité exceptionnelle.",
    "Il est allé de {} à {} pour ses vacances et y a trouvé une atmosphère de fête permanente.",
    "Elle est partie de {} pour découvrir {} et y a rencontré une communauté accueillante et chaleureuse.",
    "On a visité {} et ensuite {} pour une expérience culinaire inégalée.",
    "Vous êtes allé(e) de {} à {} pour une aventure sportive et de plein air.",
    "Après avoir exploré {}, j'ai été attiré(e) par {} pour sa riche histoire.",
    "En débutant mon voyage à {}, j'ai été immédiatement séduit(e) par l'atmosphère vibrante de la ville avant d'arriver à {}.",
    "De {}, j'ai entrepris un périple jusqu'à {} pour découvrir sa culture unique et ses traditions anciennes.",
    "Après un séjour enrichissant à {}, j'ai pris la décision de me rendre à {} pour son paysage époustouflant.",
    "Ma visite à {} m'a inspiré(e) à explorer les trésors cachés de {}.",
    "En passant par {}, j'ai été émerveillé(e) par la diversité des expériences que cette région offre avant de poursuivre vers {}.",
    "Après avoir découvert les merveilles de {} et y avoir passé du temps, j'ai poursuivi mon voyage vers {} pour une expérience totalement différente.",
    "De {} à {}, chaque étape était une aventure unique où j'ai rencontré des gens formidables et découvert des traditions fascinantes.",
    "J'ai quitté ma ville natale de {} pour me plonger dans l'effervescence de {} et sa vie nocturne animée.",
    "Après avoir contemplé la beauté naturelle de {}, j'ai choisi de me rendre à {} pour explorer ses monuments historiques.",
    "J'ai entrepris mon voyage de {} à {}.",
    "{} m'a enchanté(e) avant d'atteindre {}.",
    "J'ai choisi de passer par {} avant d'explorer {}.",
    "Je suis allé(e) de {} à {}.",
    "J'ai visité {} avant de découvrir {}.",
    "Mon voyage m'a mené de {} à {}.",
    "En passant par {}, j'ai finalement atteint {}.",
    "À la suite de mon passage à {}, j'ai décidé de visiter {}.",
    "De {} jusqu'à {}, chaque étape était une aventure.",
    "Après avoir découvert {}, j'ai décidé de me rendre à {}.",
    "J'ai choisi {} comme prochaine destination après {}.",
    "Entre {} et {}, j'ai découvert des endroits merveilleux.",
    "J'ai quitté {} pour me diriger vers {}.",
    "Après avoir admiré {}, j'ai entrepris d'explorer {}.",
    "De {} à {}, j'ai vécu des moments inoubliables.",
    "Je suis passé(e) de {} à {} pour découvrir de nouveaux horizons.",
    "À la suite de ma visite à {}, j'ai décidé de me rendre à {}.",
    "Entre {} et {}, j'ai rencontré des personnes formidables.",
    "J'ai quitté {} pour m'aventurer à {}.",
    "Après avoir contemplé {}, j'ai décidé de visiter {}.",
    "Mon itinéraire m'a mené de {} à {}.",
    "En partant de {}, je me suis dirigé(e) vers {}.",
    "De {} à {}, chaque étape a été une source d'émerveillement.",
    "Après avoir exploré {}, j'ai continué ma route jusqu'à {}.",
    "En quittant {}, je suis allé(e) à {} pour découvrir de nouveaux paysages.",
    "Entre {} et {}, j'ai découvert une richesse culturelle incroyable.",
    "J'ai décidé de partir de {} pour me rendre à {}.",
    "Après avoir découvert {}, je me suis dirigé(e) vers {}.",
    "Ma visite à {} m'a inspiré(e) à explorer {}.",
    "En voyageant de {} à {}, j'ai été émerveillé(e) par la diversité.",
    "Après avoir contemplé {}, j'ai entrepris de visiter {}.",
    "Je suis allé(e) de {} jusqu'à {} pour explorer de nouveaux lieux.",
    "Après avoir passé du temps à {}, j'ai décidé de me rendre à {}.",
    "En découvrant {}, j'ai été attiré(e) par {}.",
    "De {} à {}, j'ai apprécié chaque moment de mon périple.",
    "Après avoir exploré {}, j'ai décidé de découvrir {}.",
    "Mon itinéraire m'a conduit de {} à {} pour une expérience unique.",
    "Après avoir visité {}, j'ai poursuivi mon voyage jusqu'à {}.",
    "J'ai choisi {} comme prochaine étape après être passé(e) par {}.",
    "De {} à {}, j'ai été fasciné(e) par la diversité des paysages.",
    "Après avoir découvert {}, j'ai décidé de me rendre à {} pour en voir plus.",
    "En voyageant de {} à {}, j'ai été surpris(e) par la richesse culturelle.",
    "Après avoir exploré {}, j'ai entrepris de découvrir {}.",
    "Je suis passé(e) de {} à {} pour une expérience enrichissante.",
    "Après avoir visité {}, j'ai poursuivi mon périple jusqu'à {}.",
    "En quittant {}, je me suis dirigé(e) vers {} pour de nouvelles découvertes.",
    "J'ai choisi {} comme prochaine destination après être passé(e) par {}.",
    "De {} à {}, j'ai été captivé(e) par la beauté des lieux.",
    "Après avoir passé du temps à {}, j'ai décidé de visiter {}.",
    "Mon voyage de {} à {} m'a offert une diversité incroyable.",
    "En partant de {}, je me suis rendu(e) à {} pour de nouvelles aventures.",
    "Après avoir découvert {}, j'ai décidé de me rendre à {} pour en voir plus.",
    "En voyageant de {} à {}, j'ai été surpris(e) par la richesse culturelle.",
    "Après avoir exploré {}, j'ai entrepris de découvrir {}.",
    "Je suis passé(e) de {} à {} pour une expérience enrichissante.",
    "Après avoir visité {}, j'ai poursuivi mon périple jusqu'à {}.",
    "En quittant {}, je me suis dirigé(e) vers {} pour de nouvelles découvertes.",
    "J'ai choisi {} comme prochaine destination après être passé(e) par {}.",
    "De {} à {}, j'ai été captivé(e) par la beauté des lieux.",
    "Après avoir passé du temps à {}, j'ai décidé de visiter {}.",
    "Mon voyage de {} à {} m'a offert une diversité incroyable.",
    "En partant de {}, je me suis rendu(e) à {} pour de nouvelles aventures.",
    "Je suis allé(e) de {} à {}.",
    "J'ai visité {} avant de découvrir {}.",
    "De {} à {}, j'ai parcouru un long chemin.",
    "À la suite de mon séjour à {}, j'ai voyagé jusqu'à {}.",
    "Mon périple m'a mené de {} à {}.",
    "Je me suis rendu(e) de {} vers {}.",
    "Après {} est venu(e) {} lors de mon voyage.",
    "J'ai quitté {} pour me rendre à {}.",
    "En partant de {}, je suis arrivé(e) à {}.",
    "De {} jusqu'à {}, mon itinéraire était passionnant.",
    "J'ai exploré {} avant de me diriger vers {}.",
    "Ma route m'a conduit(e) de {} à {}.",
    "De {} à {}, j'ai découvert de nouveaux horizons.",
    "Après mon séjour à {}, j'ai continué vers {}.",
    "J'ai voyagé de {} à {} pour découvrir de nouvelles cultures.",
    "De {} jusqu'à {}, mon trajet a été plein de surprises.",
    "En partant de {} pour aller à {}, j'ai vécu des aventures incroyables.",
    "J'ai exploré {} avant de me rendre à {}.",
    "J'ai découvert {} après être passé(e) par {}.",
    "De {} à {}, j'ai fait un saut inattendu.",
    "En quittant {}, je me suis dirigé(e) vers {}.",
    "De {} à {}, j'ai fait une escale enrichissante.",
    "Après mon passage à {}, je suis parti(e) pour {}.",
    "J'ai continué mon voyage de {} à {}.",
    "De {} à {}, j'ai exploré de nouveaux horizons.",
    "Après {} est venu {} lors de mon périple.",
    "De {} à {}, j'ai fait une pause avant de repartir vers {}.",
    "J'ai fait étape à {} avant de me rendre à {}.",
    "En partant de {}, je suis arrivé(e) à {}.",
    "J'ai exploré {} avant de me diriger vers {}.",
    "Ma route m'a conduit(e) de {} à {}.",
    "De {} à {}, j'ai découvert de nouveaux horizons.",
    "Après mon séjour à {}, j'ai continué vers {}.",
    "J'ai voyagé de {} à {} pour découvrir de nouvelles cultures.",
    "De {} jusqu'à {}, mon trajet a été plein de surprises.",
    "En partant de {} pour aller à {}, j'ai vécu des aventures incroyables.",
    "Ma visite à {} a été suivie par un passage à {}.",
    "De {} à {}, j'ai apprécié chaque étape de mon voyage.",
    "Après avoir quitté {}, je me suis dirigé(e) vers {}.",
    "J'ai entrepris mon voyage de {} à {}.",
    "En passant de {} à {}, j'ai rencontré des personnes formidables.",
    "De {} à {}, mon parcours a été riche en découvertes.",
    "Après {} vient {} dans mon itinéraire.",
    "J'ai découvert {} après être passé(e) par {}.",
"En quittant {}, je me suis dirigé(e) vers {}.",
    "De {} à {}, j'ai fait une escale enrichissante.",
    "Après mon passage à {}, je suis parti(e) pour {}.",
    "J'ai continué mon voyage de {} à {}.",
    "De {} à {}, j'ai exploré de nouveaux horizons.",
    "Après {} est venu {} lors de mon périple.",
    "De {} à {}, j'ai fait une pause avant de repartir vers {}.",
    "J'ai fait étape à {} avant de me rendre à {}.",
    "De {} à {}, j'ai parcouru un long chemin.",
    "À la suite de mon séjour à {}, j'ai voyagé jusqu'à {}.",
    "En partant de {}, je me suis rendu(e) à {}.",
    "Mon voyage de {} à {} était incroyable.",
    "Lors de mon passage de {} à {}, j'ai été émerveillé(e).",
    "Nous avons voyagé de {} à {} ensemble.",
    "En visitant {} et ensuite {}, j'ai appris beaucoup de choses.",
    "Ils ont exploré {} avant de se diriger vers {}.",
    "Elles ont parcouru un long chemin de {} à {}.",
    "Il est allé de {} à {} pour ses vacances.",
    "Elle est partie de {} pour découvrir {}.",
    "On a visité {} et ensuite {} pour une expérience inoubliable.",
    "Vous êtes allé(e) de {} à {} pour vos vacances.",
    "En passant de {} à {}, tu as trouvé quelque chose d'intéressant.",
    "Lors de votre séjour de {} à {}, vous avez vu beaucoup de choses.",
    "Ils ont voyagé de {} à {} pour affaires.",
    "Elles sont parties de {} à {} pour une escapade.",
    "Il a parcouru un long chemin de {} à {}.",
    "Elle a découvert {} après avoir visité {}.",
    "On est allé de {} à {} pour des raisons spéciales.",
    "Nous sommes partis de {} à {} pour explorer.",
    "En visitant {} et ensuite {}, nous avons réalisé beaucoup de choses.",
    "Vous avez exploré {} avant de vous rendre à {}.",
    "En passant de {} à {}, vous avez eu une aventure incroyable.",
    "Ils sont partis de {} à {} pour des vacances reposantes.",
    "Elles ont voyagé de {} à {} pour une expérience enrichissante.",
    "Il est allé de {} à {} pour se ressourcer.",
    "Elle est partie de {} pour découvrir {} et s'y installer.",
    "On a visité {} et ensuite {} pour une escapade culturelle.",
    "Vous êtes allé(e) de {} à {} pour un changement de paysage.",
    "En passant de {} à {}, tu as découvert de nouvelles perspectives.",
    "Lors de votre séjour de {} à {}, vous avez vécu des moments uniques.",
    "Ils ont voyagé de {} à {} pour des affaires importantes.",
    "Elles sont parties de {} à {} pour une aventure mémorable.",
    "Lors de mon voyage, de {} à {}, j'ai découvert de nouveaux horizons.",
    "Parti(e) de {} et arrivé(e) à {}, un voyage inoubliable.",
    "En partant de {}, je me suis dirigé(e) vers {}.",
    "C'est de {} à {} que j'ai tracé mon itinéraire.",
    "{} m'a enchanté(e) avant d'atteindre {}.",
    "J'ai choisi de passer par {} avant d'explorer {}.",
    "J'ai choisi de passer par {}.",
]


class DataGenerator:
    def __init__(self):
        self.url = "https://static.data.gouv.fr/resources/regions-departements-villes-et-villages-de-france-et-doutre-mer/20180802-085038/French-zip-code-3.0.0-CSV.tar.gz"
        # self.download_and_extract_data() decomment if already download

        unique_patterns = list(set(patterns))
        unique_patterns.sort()
        self.patterns = unique_patterns

        self.cities = pd.read_csv(
            "datas/csv/cities.csv", encoding="utf-8", usecols=["name"]
        )
        self.sentences = []
        self.docs = []
        self.load_spacy_model()

    def download_and_extract_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
                tar.extractall(path="datas")
            logging.info("Data downloaded and extracted successfully.")
        else:
            logging.error("Failed to download the file.")

    def load_spacy_model(self):
        self.nlp = spacy.load("fr_core_news_sm")
        logging.info("SpaCy model loaded successfully.")

    def generate_sentences(self):
        logging.info("Generating sentences...")
        num_sentences = len(self.patterns)
        for _ in range(num_sentences):
            for _ in range(num_sentences):

                pattern = random.choice(self.patterns)
                pattern_elements = pattern.count("{}")
                available_cities = self.cities["name"].tolist()

                if pattern_elements > len(available_cities):
                    pattern_elements = len(available_cities)
                replacements = random.sample(available_cities, pattern_elements)

                line = pattern.format(*replacements)
                    
                depart_start_index = line.index(replacements[0])
                depart_end_index = depart_start_index + len(replacements[0])

                if (len(replacements) >= 2):
                    if replacements[0] not in replacements[1] and replacements[1] not in replacements[0]:
                        arr_start_index = line.index(replacements[1])
                        arr_end_index = arr_start_index + len(replacements[1])

                        self.sentences.append(
                            {
                                "id": len(self.sentences) + 1,
                                "text": line,
                                "label": [
                                    [depart_start_index, depart_end_index, "DEP"],
                                    [arr_start_index, arr_end_index, "DEST"],
                                ],
                            }
                        )

                else:
                    self.sentences.append(
                        {
                            "id": len(self.sentences) + 1,
                            "text": line,
                            "label": [
                                [depart_start_index, depart_end_index, "DEP"],
                            ],
                        }
                    )

    def process_sentences(self):
        logging.info("Processing sentences...")
        for sentence in self.sentences:
            doc = self.nlp(sentence["text"])
            ents = []
            for start, end, label in sentence["label"]:
                span = doc.char_span(start_idx=start, end_idx=end, label=label)
                if span is not None:
                    ents.append(span)
                else:
                    print(
                        "Skipping span (does not align to tokens):",
                        start,
                        end,
                        label,
                        doc.text[start:end],
                    )

            doc.ents = ents
            self.docs.append(doc)

    def save_to_csv(self, file_path, docs):
        logging.info(f"Saving data to {file_path}...")

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Sentence #", "Word", "POS", "Tag", "sentence"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            sentence_id = 0

            for doc in docs:
                sentence_id += 1
                sentence_tokens = [token.text for token in doc]
                sentence_iob_tags = biluo_to_iob(doc_to_biluo_tags(doc))
                sentence_pos_tags = [token.pos_ for token in doc]

                for token, pos_tag, iob_tag in zip(
                    sentence_tokens, sentence_pos_tags, sentence_iob_tags
                ):
                    writer.writerow(
                        {
                            "Sentence #": "Sentence:" + str(sentence_id),
                            "Word": token,
                            "POS": pos_tag,
                            "Tag": iob_tag,
                            "sentence": doc,
                        }
                    )

    def split_data(self, train_ratio=0.2, dev_ratio=0.1):
        num_sentences = len(self.sentences)
        num_train = int(num_sentences * train_ratio)
        num_dev = int(num_sentences * dev_ratio)
        num_test = int(num_sentences * dev_ratio)

        train_set = self.docs[:num_train]
        dev_set = self.docs[num_train : num_train + num_dev]
        test_set = self.docs[-num_test:]

        train_file_path = "datas/train_iob.csv"
        dev_file_path = "datas/dev_iob.csv"
        test_file_path = "datas/test_iob.csv"

        self.save_to_csv(train_file_path, train_set)
        self.save_to_csv(dev_file_path, dev_set)
        self.save_to_csv(test_file_path, test_set)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("Generating data...")

    data_generator = DataGenerator()
    data_generator.generate_sentences()
    data_generator.process_sentences()
    data_generator.split_data()
