import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import spotlight
import urllib, json
import pandas as pd
from collections import Counter
import random
import os
cn = Namespace("http://nhscausalknowledgegraph.org/condtion/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
import numpy as np

# load the graph
g = rdflib.Graph()
result = g.parse('cknns/nhskg', format='turtle')

# setting self-namespaces 
causes = URIRef(cn.causesDisease)
anatomicOn = URIRef(cn.causeOnAnatomicStructure)
drug = URIRef(cn.drugTo)
diag = URIRef(cn.diagnosisTo)
symptomOf = URIRef(cn.causesSymptom)
treatment = URIRef(cn.treatmentTo)
#question=  URIRef(cn.question)
seasonOf = URIRef(cn.seasonAffectTo)
hasCP = URIRef(cn.hasCausalProbablity)
#anabout = URIRef(cn.aLabel)
sameAs = URIRef(owl.sameAs)
agegroup = URIRef(cn.causesAffectionToAgeGroup)
physiologyOf = URIRef(cn.causesPhysiology)
habitTo = URIRef(cn.HabitCausesTo)
speciesTo = URIRef(cn.SpeciesCausesTo)
disease = URIRef('http://dbpedia.org/ontology/Disease')
wikidisease = URIRef('https://www.wikidata.org/wiki/Q12136')
anat = URIRef('http://dbpedia.org/ontology/AnatomicalStructure')
wikianat = URIRef('https://www.wikidata.org/wiki/Q4936952')
symp = URIRef('http://dbpedia.org/resource/Category:Symptoms_and_signs')
presign = URIRef('http://purl.org/dc/terms/subject')
drugs = URIRef('http://dbpedia.org/ontology/Drug')
condition = URIRef('http://umbel.org/umbel/rc/AilmentCondition')
diseaseProperty = URIRef('http://dbpedia.org/property/diseasesdb')
diags = URIRef('http://dbpedia.org/page/Medical_diagnosis')
treats = URIRef('http://dbpedia.org/page/Therapy')
ages = URIRef('http://dbpedia.org/page/Category:Human_development')
sex = URIRef('http://dbpedia.org/page/Category:Sex')
season = URIRef('http://dbpedia.org/page/Season')
species = URIRef('http://dbpedia.org/ontology/Species')
physiology = URIRef('http://dbpedia.org/page/Category:Human_physiology')
habit = URIRef('http://dbpedia.org/page/Category:Habits')
pt = URIRef(cn.causalityTo)
pv = URIRef(cn.pvalue)

def spalq_condition_ds(sym,pg):
    #pg = rdflib.Graph()
    #pg.parse('cknns/pkg.ttl', format='turtle')
    #print (result)
    #print (qres)
    d = []
    for si in sym:
        querystring = "SELECT DISTINCT ?d ?s WHERE {"
        querystring = querystring+"?d <"+RDF.type+"> <"+disease+"> . " 
        querystring = querystring+"?d ?p ?s FILTER regex(str(?s), '"+si+"') . }" 
        qres = g.query(querystring)
        print(si,len(qres))
        for row in qres:
            di = str(row.asdict()['d'].toPython()).split('/')[-1]
            #print (di)
            pvstring = str((1.0/len(qres)))
            #print (pvstring)
            snode = BNode()
            subj = URIRef(row.asdict()['d'].toPython())
            obj = URIRef(row.asdict()['s'].toPython())
            pg.add( (subj, RDF.type, disease) )
            pg.add( (obj, RDF.type, symp) )
            pg.add( (subj, hasCP, snode ) )
            pg.add( (snode, pt, obj) )
            pg.add( (snode, pv, Literal(pvstring)) )
            d.append(di)
    #pg.serialize(destination='cknns/pkg.ttl', format='turtle')
    #pg.close()
    return d

def spalq_position_ds(posi,pg):
    #pg = rdflib.Graph()
    #pg.parse('cknns/pkg.ttl', format='turtle')
    #print (result)
    #print (qres)
    d = []
    for si in posi:
        querystring = "SELECT DISTINCT ?d ?s WHERE {"
        querystring = querystring+"?d <"+RDF.type+"> <"+disease+"> . " 
        querystring = querystring+"?d <"+anatomicOn+"> ?s FILTER regex(str(?s), '"+si+"') . }" 
        qres = g.query(querystring)
        print(si,len(qres))
        for row in qres:
            di = str(row.asdict()['d'].toPython()).split('/')[-1]
            #print (di)
            pvstring = str((1.0/len(qres)))
            #print (pvstring)
            snode = BNode()
            subj = URIRef(row.asdict()['d'].toPython())
            obj = URIRef(row.asdict()['s'].toPython())
            pg.add( (subj, RDF.type, disease) )
            pg.add( (obj, RDF.type, anat) )
            pg.add( (subj, hasCP, snode ) )
            pg.add( (snode, pt, obj) )
            pg.add( (snode, pv, Literal(pvstring)) )
            d.append(di)
    #pg.serialize(destination='cknns/pkg.ttl', format='turtle')
    #pg.close()
    return d

def spalq_pre_history(dis,sym,pg):
    #pg = rdflib.Graph()
    #pg.parse('cknns/pkg.ttl', format='turtle')
    #print (result)
    #print (qres)
    d = []
    d1 = []
    if dis != '':
        for si in sym:
            si = si.replace(' ','-')
            querystring = "SELECT DISTINCT ?d ?d1 ?s WHERE {"
            querystring = querystring+"?d <"+RDF.type+"> <"+disease+"> FILTER regex(str(?d), '"+dis[0]+"') . "
            querystring = querystring+"?d <"+causes+"> ?d1 ."
            querystring = querystring+"?d1 ?p ?s FILTER regex(str(?s), '"+si+"') . }"
            qres = g.query(querystring)
            print(si,len(qres))
            for row in qres:
                di = str(row.asdict()['d'].toPython()).split('/')[-1]
                pvstring = str((1.0/len(qres)))
                snode = BNode()
                subj = URIRef(row.asdict()['d'].toPython())
                obj1 = URIRef(row.asdict()['d1'].toPython())
                obj2 = URIRef(row.asdict()['s'].toPython())
                pg.add( (subj, RDF.type, disease) )
                pg.add( (obj1, RDF.type, disease) )
                pg.add( (subj, causes, obj1) )
                pg.add( (subj, hasCP, snode ) )
                pg.add( (snode, pt, obj1) )
                pg.add( (snode, pt, obj2) )
                pg.add( (snode, pv, Literal(pvstring)) )
                d.append(di)
                d1.append(obj1)
    #pg.serialize(destination='cknns/pkg.ttl', format='turtle')
    #pg.close()
    return d,d1

def spalq_age_ds(ageg,t,pg):
    #pg = rdflib.Graph()
    #pg.parse('cknns/pkg.ttl', format='turtle')
    #print (result)
    #print (qres)
    d = []
    for si in ageg:
        querystring = "SELECT DISTINCT ?d ?s WHERE {"
        querystring = querystring+"?d <"+RDF.type+"> <"+disease+"> . " 
        querystring = querystring+"?d <"+agegroup+"> ?s FILTER regex(str(?s), '"+si+"') . }" 
        qres = g.query(querystring)
        print(si,len(qres))
        for row in qres:
            di = str(row.asdict()['d'].toPython()).split('/')[-1]
            #print (di)
            pvstring = str((1.0/len(qres)))
            #print (pvstring)
            snode = BNode()
            subj = URIRef(row.asdict()['d'].toPython())
            obj = URIRef(row.asdict()['s'].toPython())
            pg.add( (subj, RDF.type, disease) )
            if t==0:
                pg.add( (obj, RDF.type, ages) )
            else:
                pg.add( (obj, RDF.type, sex) )
            pg.add( (subj, hasCP, snode ) )
            pg.add( (snode, pt, obj) )
            pg.add( (snode, pv, Literal(pvstring)) )
            d.append(di)
    #pg.serialize(destination='cknns/pkg.ttl', format='turtle')
    #pg.close()
    return d

#PKG GENERATION FUNCTION!
def predict_inputs(_syms,_anat,pre_dis,_age,_sex):
    pg = rdflib.Graph()
    spalq_condition_ds(_syms,pg)
    spalq_position_ds(_anat,pg)
    spalq_pre_history(pre_dis,_syms,pg)
    spalq_age_ds(_age,0,pg)
    spalq_age_ds(_sex,1,pg)
    pg.serialize(destination='cknns/a_pkg.ttl', format='turtle')
    pg.close()

def predict_ranking_dic(in1,in2,in3,in4,in5):
    predict_inputs(in1,in2,in3,in4,in5)
    pdictg = rdflib.Graph()
    pdictg.parse('cknns/a_pkg.ttl', format='turtle')
    querystring = "SELECT DISTINCT ?d ?tp ?v WHERE {"
    querystring = querystring+"?d <"+RDF.type+"> <"+disease+"> . " 
    querystring = querystring+"?d <"+hasCP+"> ?cp . "
    querystring = querystring+"?cp <"+pt+"> ?t . ?t <"+RDF.type+"> ?tp . ?cp <"+pv+"> ?v}"
    print (querystring)
    qres = pdictg.query(querystring)
    ddict = {}
    sexv = []
    agev = []
    asv = []
    sdv = []
    indv = []
    for row in qres:
        di = str(row.asdict()['d'].toPython()).split('/')[-1]
        ti = str(row.asdict()['tp'].toPython()).split('/')[-1]
        tv = str(row.asdict()['v'].toPython()).split('/')[-1]
        #print (di,ti,tv)
        if di not in ddict:
            sexv = []
            agev = []
            asv = []
            sdv = []
            indv = []
        if ti =='Category:Sex':
            #print (tv)
            sexv.append(tv)
        elif ti =='Category:Human_development':
            #print (tv)
            agev.append(tv)
        elif ti =='AnatomicalStructure':
            asv.append(tv)
        else:
            if ti =='Category:Symptoms_and_signs':
                sdv.append(tv)
            else:
                indv.append(tv)
        #print (sdv,asv,sdv)
        ddict[di] = [sdv,asv,agev,sexv,indv] 
    return ddict

def prediction_function_main(sym, b_part, condition, ch_ad, gender):
    if not b_part:
        b_part=''
    if not condition:
        condition = ''
    if not ch_ad:
        ch_ad = ''
    if not gender:
        gender = ''

    preparing = predict_ranking_dic(sym, b_part, condition, ch_ad, gender)
    p0 = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    for x, y in preparing.items():
        if len(y[0])>0:
            p=1.0
            for sy in y[0]:
                p=p*float(sy)
                mp=1/p
            p0.append(np.log(mp))
        else:
            p0.append(0)
        if len(y[1])>0:
            p=1
            for sy in y[1]:
                p=p*float(sy)
                mp=1/p
            p1.append(np.log(mp))
        else:
            p1.append(0)
        if len(y[2])>0:
            p=1
            for sy in y[2]:
                p=p*float(sy)
                mp=1/p
            p2.append(np.log(mp))
        else:
            p2.append(0)
        if len(y[3])>0:
            p=1
            for sy in y[3]:
                p=p*float(sy)
                mp=1/p
            p3.append(np.log(mp))
        else:
            p3.append(0)
        if len(y[4])>0:
            p=1
            for sy in y[4]:
                p=p*float(sy)
                mp=1/p
            p4.append(np.log(mp))
        else:
            p4.append(0)
    df = pd.DataFrame(columns=['d', 'pred_v'])
    i=0
    for x, y in preparing.items():
        esym = 0
        eana = 0
        eage = 0
        esex = 0
        eind = 0
        if len(y[0])>0:
            p=1
            for sy in y[0]:
                p=p*float(sy)
                pc=np.log(1/p)
            esym = (pc - min(p0))/(max(p0)-min(p0))
        if len(y[1])>0:
            p=1
            for sy in y[1]:
                p=p*float(sy)
                pc=np.log(1/p)
            eana = (pc - min(p1))/(max(p1)-min(p1))
        if len(y[2])>0:
            p=1
            for sy in y[2]:
                p=p*float(sy)
                pc=np.log(1/p)
            eage = (pc - min(p2))/(max(p2)-min(p2))
        if len(y[3])>0:
            p=1
            for sy in y[3]:
                p=p*float(sy)
                pc=np.log(1/p)
            esex = (pc - min(p3))/(max(p3)-min(p3))
        if len(y[4])>0:
            p=1
            for sy in y[4]:
                p=p*float(sy)
                pc=np.log(1/p)
            eind = (pc - min(p4))/(max(p4)-min(p4))
        if eind == 0:
            er=(0.4*esym+0.4*eana+0.1*eage+0.1*esex)
        else:
            er=(0.4*esym+0.4*eana+0.1*eage+0.1*esex)*eind
        if x =='Food-allergy':
            print(er)
        if x =='Bronchitis':
            print(er)
        df.loc[i]=x,er*100
        i=i+1
    return df.sort_values(by='pred_v', ascending=False)