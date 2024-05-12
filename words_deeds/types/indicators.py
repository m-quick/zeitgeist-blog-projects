from dataclasses import dataclass, field


@dataclass
class Indicator:
    name: str
    more_dem: list[int] = field(default_factory=lambda: [])
    less_dem: list[int] = field(default_factory=lambda: [])


partrght = Indicator(name="partrght", more_dem=[1])

partprf = Indicator(name="partprf", more_dem=[4], less_dem=[1, 2, 3])

partprh = Indicator(name="partprh", more_dem=[4], less_dem=[1, 2, 3])

oversght = Indicator(name="oversght", more_dem=[1, 2, 3], less_dem=[4])

voteun = Indicator(name="voteun", more_dem=[1], less_dem=[2])

hoselect = Indicator(name="hoselect", more_dem=[2], less_dem=[1, 3])

hogelect = Indicator(name="hogelect", more_dem=[2], less_dem=[1, 3, 4])

express = Indicator(name="express", more_dem=[1])

opinion = Indicator(name="opinion", more_dem=[1])

censor = Indicator(name="censor", more_dem=[1, 2])

press = Indicator(name="press", more_dem=[1])

assoc = Indicator(name="assoc", more_dem=[1])

govmed = Indicator(name="govmed", more_dem=[2, 3], less_dem=[1])

hosdiss = Indicator(name="hosdiss", more_dem=[1], less_dem=[2])

hosimm = Indicator(name="hosimm", more_dem=[2, 3], less_dem=[1])

hogdiss = Indicator(name="hogdiss", more_dem=[1], less_dem=[2])

intexec = Indicator(name="intexec", more_dem=[1, 2, 3], less_dem=[4])

invexe = Indicator(name="invexe", more_dem=[1], less_dem=[2])

standliv = Indicator(name="standliv", more_dem=[1])

equal = Indicator(name="equal", more_dem=[1])

judind = Indicator(name="judind", more_dem=[1], less_dem=[2])

judfin = Indicator(name="judfin", more_dem=[1])

judsal = Indicator(name="judsal", more_dem=[1], less_dem=[2])

rulelaw = Indicator(name="rulelaw", more_dem=[1])

freerel = Indicator(name="freerel", more_dem=[1])

privacy = Indicator(name="privacy", more_dem=[1])

freemove = Indicator(name="freemove", more_dem=[1])

petition = Indicator(name="petition", more_dem=[1])

assem = Indicator(name="assem", more_dem=[1])

strike = Indicator(name="strike", more_dem=[1, 2])

inalrght = Indicator(name="inalrght", more_dem=[1])

devlpers = Indicator(name="devlpers", more_dem=[1])

votelim_3 = Indicator(name="votelim_3", more_dem=[0], less_dem=[1])

votelim_4 = Indicator(name="votelim_4", more_dem=[0], less_dem=[1])

votelim_7 = Indicator(name="votelim_7", more_dem=[0], less_dem=[1])

votelim_13 = Indicator(name="votelim_13", more_dem=[0], less_dem=[1])

votelim_14 = Indicator(name="votelim_14", more_dem=[0], less_dem=[1])

votelim_15 = Indicator(name="votelim_15", more_dem=[0], less_dem=[1])

legdiss = Indicator(name="votelim_15", less_dem=[1, 2, 3, 4])

votelim_15 = Indicator(name="votelim_15", more_dem=[0], less_dem=[1])

hosrest_1 = Indicator(name="hosrest_1", more_dem=[0], less_dem=[1])

hosrest_2 = Indicator(name="hosrest_2", more_dem=[0], less_dem=[1])

hosrest_3 = Indicator(name="hosrest_3", more_dem=[0], less_dem=[1])

hosrest_4 = Indicator(name="hosrest_4", more_dem=[0], less_dem=[1])

hosrest_7 = Indicator(name="hosrest_7", more_dem=[0], less_dem=[1])

hosrest_10 = Indicator(name="hosrest_10", more_dem=[0], less_dem=[1])

