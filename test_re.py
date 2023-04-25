import json5 as json
import re
info = """
Language model pre-training has been shown to
be effective for improving many natural language
processing tasks (Dai and Le, 2015; Peters et al.,
2018a; Radford et al., 2018; Howard and Ruder,
2018). These include sentence-level tasks such as
natural language inference (Bowman et al., 2015;
Williams et al., 2018) and paraphrasing (Dolan
and Brockett, 2005), which aim to predict the relationships between sentences by analyzing them
holistically, as well as token-level tasks such as
named entity recognition and question answering,
where models are required to produce fine-grained
output at the token level (Tjong Kim Sang and
De Meulder, 2003; Rajpurkar et al., 2016).
""".replace('\n','')
running_re_sub = json.load(open("running_re_sub.jsonc"))
for pattern, repl in running_re_sub.items():
    print(info)
    print("--------------------------------")
    info = re.sub(pattern,repl,info)
    print(pattern,':',repl)
    print("--------------------------------")
    print(info)