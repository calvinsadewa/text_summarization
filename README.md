# text_summarization
Text summarization using cortical SDR (http://www.cortical.io/technology_representations.html) and PageRank algorithm (networkx, https://networkx.github.io/)

### How it work
- Split text into sentences
- Calculate Similarity between sentences (by changing sentence to cortical SDR and calculate similarity using cosine similarity)
- Create a graph with node as sentence and similarity as edge
- PageRank the graph (using networkx) (The sentence with highest rank assumed to be the most representative sentence)
- Create Minimum Spanning Tree from PageRank Result
- Get n sentence from minimum spanning tree starting from root by minimum distance from root (Probably not the most effecient)

### Code
```
with open("magic.txt",encoding="utf8") as magic_text:
    text = magic_text.read()
    summ = summarize(text,10)
    for sentence in summ:
        print(sentence.encode('cp850', errors='replace'))
```
Result
```
b' Note that although more knowledge always helps, a complete understanding of magic is not necessary for this?for example, new taxonomies continue to appear in various subdomains of vision science (Changizi, 2009; Gregory, 2009) even though our scientific understanding of visual perception remains incomplete'
b', Houdin, 1868/2006; Wonder and Minch, 1996), a better understanding of the perceptual and cognitive mechanisms underlying various aspects of magic could well inform the design of better magic tricks, and perhaps even presentation techniques'
b' But how might this be done? And to what extent could magic ultimately contribute to our exploration of the human mind?\n\nIn this paper we propose a framework that describes many of the approaches that have been?or could be?taken to use magic to investigate human perception and cognition'
b' However, controlled investigation requires a version of the trick less concerned with the circumstances of a particular performance, and more with the general factors that influence the observer?s perceptual and cognitive mechanisms'
b'\nEXPLANATION\n\nAs in the case of other phenomena involving perception or cognition, the explanation of a magic trick can be sought at three distinct levels of analysis: (a) the psychological mechanisms involved, (b) the neural implementation of these, and (c) the functional considerations (or computational theory) as to why these mechanisms are as they are'
b' This paradigm has been used to investigate infants? understanding of the physical world in general, ranging from the idea that objects cannot occupy the same space (penetration effect) to the concept that stable objects need a support of some kind (see Baillargeon, 1994)'
b' For instance, why do we even have a sense of wonder in the first place? Which circumstances invoke it? What kinds of violations give rise to what kinds of wonder? What?if anything?does this experience enable us to do?\n\nSuch issues are the concern of a functional (or computational) level of analysis, which focuses not only on describing the function carried out, but also on justifying why it has the form it has'
b' Individual differences exist in magical thinking (Subbotsky, 2004; Subbotsky and Quinteros, 2002), and it would be worth exploring whether similar differences exist in regards to other aspects of magic; they might reveal interesting personality traits, or cognitive or perceptual styles'
b' Could the study of magic be carried out in a coherent way that encompasses most magic tricks? Could it eventually become an area of research akin to, say, vision science, resulting in a better understanding of known effects, and perhaps even the prediction of new ones?\n\nIn what follows, we present a few?admittedly incomplete?suggestions about how this issue might be approached'
b' But our intent here is to show that there does exist some possibility of organizing a study of magic as a scientific discipline, one that could enable a better understanding of magic tricks, and ultimately, a better understanding of human perception and cognition'
```