hogrest_1 = Indicator(name="hogrest_1", more_dem=[0], less_dem=[1])

hogrest_2 = Indicator(name="hogrest_2", more_dem=[0], less_dem=[1])

hogrest_3 = Indicator(name="hogrest_3", more_dem=[0], less_dem=[1])

hogrest_4 = Indicator(name="hogrest_4", more_dem=[0], less_dem=[1])

hogrest_7 = Indicator(name="hogrest_7", more_dem=[0], less_dem=[1])

hogrest_10 = Indicator(name="hogrest_10", more_dem=[0], less_dem=[1])

lhrest_1 = Indicator(name="lhrest_1", more_dem=[0], less_dem=[1])

lhrest_2 = Indicator(name="lhrest_2", more_dem=[0], less_dem=[1])

lhrest_3 = Indicator(name="lhrest_3", more_dem=[0], less_dem=[1])

lhrest_4 = Indicator(name="lhrest_4", more_dem=[0], less_dem=[1])

lhrest_7 = Indicator(name="lhrest_7", more_dem=[0], less_dem=[1])

uhrest_1 = Indicator(name="uhrest_1", more_dem=[0], less_dem=[1])

uhrest_2 = Indicator(name="uhrest_2", more_dem=[0], less_dem=[1])

uhrest_3 = Indicator(name="uhrest_3", more_dem=[0], less_dem=[1])

uhrest_4 = Indicator(name="uhrest_4", more_dem=[0], less_dem=[1])

uhrest_7 = Indicator(name="uhrest_7", more_dem=[0], less_dem=[1])

lhselect_3 = Indicator(name="lhselect_3", more_dem=[1], less_dem=[0])

uhselect_3 = Indicator(name="uhselect_3", more_dem=[1], less_dem=[0])

jrempro_1 = Indicator(name="jrempro_1", more_dem=[0], less_dem=[1])

jrempro_2 = Indicator(name="jrempro_2", more_dem=[0], less_dem=[1])

jrempro_3 = Indicator(name="jrempro_3", more_dem=[0], less_dem=[1])

equalgr_1 = Indicator(name="equalgr_1", more_dem=[1])

equalgr_2 = Indicator(name="equalgr_2", more_dem=[1])

equalgr_3 = Indicator(name="equalgr_3", more_dem=[1])

equalgr_4 = Indicator(name="equalgr_4", more_dem=[1])

equalgr_5 = Indicator(name="equalgr_5", more_dem=[1])

equalgr_6 = Indicator(name="equalgr_6", more_dem=[1])

equalgr_7 = Indicator(name="equalgr_7", more_dem=[1])

equalgr_8 = Indicator(name="equalgr_8", more_dem=[1])

equalgr_9 = Indicator(name="equalgr_9", more_dem=[1])

equalgr_10 = Indicator(name="equalgr_10", more_dem=[1])

equalgr_11 = Indicator(name="equalgr_11", more_dem=[1])

equalgr_12 = Indicator(name="equalgr_12", more_dem=[1])

equalgr_13 = Indicator(name="equalgr_13", more_dem=[1])

equalgr_14 = Indicator(name="equalgr_14", more_dem=[1])

equalgr_15 = Indicator(name="equalgr_15", more_dem=[1])

equalgr_16 = Indicator(name="equalgr_16", more_dem=[1])

rightres_1 = Indicator(name="rightres_1", less_dem=[1])

rightres_2 = Indicator(name="rightres_2", less_dem=[1])

rightres_3 = Indicator(name="rightres_3", less_dem=[1])

rightres_4 = Indicator(name="rightres_4", less_dem=[1])

rightres_5 = Indicator(name="rightres_5", less_dem=[1])

rightres_6 = Indicator(name="rightres_6", less_dem=[1])

rightres_7 = Indicator(name="rightres_7", less_dem=[1])

rightres_8 = Indicator(name="rightres_8", less_dem=[1])

binding = Indicator(name="binding", more_dem=[1])
