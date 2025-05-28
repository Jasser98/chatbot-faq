from flask import Flask, request, jsonify
from flask_cors import CORS  # ➕ ajouter ça
import difflib
import unicodedata

app = Flask(__name__)
CORS(app)  # ➕ autorise toutes les origines (ou configure si besoin)

# 🔧 Nettoyage du texte
def nettoyer(text):
    text = text.lower().strip()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

# ✅ Données FAQ
faq_data = [
    
  {
    "instruction":"Quels sont les crédits offerts ?",
    "output":"Taloan propose trois types de crédits : immobilier (3 à 10 ans, 5%), auto (2 à 5 ans, 3%) et personnel (1 à 3 ans, 1%)."
  },
  {
    "instruction":"Quels crédits sont disponibles chez Taloan ?",
    "output":"Les employés peuvent choisir entre crédit immobilier, crédit auto ou crédit personnel avec des taux et durées spécifiques."
  },
  {
    "instruction":"Puis-je prendre un crédit immobilier chez Taloan ?",
    "output":"Oui, le crédit immobilier est disponible pour une durée de 3 à 10 ans avec un taux de 5%."
  },
  {
    "instruction":"Quelle est la durée d’un crédit personnel ?",
    "output":"Un crédit personnel dure entre 1 et 3 ans, avec un taux de 1%."
  },
  {
    "instruction":"Quel est le taux d’intérêt du crédit auto ?",
    "output":"Le crédit auto est proposé avec un taux fixe de 3%."
  },
  {
    "instruction":"Comment vais-je recevoir les notifications ?",
    "output":"Toutes les notifications importantes sont envoyées par e-mail."
  },
  {
    "instruction":"Est-ce que je reçois un e-mail pour chaque étape ?",
    "output":"Oui, un e-mail est envoyé à chaque étape importante de votre demande."
  },
  {
    "instruction":"Les notifications arrivent-elles par SMS ?",
    "output":"Non, actuellement seules les notifications par e-mail sont supportées."
  },
  {
    "instruction":"Quels documents dois-je fournir ?",
    "output":"Une pièce d'identité, une fiche de paie récente et un RIB."
  },
  {
    "instruction":"Quel format pour les documents ?",
    "output":"Les documents doivent être en format PDF ou JPEG."
  },
  {
    "instruction":"Comment envoyer mes documents ?",
    "output":"Utilisez l’espace client pour téléverser vos fichiers après avoir rempli le formulaire."
  },
  {
    "instruction":"Quelle est l’étape initiale dans la demande de crédit ?",
    "output":"La première étape consiste à remplir le formulaire de demande."
  },
  {
    "instruction":"Quelle est l’étape d’analyse des documents dans la demande de crédit ?",
    "output":"Les documents sont analysés pour vérifier leur conformité."
  },
  {
    "instruction":"Quelle est l’étape de négociation dans la demande de crédit ?",
    "output":"Une négociation a lieu si le montant dépasse le seuil autorisé."
  },
  {
    "instruction":"Quelle est l’étape de génération du devis dans la demande de crédit ?",
    "output":"Un devis final est généré pour récapituler les conditions."
  },
  {
    "instruction":"Quelle est l’étape de signature dans la demande de crédit ?",
    "output":"Le contrat est ensuite signé par les deux parties."
  },
  {
    "instruction":"Quelle est l’étape finale dans la demande de crédit ?",
    "output":"Une fois signé, le montant est transféré."
  },
  {
    "instruction":"Quelle est l’étape de remboursement dans la demande de crédit ?",
    "output":"Le remboursement se fait ensuite selon l’échéancier établi."
  },
  {
    "instruction":"Comment puis-je faire une simulation de crédit ?",
    "output":"Accédez à la page de simulation, remplissez les champs requis et soumettez."
  },
  {
    "instruction":"Où dois-je faire une simulation de crédit ?",
    "output":"La simulation se fait avant l’ouverture d’un espace client."
  },
  {
    "instruction":"Quelles étapes suivre pour faire une simulation de crédit ?",
    "output":"La simulation se fait avant l’ouverture d’un espace client."
  },
  {
    "instruction":"Comment faire une réclamation ?",
    "output":"Vous pouvez soumettre une réclamation via la page ‘Réclamations’."
  },
  {
    "instruction":"Puis-je faire une réclamation ?",
    "output":"Toute réclamation est traitée sous 48 heures."
  },
  {
    "instruction":"Où dois-je faire une réclamation ?",
    "output":"Allez dans la section Réclamation de l’espace client et remplissez le formulaire."
  },
  {
    "instruction":"À qui m’adresser pour faire une réclamation ?",
    "output":"Allez dans la section Réclamation de l’espace client et remplissez le formulaire."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 1)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 2)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 3)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 4)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 5)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 6)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 7)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 8)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 9)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 10)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 11)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 12)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 13)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 14)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 15)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 16)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 17)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 18)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 19)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 20)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 21)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 22)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 23)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 24)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 25)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 26)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 27)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 28)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 29)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 30)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 31)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 32)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 33)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 34)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 35)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 36)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 37)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 38)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 39)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 40)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 41)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 42)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 43)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 44)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 45)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 46)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 47)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 48)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 49)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 50)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 51)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 52)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 53)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 54)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 55)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 56)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 57)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 58)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 59)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 60)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 61)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 62)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 63)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 64)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 65)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 66)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 67)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 68)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 69)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 70)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 71)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 72)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 73)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 74)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 75)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 76)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 77)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 78)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 79)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 80)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 81)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 82)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 83)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 84)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 85)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 86)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 87)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 88)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 89)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 90)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 91)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 92)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 93)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 94)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 95)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 96)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 97)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 98)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 99)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 100)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 101)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 102)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 103)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 104)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 105)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 106)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 107)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 108)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 109)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 110)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 111)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 112)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 113)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 114)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 115)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 116)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 117)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 118)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 119)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 120)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 121)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 122)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 123)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 124)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 125)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 126)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 127)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 128)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 129)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 130)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 131)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 132)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 133)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 134)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 135)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 136)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 137)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 138)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 139)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 140)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 141)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 142)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 143)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 144)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 145)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 146)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 147)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 148)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 149)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 150)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 151)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 152)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 153)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 154)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 155)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 156)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 157)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 158)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 159)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 160)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 161)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 162)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 163)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 164)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 165)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  },
  {
    "instruction":"Puis-je avoir plusieurs crédits à la fois ? (version 166)",
    "output":"Oui, sous certaines conditions et en fonction de votre capacité d’endettement."
  },
  {
    "instruction":"Comment connaître le montant maximum auquel j’ai droit ? (version 167)",
    "output":"Le montant maximal dépend de votre ancienneté et de votre salaire."
  },
  {
    "instruction":"Puis-je rembourser mon crédit par anticipation ? (version 168)",
    "output":"Oui, un remboursement anticipé est autorisé sans frais."
  },
  {
    "instruction":"À quelle fréquence sont envoyés les relevés ? (version 169)",
    "output":"Les relevés sont envoyés chaque mois par e-mail."
  },
  {
    "instruction":"Le taux d’intérêt peut-il changer ? (version 170)",
    "output":"Non, les taux sont fixes pour chaque type de crédit."
  },
  {
    "instruction":"Puis-je modifier ma demande après soumission ? (version 171)",
    "output":"Oui, vous pouvez la modifier avant l’étape de négociation."
  },
  {
    "instruction":"Combien de temps faut-il pour obtenir une réponse ? (version 172)",
    "output":"En moyenne, une réponse est donnée sous 3 à 5 jours ouvrés."
  },
  {
    "instruction":"Qui peut demander un crédit chez Taloan ? (version 173)",
    "output":"Tous les employés de Talan peuvent faire une demande de crédit."
  },
  {
    "instruction":"Comment activer mon compte client ? (version 174)",
    "output":"Remplissez le formulaire depuis la page d’accueil et attendez notre appel."
  },
  {
    "instruction":"Mon compte est inactif, que faire ? (version 175)",
    "output":"Contactez l’assistance via votre espace client pour réactivation."
  }


]

# 🔍 Recherche exacte
def find_answer_exact(user_question):
    cleaned_user = nettoyer(user_question)
    for item in faq_data:
        if nettoyer(item["instruction"]) == cleaned_user:
            return item["output"]
    return None

# 🔍 Recherche floue avec difflib
def find_answer_fuzzy(user_question):
    cleaned_question = nettoyer(user_question)
    questions = [item["instruction"] for item in faq_data]
    cleaned_questions = [nettoyer(q) for q in questions]

    closest_match = difflib.get_close_matches(cleaned_question, cleaned_questions, n=1, cutoff=0.3)
    if closest_match:
        index = cleaned_questions.index(closest_match[0])
        return faq_data[index]["output"]
    return None

# 🌐 Endpoint API
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("question", "")
    response = find_answer_exact(user_input)
    if not response:
        response = find_answer_fuzzy(user_input)
    if not response:
        response = "Désolé, je n’ai pas compris votre question."
    return jsonify({"response": response})

@app.route('/', methods=['GET'])
def home():
    return "✅ Chatbot FAQ is running. Use POST /chat with a JSON body {\"question\": \"...\"}"


# 🔁 Démarrage avec port dynamique pour Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)