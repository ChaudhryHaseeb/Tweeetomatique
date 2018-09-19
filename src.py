import tweepy, os, random, emoji, networkx as nx

consumer_key = "9zCEFtXq72cSIWqdhFtMWC0GW"
consumer_secret = "XBeTVvrdHu9uBlXT7WBXqtJ6FZC35VuUL0OPMbP0d6juZOJajy"
access_token = "964503642987474950-1RvDhQ4TXUL0woHHTrZO5ukGQL8P0eR"
access_token_secret = "kEIXOtUoM3VuBIKYaOSDckvt5GHNuRWFdp57XC0SkWElh"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


nbFic=len(os.listdir('Tweets'))
G=nx.MultiDiGraph()
liste=[]
mots=[]
n=1


def recuperation_dans_fichiers(api):
    i=1
    for status in tweepy.Cursor(api.user_timeline, screen_name='@fhollande', tweet_mode='extended').items():
        fichier = open("Tweets/tweet"+str(i)+".txt", "w")
        fichier.write(status._json['full_text'])
        fichier.close()
        i=i+1

def retrait_char_speciaux(contenu):
    fd = open("indesirable.txt", "r")
    indes = fd.read().split(" ")
    for ele in indes:
        for mot in contenu:
            if (mot is ele) or (mot.startswith(ele)):
                contenu.remove(mot)
            for c in mot:
                if (c in mot):
                    if (c in emoji.UNICODE_EMOJI):
                        mot.replace(c, "")
    return contenu 
    
def recuperation_liste_mots_tweet(nb):
    fd = open("Tweets/tweet"+str(nb)+".txt","r" ) 
    contenu = fd.read()
    fd.close()
    return contenu.lower().split(" ")

def creation_noeuds_arcs():
    i=0
    for mot in liste:
        G.add_node(mot)
    for i in range(len(liste)-1):
        if G.has_edge(liste[i], liste[i+1])==False:
            G.add_edge(liste[i], liste[i+1],key='poids', weight=1)
        else:
            G[liste[i]][liste[i+1]]['poids']['weight'] = G[liste[i]][liste[i+1]]['poids']['weight']+1

def generation_tweet (mots):
    i=0
    newTweet=[]
    while len(mots):
        choice=random.choice(mots)
        del(mots[:])
        newTweet.append(choice)
        for voisin in list(G.neighbors(choice)):
            while i <= G[choice][voisin]['poids']['weight']:
                 mots.append(voisin)
                 i=i+1
            i=0
    affichage_tweet_generer(newTweet)
    ajouter_tweet_fichier(newTweet)
    
def affichage_tweet_generer(tweet):
    tweet[0]=tweet[0][0].upper()+tweet[0][1:]
    for mot in tweet:
        print(mot, end=' ')
    print('\n')

def ajouter_tweet_fichier(tweet):
    fichier = open("Tweets_genere.txt", "a")
    fichier.write(" ".join(tweet)+"\n\n")
    fichier.close()

while n<nbFic:
    #recuperation_dans_fichiers(api)
    liste = retrait_char_speciaux(recuperation_liste_mots_tweet(n))
    if (liste[0]=="rt"):
        n=n+1
    else:
        mots.append(liste[0])
        creation_noeuds_arcs ()
        n=n+1

generation_tweet(mots)

G.clear()