from flask import Flask, request, jsonify
import difflib
import unicodedata

app = Flask(__name__)

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
    {"instruction": "À qui est destiné le crédit ?", "output": "Le crédit est exclusivement réservé aux salariés en contrat actif chez Talan."},
    {"instruction": "Puis-je demander un crédit si je suis en période d’essai ?", "output": "Non, les demandes de crédit sont acceptées uniquement après validation de la période d’essai."},
    {"instruction": "Quels sont les types de crédit disponibles ?", "output": "Crédit immobilier (1–10 ans, 5%), crédit auto (1–5 ans, 3%), crédit personnel (1–3 ans, 1%)."},
    {"instruction": "Quelle est la différence entre les trois types de crédits ?", "output": "Le crédit immobilier concerne les biens immobiliers, l'auto pour l’achat d’un véhicule, et le personnel pour des besoins individuels (santé, voyage, etc.)."},
    {"instruction": "Le crédit personnel peut-il être utilisé pour acheter une voiture ?", "output": "Non, l’achat de véhicule nécessite un crédit auto spécifique."},
    {"instruction": "Puis-je faire une simulation de crédit ?", "output": "Oui, une simulation est disponible sur l’espace employé via le portail Talan."},
    {"instruction": "Quel est le taux d’intérêt du crédit immobilier ?", "output": "5% sur une durée de 1 à 10 ans."},
    {"instruction": "Quel est le taux d’un crédit auto ?", "output": "3% sur une durée de 1 à 5 ans."},
    {"instruction": "Quel est le taux d’un crédit personnel ?", "output": "1% sur une durée de 1 à 3 ans."},
    {"instruction": "Quels documents dois-je fournir ?", "output": "Carte d’identité (CIN), trois derniers relevés bancaires, facture ou attestation liée au crédit, fiche de paie récente."},
    {"instruction": "Quels sont les justificatifs pour un prêt immobilier ?", "output": "Une promesse de vente, contrat préliminaire ou devis de construction est requis en plus des pièces standards."},
    {"instruction": "Que faut-il pour un crédit auto ?", "output": "Facture pro forma ou devis du véhicule à financer, en plus des autres pièces."},
    {"instruction": "Quels justificatifs pour un prêt personnel ?", "output": "Une attestation de besoin (frais médicaux, études, voyage) est recommandée."},
    {"instruction": "Puis-je obtenir plusieurs crédits à la fois ?", "output": "Non, un seul crédit peut être actif par employé à la fois."},
    {"instruction": "Est-ce que les intérimaires ou freelances peuvent en bénéficier ?", "output": "Non, seuls les salariés en CDI chez Talan sont éligibles."},
    {"instruction": "Que se passe-t-il en cas de départ de l’entreprise ?", "output": "Le crédit devient immédiatement exigible ou doit être renégocié avec les ressources humaines."},
    {"instruction": "Combien de temps prend le traitement d’une demande ?", "output": "En moyenne 5 jours ouvrés après la réception complète du dossier."},
    {"instruction": "Puis-je transmettre mes documents par email ?", "output": "Oui, les documents peuvent être scannés et envoyés via l’interface RH ou par mail sécurisé."},
    {"instruction": "Qui valide ma demande de crédit ?", "output": "Le service RH et la direction financière valident conjointement chaque dossier."},
    {"instruction": "Puis-je rembourser plus tôt que prévu ?", "output": "Oui, un remboursement anticipé est possible sans pénalité."},
    {"instruction": "Puis-je demander un crédit pendant mon congé ?", "output": "Oui, tant que vous êtes toujours salarié actif chez Talan."},
    {"instruction": "Comment suis-je informé de l’avancement de ma demande ?", "output": "Vous recevrez un email ou une notification sur l’espace employé à chaque étape du traitement."},
    {"instruction": "Puis-je être refusé ?", "output": "Oui, si les critères d’éligibilité ou de solvabilité ne sont pas remplis."},
    {"instruction": "Quelles sont les causes fréquentes de refus ?", "output": "Absence de documents, situation bancaire non saine, ancienneté insuffisante, projet non cohérent avec le type de crédit."},
    {"instruction": "Est-ce que je peux faire un crédit pour un membre de ma famille ?", "output": "Non, le crédit doit être directement lié à vos propres besoins."},
    {"instruction": "Est-ce que le taux est négociable ?", "output": "Non, les taux sont fixes et définis par la politique interne de Talan."},
    {"instruction": "Existe-t-il une assurance obligatoire ?", "output": "Non, mais une assurance emprunteur est fortement recommandée, notamment pour les prêts immobiliers."},
    {"instruction": "Que faire si je perds ma fiche de paie ?", "output": "Vous pouvez demander une copie au service RH."},
    {"instruction": "Quelle est la mensualité pour un crédit auto de 20 000 TND sur 5 ans ?", "output": "Avec un taux de 3%, cela équivaut à environ 359 TND/mois (simulation à confirmer)."},
    {"instruction": "Quel est l’âge minimum pour bénéficier du crédit ?", "output": "Vous devez avoir au moins 18 ans et être en contrat actif chez Talan."},
    {"instruction": "Puis-je choisir ma date de prélèvement ?", "output": "Oui, lors de la signature du contrat, vous pouvez choisir la date mensuelle."},
    {"instruction": "Le crédit est-il renouvelable ?", "output": "Non, un nouveau crédit ne peut être demandé qu’après remboursement total de l’ancien."},
    {"instruction": "Est-ce que je peux annuler ma demande ?", "output": "Oui, tant que le contrat n’a pas été signé, la demande peut être annulée sans frais."},
    {"instruction": "Les crédits sont-ils soumis à l’approbation d’une banque ?", "output": "Non, le crédit est géré exclusivement en interne par Talan."},
    {"instruction": "Comment le crédit est-il versé ?", "output": "Les fonds sont versés sur le compte bancaire indiqué après validation finale du dossier."},
    {"instruction": "Est-ce que le taux change avec l’ancienneté ?", "output": "Non, les taux sont fixes et indépendants de l’ancienneté."},
    {"instruction": "Qui puis-je contacter pour avoir plus d’informations ?", "output": "Le service RH ou votre référent financier est à votre disposition pour toute question."},
    {"instruction": "Je n’ai pas de facture, puis-je quand même faire une demande ?", "output": "Une attestation de besoin ou un devis est obligatoire pour justifier le crédit."},
    {"instruction": "Quelles informations dois-je fournir dans la demande ?", "output": "Montant demandé, durée souhaitée, type de crédit, coordonnées bancaires, pièce justificative du projet."},
    {"instruction": "Le crédit figure-t-il sur mon bulletin de salaire ?", "output": "Oui, la mensualité est prélevée directement et visible sur votre fiche de paie."},
    {"instruction": "Quel est le plafond maximum pour chaque crédit ?", "output": "Le plafond dépend de votre revenu mensuel net et du type de crédit. Simulation recommandée."},
    {"instruction": "Puis-je demander un crédit sans relevé bancaire ?", "output": "Non, les trois derniers relevés bancaires sont obligatoires."}
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